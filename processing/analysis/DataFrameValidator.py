import pandas as pd
import math


class DataFrameValidator:
    """Validate a Dataframe for use in BinaryDataAnalisys
       Be aware: the values for the time column are expected to be timestamps in milliseconds
    """
    time_column = 'time'
    expected_columns = ['id', 'state', time_column]
    minimum_days_of_data_needed = 7

    def validate(self, df):
        """Validate a dataframe with the values specified above

        Args:
            df: the dataframe to validate

        Returns:
            boolean: if it's valid or not
        """
        columns_valid = self.validate_columns(df)
        if not columns_valid:
            return False

        min_amount_of_data_valid = self.validate_minimum_days_of_data_needed(df)
        if not min_amount_of_data_valid:
            return False

        return True

    def validate_columns(self, df):
        """Validate a dataframe's columns with the values specified above

        Args:
            df: the dataframe to validate

        Returns:
            boolean: if the columns are valid or not
        """
        expected_df_columns = pd.DataFrame(columns=self.expected_columns)

        columns_too_many = df.columns.difference(expected_df_columns.columns)
        if not len(columns_too_many) == 0:
            print('The provided dataframe has too many columns:', *columns_too_many, sep='\n')

        columns_too_few = expected_df_columns.columns.difference(df.columns)
        if not len(columns_too_few) == 0:
            print('The provided dataframe is missing the following columns:', *columns_too_few, sep='\n')

        return len(columns_too_many) + len(columns_too_few) == 0

    def validate_minimum_days_of_data_needed(self, df):
        """Validate a dataframe's amount of data with the values specified above

        Args:
            df: the dataframe to validate

        Returns:
            boolean: if the data is valid or not
        """
        df_time = df.sort_values(by=[self.time_column])[self.time_column]
        first_timestamp = df_time.values[0]
        last_timestamp = df_time.values[-1]
        diff = last_timestamp - first_timestamp
        days = diff / 1000 / 60 / 60 / 24
        enough_data = days > self.minimum_days_of_data_needed

        if not enough_data:
            print(
                'There is a minimum of ' +
                str(self.minimum_days_of_data_needed) +
                ' days of data needed, only ' +
                str(math.floor(days * 100) / 100) +
                ' days of data was given!'
            )

        return enough_data
