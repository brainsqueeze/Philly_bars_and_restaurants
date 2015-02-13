import numpy as np
import pandas as pd
import datetime, time
import itertools


def FillOldTab():
    """
    Old tables do not have all of the detailed information.  Here I am finding
    that info from more recent lists and using that to fill in gaps in the old 
    tables.  I will only keep listings for which I can find the detailed info.
    """
    df14 = pd.read_csv('Lists/foobooz-50-best-bars-philadelphia_2014.tsv', sep='\t', index_col='Rank')
    df13 = pd.read_csv('Lists/foobooz-50-best-bars-philadelphia_2013.tsv', sep='\t', index_col='Rank').loc[:,['Bar']]
    df12 = pd.read_csv('Lists/foobooz-50-best-bars-philadelphia_2012.tsv', sep='\t', index_col='Rank').loc[:,['Bar']]
    df11 = pd.read_csv('Lists/foobooz-50-best-bars-philadelphia_2011.tsv', sep='\t', index_col='Rank').loc[:,['Bar']]
    df10 = pd.read_csv('Lists/foobooz-50-best-bars-philadelphia_2010.tsv', sep='\t', index_col='Rank').loc[:,['Bar']]
    df09 = pd.read_csv('Lists/foobooz-50-best-bars-philadelphia_2009.tsv', sep='\t', index_col='Rank').loc[:,['Bar']]

    Bar14 = pd.Series(df14['Bar'])
    Bar13 = pd.Series(df13['Bar'])
    Bar12 = pd.Series(df12['Bar'])
    Bar11 = pd.Series(df11['Bar'])
    Bar10 = pd.Series(df10['Bar'])
    Bar09 = pd.Series(df09['Bar'])
    
    int13 = pd.Series(list(set(Bar14).intersection(set(Bar13))))
    int12 = pd.Series(list(set(Bar14).intersection(set(Bar12))))
    int11 = pd.Series(list(set(Bar14).intersection(set(Bar11))))
    int10 = pd.Series(list(set(Bar14).intersection(set(Bar10))))
    int09 = pd.Series(list(set(Bar14).intersection(set(Bar09))))

    List13 = df13[Bar13.isin(int13)]
    List13 = List13.sort(['Bar'], ascending=True)
    List13 = pd.merge(List13, df14[Bar14.isin(int13)].sort(['Bar'], ascending=True).loc[:, ['Bar', 'Neighborhood', 'Address', 'Cuisine Category', 'Price']], on='Bar', left_index=True, right_index=False)

    List12 = df12[Bar12.isin(int12)]
    List12 = List12.sort(['Bar'], ascending=True)
    List12 = pd.merge(List12, df14[Bar14.isin(int12)].sort(['Bar'], ascending=True).loc[:, ['Bar', 'Neighborhood', 'Address', 'Cuisine Category', 'Price']], on='Bar', left_index=True, right_index=False)

    List11 = df11[Bar11.isin(int11)]
    List11 = List11.sort(['Bar'], ascending=True)
    List11 = pd.merge(List11, df14[Bar14.isin(int11)].sort(['Bar'], ascending=True).loc[:, ['Bar', 'Neighborhood', 'Address', 'Cuisine Category', 'Price']], on='Bar', left_index=True, right_index=False)

    List10 = df10[Bar10.isin(int10)]
    List10 = List10.sort(['Bar'], ascending=True)
    List10 = pd.merge(List10, df14[Bar14.isin(int10)].sort(['Bar'], ascending=True).loc[:, ['Bar', 'Neighborhood', 'Address', 'Cuisine Category', 'Price']], on='Bar', left_index=True, right_index=False)

    List09 = df09[Bar09.isin(int09)]
    List09 = List09.sort(['Bar'], ascending=True)
    List09 = pd.merge(List09, df14[Bar14.isin(int09)].sort(['Bar'], ascending=True).loc[:, ['Bar', 'Neighborhood', 'Address', 'Cuisine Category', 'Price']], on='Bar', left_index=True, right_index=False)

    df14['Year'] = 2014
    List13['Year'] = 2013
    List12['Year'] = 2012
    List11['Year'] = 2011
    List10['Year'] = 2010
    List09['Year'] = 2009
    Total = df14.sort(['Bar'], ascending=True).append([List13, List12, List11, List10, List09])

    Total.to_csv('Lists/Bars_total.tsv', sep='\t')

    List13.to_csv('Lists/2013_Bars_appended.tsv', sep='\t')
    List12.to_csv('Lists/2012_Bars_appended.tsv', sep='\t')
    List11.to_csv('Lists/2011_Bars_appended.tsv', sep='\t')
    List10.to_csv('Lists/2010_Bars_appended.tsv', sep='\t')
    List09.to_csv('Lists/2009_Bars_appended.tsv', sep='\t')
   
    


def main():
    FillOldTab()


    

if __name__ == '__main__':
    main()
