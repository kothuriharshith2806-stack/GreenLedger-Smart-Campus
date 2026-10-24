import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "sample_resource_readings.csv"

class TestGreenLedgerSampleData(unittest.TestCase):
    def test_file_exists_and_schema(self):
        self.assertTrue(DATA.exists())
        df = pd.read_csv(DATA)
        expected = {"date", "building", "electricity_kwh", "water_m3", "waste_kg", "data_status"}
        self.assertTrue(expected.issubset(df.columns))

    def test_sample_data_is_labelled(self):
        df = pd.read_csv(DATA)
        self.assertTrue(df["data_status"].astype(str).str.contains("SYNTHETIC SAMPLE").all())

    def test_positive_numeric_values(self):
        df = pd.read_csv(DATA)
        for col in ["electricity_kwh", "water_m3", "waste_kg"]:
            self.assertTrue(pd.to_numeric(df[col], errors="coerce").notna().all())
            self.assertTrue((pd.to_numeric(df[col]) > 0).all())

    def test_expected_sample_dimensions(self):
        df = pd.read_csv(DATA)
        self.assertEqual(df["building"].nunique(), 3)
        self.assertEqual(len(df), 90 * 3)

if __name__ == "__main__":
    unittest.main()
