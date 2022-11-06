# Compaire Two Data Frames

As a Data Scientist we always start our job from data analasys, some time in this process we need to cross check the two data sets at column level or row level or each label level or null values level. There is no algarithem to perforn such kind of comperiion between two data sets. That's why I made this algarithem to achive all level of comperions betwwn two data sets.

    This algarithem helps to identify below differences
        1. column name differences.
        2. row number differences.
        3. Null values differences.
        4. Data / label differences.

## Environment Reqirments:
    Python Version - 3.8
    Pandas Version - 1.2.2

## How To Use

cmpr_dfs = CompareTwoDataFrames(df_1,df_2)

the above line represents the syntax of compare algorthm. this algorth should need two data frames df_1 and df_2

df_1 ---> first data frame  
df_2 ---> second data frame


    import pandas as pd
    from compare_two_data_frames import CompareTwoDataFrames

    df_1 = pd.read_csv('E:/DATA_SCIENCE/compare_two_data_frames/Data/Maths.csv')
    df_2 = pd.read_csv('E:/DATA_SCIENCE/compare_two_data_frames/Data/Portuguese.csv')

    data_diff = CompareTwoDataFrames(df_1, df_2)



## CompareTwoDataFrames Keys

column_diff  
clms_rows_count_diff  
null_value_diff  
values_diff 

| KEY                  |USE                                                               | SYNTAX       | 
| -------------------- | ---------------------------------------------------------------- | ---------- |
| column_diff          | Displays differences between columns of two data sets            | data_diff.column_diff|
| null_value_diff      | Displays differences of null values count between two data sets  | data_diff.null_value_diff|
| clms_rows_count_diff | Displays differences between row numbers                         | data_diff.clms_rows_count_diff|
| values_diff          | Displays differences of each and evry value                      | data_diff.values_diff|


