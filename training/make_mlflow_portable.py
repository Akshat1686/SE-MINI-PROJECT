"""Rewrite the MLflow experiment's artifact location to a relative path.

MLflow absolutizes the artifact location when the experiment is created,
which ties mlruns.db to the machine that trained. Run this after training
(and before zipping mlruns.db + mlruns/ as a CI artifact) so the store can
be opened on any machine::

    mlflow ui --backend-store-uri sqlite:///mlruns.db

Run from the repo root::

    python training/make_mlflow_portable.py
"""
import sqlite3
from pathlib import Path

from training.mlflow_utils import TRACKING_URI

DB = Path(TRACKING_URI.replace("sqlite:///", ""))


def main():
    con = sqlite3.connect(DB)
    con.execute("update experiments set artifact_location='./mlruns'")
    con.commit()
    print(f"{DB}: artifact locations rewritten to ./mlruns")


if __name__ == "__main__":
    main()
