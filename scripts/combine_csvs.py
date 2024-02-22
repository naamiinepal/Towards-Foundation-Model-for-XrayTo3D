import argparse
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

parser = ArgumentParser()
parser.add_argument("first_dir")
parser.add_argument("second_dir")
parser.add_argument("--save-dir", required=True)

args = parser.parse_args()

print(args)

csvs = ["train", "train_noaug", "val", "test", "train+val"]

first_dir_csvs = sorted(list(Path(args.first_dir).rglob("*.csv")))
second_dir_csvs = sorted(list(Path(args.second_dir).rglob("*.csv")))

save_path = Path(args.save_dir) / "name_placeholder.csv"
# create intermediate directories if required
save_path.parent.mkdir(parents=True, exist_ok=True)

for csv_type in csvs:
    csv_suffix = csv_type + ".csv"
    first_csv = next(
        first_csv for first_csv in first_dir_csvs if str(first_csv).endswith(csv_suffix)
    )
    second_csv = next(
        second_csv for second_csv in second_dir_csvs if str(second_csv).endswith(csv_suffix)
    )

    print(first_csv.name, second_csv.name)

    first_df = pd.read_csv(first_csv, index_col=0)
    second_df = pd.read_csv(second_csv, index_col=0)

    combined_df = pd.concat((first_df, second_df))

    combined_df.to_csv(Path(save_path).with_name(csv_type).with_suffix(".csv"))
