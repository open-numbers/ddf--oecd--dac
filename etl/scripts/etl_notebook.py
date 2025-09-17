# -*- coding: utf-8 -*-

from pathlib import Path

import pandas as pd

from ddf_utils.str import to_concept_id


source = "../source/Table5_Data.zip"
out_dir = "../../"


def gen_datapoints(df: pd.DataFrame) -> pd.DataFrame:
    """Generate datapoints dataframe."""
    cols = {
        "AIDTYPE": "aid_type",
        "AMOUNTTYPE": "amount_type",
        "DONOR": "donor",
        "SECTOR": "sector",
        "Year": "year",
        "Value": "oda",
    }
    dp = df[list(cols.keys())].copy()
    dp = dp.rename(columns=cols)

    id_cols = ["aid_type", "amount_type", "donor", "sector"]
    for c in id_cols:
        dp[c] = dp[c].astype(str).map(to_concept_id)

    return dp.set_index(id_cols + ["year"])


def gen_entities(df: pd.DataFrame) -> dict:
    """Generate all entity dataframes."""
    entity_domains = {
        "aid_type": ["AIDTYPE", "Aid type"],
        "amount_type": ["AMOUNTTYPE", "Amount type"],
        "donor": ["DONOR", "Donor"],
        "sector": ["SECTOR", "Sector"],
    }
    entities = {}
    for concept, (id_col, name_col) in entity_domains.items():
        edf = df[[id_col, name_col]].drop_duplicates().copy()
        edf.columns = [concept, "name"]
        edf[concept] = edf[concept].astype(str).map(to_concept_id)
        edf = edf.sort_values(by=concept).reset_index(drop=True)
        entities[concept] = edf
    return entities


def gen_concepts() -> pd.DataFrame:
    """Generate concepts dataframe."""
    # manually insert some concepts
    concepts = [
        {"concept": "oda", "concept_type": "measure", "name": "Aid (ODA) by sector and donor"},
        {"concept": "year", "concept_type": "time", "name": "Year"},
        {"concept": "name", "concept_type": "string", "name": "Name"},
    ]
    entity_domains = {
        "aid_type": "Aid type",
        "amount_type": "Amount type",
        "donor": "Donor",
        "sector": "Sector",
    }
    entities_concepts = []
    for concept, name in entity_domains.items():
        entities_concepts.append(
            {"concept": concept, "name": name, "concept_type": "entity_domain"}
        )

    cdf = pd.DataFrame.from_records([*concepts, *entities_concepts])
    return cdf


def main():
    """main function to run ETL"""
    # read data
    data = pd.read_csv(source)

    # datapoints
    dp = gen_datapoints(data)
    (
        dp.to_csv(
            Path(
                out_dir, "ddf--datapoints--oda--by--aid_type--amount_type--donor--sector--year.csv"
            )
        )
    )

    # entities
    entities = gen_entities(data)
    for k, v in entities.items():
        path = Path(out_dir, f"ddf--entities--{k}.csv")
        v.to_csv(path, index=False)

    # concepts
    cdf = gen_concepts()
    cdf.to_csv(Path(out_dir, "ddf--concepts.csv"), index=False)

    print("Done.")


if __name__ == "__main__":
    main()
