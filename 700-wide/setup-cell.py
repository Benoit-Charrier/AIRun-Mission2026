# K 7.W.1 — Setup cell (DuckDB + Python workspace)
# Verified: 2026-07-02 | Environment: Python 3.14 + DuckDB 1.5.4

import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install",
                "duckdb>=1.4", "pandas", "numpy", "matplotlib", "plotly",
                "--quiet"], check=True)

import duckdb
import pandas as pd
import os, random
import numpy as np
from datetime import datetime

# In-memory DuckDB connection
con = duckdb.connect()

con.execute("""
    CREATE TABLE hello_world (
        id INTEGER,
        message VARCHAR,
        created_at TIMESTAMP
    )
""")
con.execute("""
    INSERT INTO hello_world VALUES
        (1, 'Pipeline kata workspace ready', NOW()),
        (2, 'DuckDB version: """ + duckdb.__version__ + """', NOW()),
        (3, 'Reference case: Nordstar Customer 360', NOW())
""")

result = con.execute("SELECT * FROM hello_world").fetchdf()
print(result.to_string(index=False))
print("\nEnvironment ready [OK]")
