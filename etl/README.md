# ETL Process for OECD-DAC Dataset

This directory contains the ETL (Extract, Transform, Load) script to process OECD Development Assistance Committee (DAC) data into DDF format.

## Prerequisites

### Install Dependencies

```bash
pip install pandas ddf_utils
```

## Data Sources

You need to manually download the following source files from the OECD Data Explorer:

### 1. DAC5 Dataset (Table 5)

Download the full DAC5 dataset from:
https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CDevelopment%23DEV%23%7COfficial%20Development%20Assistance%20%28ODA%29%23DEV_ODA%23&pg=0&fc=Topic&bp=true&snb=27&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_DAC1%40DF_DAC5&df[ag]=OECD.DCD.FSD&df[vs]=1.4&dq=ALLD.528....Q.&lom=LASTNPERIODS&lo=5&to[TIME_PERIOD]=false

- Save as `etl/source/Table5_Data.zip`

### 2. DAC2a Dataset (Table 2a)

Download the full DAC2a dataset from:
https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CDevelopment%23DEV%23%7COfficial%20Development%20Assistance%20%28ODA%29%23DEV_ODA%23&pg=0&fc=Topic&bp=true&snb=27&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_DAC2%40DF_DAC2A&df[ag]=OECD.DCD.FSD&df[vs]=1.3

- Save as `etl/source/Table2a_Data.zip`

## Running the ETL Script

Once you have downloaded both source files, run the ETL script:

```bash
cd etl/scripts
python etl_notebook.py
```

