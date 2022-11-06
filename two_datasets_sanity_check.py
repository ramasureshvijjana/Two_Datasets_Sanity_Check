from matplotlib.pyplot import axes
import pandas as pd
import copy
from itertools import chain

class TwoDatasetsSanityCheck:

    def __init__(self, df_1, df_2):

        # Converting column names into lower case.
        df_1.columns = df_1.columns.str.lower()
        df_2.columns = df_2.columns.str.lower()

        # Define all parameters.
        self.df_1 = df_1
        self.df_2 = df_2
        self.values_diff = ''
        self.column_diff = 'Both df_1 and df_2 columns names are same [No difference]'
        self.clms_rows_count_diff = pd.DataFrame()
        self.null_value_diff = pd.DataFrame() 
        self.rows_missing_in_df_1 = pd.DataFrame()
        self.rows_missing_in_df_2 = pd.DataFrame()
        self.status = ''
        self.comparing()

    def columns_compare(self):
        if sorted(self.df_1.columns) != sorted(self.df_2.columns):
            self.column_diff = dict()
            columns_not_in_df1 = [clm for clm in self.df_2.columns if clm not in self.df_1.columns]
            columns_not_in_df2 = [clm for clm in self.df_1.columns if clm not in self.df_2.columns]
            self.column_diff['df_2_extra_columns'] = columns_not_in_df1
            self.column_diff['df_1_extra_columns'] =  columns_not_in_df2

    def difference_caliculations(self):
        # Columns and rows count differences identifying and saving in a DataFrame.
        self.clms_rows_count_diff = pd.DataFrame([self.df_1.shape, self.df_2.shape], columns=['Rows', 'Columns'], index=['df_1', 'df_2'])

        # Null values comparison.
        df_1_null_values = self.df_1.isna().sum()
        df_2_null_values = self.df_2.isna().sum()
        unique_columns = set(chain(list(df_1_null_values.index), list(df_2_null_values.index)))

        self.null_value_diff = pd.DataFrame([[idx, df_1_null_values[idx], df_2_null_values[idx]] \
        if idx in df_1_null_values.index and idx in df_2_null_values.index \
        else ([idx, 'Column not exist', df_2_null_values[idx]] if idx not in df_1_null_values.index \
        else ([idx, df_1_null_values[idx], 'Column not exist'] if idx not in df_2_null_values.index \
        else 'Column not exist')) for idx in unique_columns], \
        columns=['Column Name', 'df_1 null values', 'df_2 null values'])

    def missing_rows(self):

        identical_df_1, identical_df_2 = copy.copy(self.df_1), copy.copy(self.df_2)

        if type(self.column_diff) == dict:
            if len(self.column_diff['df_1_extra_columns']) != 0: identical_df_1.drop(columns = self.column_diff['df_1_extra_columns'], inplace=True)
            if len(self.column_diff['df_2_extra_columns']) != 0: identical_df_2.drop(columns = self.column_diff['df_2_extra_columns'], inplace=True)

        df_2_clms = identical_df_1.columns.to_list()
        df_1_clms = identical_df_2.columns.to_list()

        if df_1_clms == df_2_clms:
            rows_missing_in_df_2 = pd.merge(identical_df_1, identical_df_2, on=df_1_clms, how='left', indicator='Exist')
            self.rows_missing_in_df_2 = rows_missing_in_df_2[rows_missing_in_df_2.Exist == 'left_only'].drop('Exist', axis=1)

            rows_missing_in_df_1 = pd.merge(identical_df_2, identical_df_1, on=df_1_clms, how='left', indicator='Exist')
            self.rows_missing_in_df_1 = rows_missing_in_df_1[rows_missing_in_df_1.Exist == 'left_only'].drop('Exist', axis=1)
        if len(self.rows_missing_in_df_2) == 0: self.rows_missing_in_df_2 = 'All df_1 rows prasent in df_2'
        if len(self.rows_missing_in_df_1) == 0: self.rows_missing_in_df_1 = 'All df_2 rows prasent in df_1'
        

    def comparing(self):
        try:
            self.values_diff = self.df_1.compare(self.df_2)
            if len(self.values_diff) == 0: self.values_diff = 'No values difference between two datasets' 
            self.columns_compare()
            self.difference_caliculations()
            self.status = 'Both data is similar'
            self.missing_rows()
        except ValueError or KeyError as e:
            # display error
            self.status = 'Both data not similar'
            self.values_diff = 'Columns or Rows are not identical'
            # column difference
            self.columns_compare()
            # row difference
            self.difference_caliculations()
            self.missing_rows()

            pass

####################
