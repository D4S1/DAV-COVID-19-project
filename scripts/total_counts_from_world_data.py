import pandas as pd
import gc

data=pd.read_csv("./../data/full_data.csv")

data_PL=data[data["location"]=="Poland"].reset_index()[["date","new_cases","new_deaths","total_cases","total_deaths"]]
data_AU=data[data["location"]=="Australia"].reset_index()[["date","new_cases","new_deaths","total_cases","total_deaths"]]

del data
gc.collect()

data_PL=data_PL.fillna(0)
data_AU=data_AU.fillna(0)
data_PL["new_cases"]=data_PL["new_cases"].astype('int')
data_PL["new_deaths"]=data_PL["new_deaths"].astype('int')
data_AU["new_cases"]=data_AU["new_cases"].astype('int')

data_AU["new_deaths"]=data_AU["new_deaths"].astype('int')

dates_PL=data_PL[data_PL["new_deaths"]!=0]["date"].values
dates_AU=data_AU[data_AU["new_deaths"]!=0]["date"].values

dates_AU=list(dates_AU)
dates_PL=list(dates_PL)
dates_AU.extend(dates_PL)
dates=sorted(list(set(dates_AU)))

del dates_PL
del dates_AU

gc.collect()


data_PL=data_PL[data_PL["date"].isin(dates) == True]
data_AU=data_AU[data_AU["date"].isin(dates) == True]

print(data_PL)
print(data_AU)

data_PL.to_csv("./../data/COVID_PL_years.csv",index=False)
data_AU.to_csv("./../data/COVID_AU_years.csv",index=False)