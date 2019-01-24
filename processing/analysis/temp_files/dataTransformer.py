import pandas as pd
from processing.analysis import DataFrameValidator
from processing.analysis import BinaryDataAnalysis


def do_shit():

    # TEMP #
    address = './staandelamp_realistic_huge.json'
    df_data = pd.read_json(address)
    df_data = df_data.sort_values(by=['time'])
    df_data['id'] = df_data['name']
    df_data = df_data.drop(columns=['name'])
    # TEMP #

    validator = DataFrameValidator()
    dataframe_is_valid = validator.validate(df_data)

    if not dataframe_is_valid:
        print('ERROR! Dataframe validation failed!')
    else:
        print('Dataframe is valid!')
        BDASCAN = BinaryDataAnalysis()
        result = BDASCAN.analyze(df_data)
        print(result[:5])
