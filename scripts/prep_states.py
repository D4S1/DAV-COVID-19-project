import pandas as pd

url = 'https://raw.githubusercontent.com/M3IT/COVID-19_Data/master/Data/COVID_AU_state.csv'
df_au = pd.read_csv(url)
df_au = df_au[['date', 'state', 'confirmed', 'confirmed_cum']]
df_au.to_csv('/home/hoshi/ME/Coding/DAV-COVID-19-project/data/AU_state_cases.csv')