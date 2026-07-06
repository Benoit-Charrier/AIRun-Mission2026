import pathlib
import sys

# Make the 500-wide root importable so `from src.logsum import ...` works in tests
sys.path.insert(0, str(pathlib.Path(__file__).parent))
