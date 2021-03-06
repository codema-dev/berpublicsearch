import csv
import json
from os import path
from pathlib import Path
from shutil import unpack_archive

from dask.diagnostics import ProgressBar
import dask.dataframe as dd


HERE = Path(__file__).parent


def convert_to_parquet(input_dirpath: str, output_filepath: str) -> None:
    """Convert csv file to parquet.

    Args:
        input_dirpath (str): Path to unzipped input directory
        output_filepath (str): Path to output data
    """
    with open(HERE / "dtypes.json", "r") as json_file:
        dtypes = json.load(json_file)

    ber_raw = dd.read_csv(
        path.join(input_dirpath, "BERPublicsearch.txt"),
        sep="\t",
        low_memory=False,
        dtype=dtypes,
        encoding="latin-1",
        quoting=csv.QUOTE_NONE,
    )

    with ProgressBar():
        ber_raw.to_parquet(output_filepath, engine="pyarrow")
