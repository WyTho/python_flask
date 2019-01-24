import pandas as pd
from processing.analysis import DataFrameValidator
from processing.analysis import BinaryDataAnalysis


def analyze_fake_event_data():
    address = 'processing/analysis/fake_events/data.json'
    df_data = pd.read_json(address)
    validator = DataFrameValidator()
    dataframe_is_valid = validator.validate(df_data)

    if not dataframe_is_valid:
        return None
    else:
        BDASCAN = BinaryDataAnalysis()
        results = BDASCAN.analyze(df_data)
        return results
