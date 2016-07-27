# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file

# configuration of file paths
source = '../source/Table5_Data.csv'
out_dir = '../../'


def extract_entities_donor(data):
    donor = data[['DONOR', 'Donor']].copy()
    donor.columns = ['donor', 'name']
    donor = donor.drop_duplicates()

    return donor


def extract_entities_sector(data):
    sector = data[['SECTOR', 'Sector']].drop_duplicates().copy()
    sector.columns = ['sector', 'name']

    return sector


def extract_concepts():
    # manually create this one
    cdf = pd.DataFrame([['total_oda', 'Total ODA', 'measure'],
                        ['year', 'Year', 'time'],
                        ['name', 'Name', 'string'],
                        ['donor', 'Donor', 'entity_domain'],
                        ['sector', 'Sector', 'entity_domain']
                        ], columns=['concept', 'name', 'concept_type'])

    return cdf


def extract_datapoints(data):
    # AIDTYPE == 528: only include Total ODA
    # AMOUNTTYPE == 'D': only include data in 2014 USD
    dps = data.query("AIDTYPE == 528 & AMOUNTTYPE == 'D'")\
          [['DONOR', 'SECTOR', 'Year', 'Value']].copy()

    dps.columns = ['donor', 'sector', 'year', 'total_oda']

    return dps.dropna().drop_duplicates()


if __name__ == '__main__':
    data = pd.read_csv(source)

    print('creating concepts files...')
    path = os.path.join(out_dir, 'ddf--concepts.csv')
    cdf = extract_concepts()
    cdf.to_csv(path, index=False)

    print('creating entities files...')
    # donor
    path = os.path.join(out_dir, 'ddf--entities--donor.csv')
    donor = extract_entities_donor(data)
    donor.to_csv(path, index=False)

    # sector
    path = os.path.join(out_dir, 'ddf--entities--sector.csv')
    sector = extract_entities_sector(data)
    sector.to_csv(path, index=False)

    print('creating datapoints files...')
    dps = extract_datapoints(data)
    path = os.path.join(out_dir,
                        'ddf--datapoints--total_oda--by--donor--sector--year.csv')
    dps.to_csv(path, index=False)

    print('creating index files...')
    create_index_file(out_dir)

    print('Done.')
