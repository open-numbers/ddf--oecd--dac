# -*- coding: utf-8 -*-

"""
"""

import json
from pathlib import Path

import pandas as pd
import numpy as np

from ddf_utils.str import to_concept_id

from ddf_utils.factory import oecd


source = '../source/TABLE5.json'
out_dir = '../../'


def main():
    data = json.load(open(source))

    # create datapoints
    dimensions = data['structure']['dimensions']
    series = data['dataSets'][0]['series']

    index_cols = [x['name'] for x in dimensions['series']]

    recs = []
    name = data['structure']['name']

    for i, v in series.items():
        idxs = list(map(int, i.split(':')))
        idx_dict = dict(zip(index_cols, idxs))
        for i, k in enumerate(idx_dict.keys()):
            assert i == dimensions['series'][i]['keyPosition']
            idx_dict[k] = dimensions['series'][i]['values'][idx_dict[k]]['id']
        for t, o in v['observations'].items():
            # TODO: might be the observations index is a list?
            year = int(dimensions['observation'][0]['values'][int(t)]['id'])

            rec = {}
            for k, v in idx_dict.items():
                rec[k] = v
            rec['year'] = year
            rec[name] = o[0]
            recs.append(rec)

    rdf = pd.DataFrame.from_records(recs)
    rdf.columns = rdf.columns.map(to_concept_id)
    rdf.amount_type = rdf.amount_type.map(to_concept_id)  # amount_type is in uppercase, fix it
    rdf = rdf.rename(columns={'aid_oda_by_sector_and_donor_dac5': 'oda'}) # rename the indicator

    (rdf.set_index(['aid_type', 'amount_type', 'donor', 'sector', 'year'])
        .to_csv(Path(out_dir,
                     'ddf--datapoints--oda--by--aid_type--amount_type--donor--sector--year.csv')))

    # create entities
    entities_concepts = []
    entities_dfs = {}

    for d in dimensions['series']:
        name = d['name']
        concept = to_concept_id(name)

        value_df = pd.DataFrame.from_records(d['values'])
        value_df.columns = [concept, 'name']

        entities_concepts.append({'concept': concept, 'name': name, 'concept_type': 'entity_domain'})
        entities_dfs[concept] = value_df

    for k, v in entities_dfs.items():
        path = Path(out_dir, f'ddf--entities--{k}.csv')
        v[k] = v[k].map(to_concept_id)
        v.to_csv(path, index=False)

    # create concepts

    # manually insert some concepts
    concepts = [
        {'concept': 'oda', 'concept_type': 'measure', 'name': 'Aid (ODA) by sector and donor'},
        {'concept': 'year', 'concept_type': 'time', 'name': 'Year'},
        {'concept': 'name', 'concept_type': 'string', 'name': 'Name'}
    ]

    cdf = pd.DataFrame.from_records([*concepts, *entities_concepts])
    cdf.to_csv(Path(out_dir, 'ddf--concepts.csv'), index=False)

    print('Done.')


if __name__ == '__main__':
    main()
