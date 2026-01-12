# -*- coding: utf-8 -*-

from pathlib import Path

import pandas as pd

from ddf_utils.str import to_concept_id


source_table5 = "../source/Table5_Data.zip"
source_table2a = "../source/Table2a_Data.zip"
out_dir = "../../"


def gen_datapoints_total_oda(df: pd.DataFrame) -> pd.DataFrame:
    """Generate datapoints for total_oda from Table5."""
    # Filter for Total ODA (aid_type = 528) only
    df = df[df["AIDTYPE"] == 528].copy()

    cols = {
        "AMOUNTTYPE": "amount_type",
        "DONOR": "donor",
        "SECTOR": "sector",
        "Year": "year",
        "Value": "total_oda",
    }
    dp = df[list(cols.keys())].copy()
    dp = dp.rename(columns=cols)

    # Drop rows with empty values
    dp = dp.dropna(subset=["total_oda"])

    id_cols = ["amount_type", "donor", "sector"]
    for c in id_cols:
        dp[c] = dp[c].astype(str).map(to_concept_id)

    return dp.set_index(id_cols + ["year"])


def gen_datapoints_oda_gni(df: pd.DataFrame) -> pd.DataFrame:
    """Generate datapoints for oda_as_recipient_gni from Table2a."""
    # Filter for ODA as % GNI (Recipient)
    df = df[df["Aid type"] == "ODA as % GNI (Recipient)"].copy()

    cols = {
        "DATATYPE": "amount_type",
        "DONOR": "donor",
        "RECIPIENT": "recipient",
        "PART": "part",
        "Year": "year",
        "Value": "oda_as_recipient_gni",
    }
    dp = df[list(cols.keys())].copy()
    dp = dp.rename(columns=cols)

    # Drop rows with empty values
    dp = dp.dropna(subset=["oda_as_recipient_gni"])

    id_cols = ["amount_type", "donor", "recipient", "part"]
    for c in id_cols:
        dp[c] = dp[c].astype(str).map(to_concept_id)

    return dp.set_index(id_cols + ["year"])


def gen_datapoints_oda_per_capita(df: pd.DataFrame) -> pd.DataFrame:
    """Generate datapoints for oda_per_capita from Table2a."""
    # Filter for ODA per Capita
    df = df[df["Aid type"] == "ODA per Capita"].copy()

    cols = {
        "DATATYPE": "amount_type",
        "DONOR": "donor",
        "RECIPIENT": "recipient",
        "PART": "part",
        "Year": "year",
        "Value": "oda_per_capita",
    }
    dp = df[list(cols.keys())].copy()
    dp = dp.rename(columns=cols)

    # Drop rows with empty values
    dp = dp.dropna(subset=["oda_per_capita"])

    id_cols = ["amount_type", "donor", "recipient", "part"]
    for c in id_cols:
        dp[c] = dp[c].astype(str).map(to_concept_id)

    return dp.set_index(id_cols + ["year"])


def gen_entities_table5(df: pd.DataFrame) -> dict:
    """Generate entity dataframes from Table5."""
    entity_domains = {
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


def gen_entities_table2a(df: pd.DataFrame) -> dict:
    """Generate entity dataframes from Table2a."""
    entity_domains = {
        "recipient": ["RECIPIENT", "Recipient"],
        "part": ["PART", "Part"],
        "donor": ["DONOR", "Donor"],
        "amount_type": ["DATATYPE", "Amount type"],
    }
    entities = {}
    for concept, (id_col, name_col) in entity_domains.items():
        edf = df[[id_col, name_col]].drop_duplicates().copy()
        edf.columns = [concept, "name"]
        edf[concept] = edf[concept].astype(str).map(to_concept_id)
        edf = edf.sort_values(by=concept).reset_index(drop=True)
        entities[concept] = edf
    return entities


def merge_entities(entities_table5: dict, entities_table2a: dict) -> dict:
    """Merge entities from both tables, combining overlapping ones."""
    merged = {}

    # Add entities from table5
    for key, value in entities_table5.items():
        merged[key] = value

    # Add entities from table2a
    for key, value in entities_table2a.items():
        if key in merged:
            # Merge if exists (e.g., donor, amount_type)
            merged[key] = (
                pd.concat([merged[key], value])
                .drop_duplicates()
                .sort_values(by=key)
                .reset_index(drop=True)
            )
        else:
            merged[key] = value

    return merged


def gen_concepts() -> pd.DataFrame:
    """Generate concepts dataframe."""
    # manually insert some concepts
    concepts = [
        {
            "concept": "total_oda",
            "concept_type": "measure",
            "name": "Total ODA by sector and donor",
        },
        {
            "concept": "oda_as_recipient_gni",
            "concept_type": "measure",
            "name": "ODA as % of recipient GNI",
        },
        {
            "concept": "oda_per_capita",
            "concept_type": "measure",
            "name": "ODA per capita",
        },
        {"concept": "year", "concept_type": "time", "name": "Year"},
        {"concept": "name", "concept_type": "string", "name": "Name"},
    ]
    entity_domains = {
        "amount_type": "Amount type",
        "donor": "Donor",
        "sector": "Sector",
        "recipient": "Recipient",
        "part": "Part",
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
    # read data from Table5
    print("Reading Table5 data...")
    data_table5 = pd.read_csv(source_table5)

    # read data from Table2a
    print("Reading Table2a data...")
    data_table2a = pd.read_csv(source_table2a)

    # datapoints - total_oda
    print("Generating total_oda datapoints...")
    dp_total_oda = gen_datapoints_total_oda(data_table5)
    dp_total_oda.to_csv(
        Path(
            out_dir,
            "ddf--datapoints--total_oda--by--amount_type--donor--sector--year.csv",
        )
    )

    # datapoints - oda_as_recipient_gni
    print("Generating oda_as_recipient_gni datapoints...")
    dp_oda_gni = gen_datapoints_oda_gni(data_table2a)
    dp_oda_gni.to_csv(
        Path(
            out_dir,
            "ddf--datapoints--oda_as_recipient_gni--by--amount_type--donor--recipient--part--year.csv",
        )
    )

    # datapoints - oda_per_capita
    print("Generating oda_per_capita datapoints...")
    dp_oda_per_capita = gen_datapoints_oda_per_capita(data_table2a)
    dp_oda_per_capita.to_csv(
        Path(
            out_dir,
            "ddf--datapoints--oda_per_capita--by--amount_type--donor--recipient--part--year.csv",
        )
    )

    # entities
    print("Generating entities...")
    entities_table5 = gen_entities_table5(data_table5)
    entities_table2a = gen_entities_table2a(data_table2a)
    entities = merge_entities(entities_table5, entities_table2a)

    for k, v in entities.items():
        path = Path(out_dir, f"ddf--entities--{k}.csv")
        v.to_csv(path, index=False)

    # concepts
    print("Generating concepts...")
    cdf = gen_concepts()
    cdf.to_csv(Path(out_dir, "ddf--concepts.csv"), index=False)

    print("Done.")


if __name__ == "__main__":
    main()
