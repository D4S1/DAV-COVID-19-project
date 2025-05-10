import pandas as pd
import gc

data=pd.read_csv("./../data/covid-hospitalizations.csv",header=0)
data=data.rename(columns={"entity":"country","iso_code":"code"})

data_AU=data[data["country"]=="Australia"].reset_index().drop(columns=["index"])
data_PL=data[data["country"]=="Poland"].reset_index().drop(columns=["index"])

columns=list(set(data_AU["indicator"].values))
columns.extend(list(set(data_PL["indicator"].values)))
columns=sorted(list(set(columns)))

dates_PL=set(data_PL["date"].values)
dates_AU=set(data_AU["date"].values)

dates_AU=sorted(list(dates_AU))
dates_PL=sorted(list(dates_PL))
dates=dates_AU.copy()
dates.extend(dates_PL)
dates=sorted(list(set(dates)))

print(f"datest_AU:\t{len(dates_AU)}\ndatest_PL:\t{len(dates_PL)}\ndatest_total:\t{len(dates)}")

data_PL_tmp=pd.DataFrame({"date":dates_PL,"country":data_PL.loc[0,"country"],"code":data_PL.loc[0,"code"]},index=dates_PL)
for c in columns:
	data_PL_tmp[c]=None
	if c in set(data_PL["indicator"].values):
		tmp=data_PL[data_PL["indicator"]==c][["date","value"]]
		tmp.index=tmp["date"]
		data_PL_tmp.loc[tmp["date"],c] = tmp["value"]
data_PL_tmp=data_PL_tmp.sort_values("date").reset_index().drop(columns=["index"])


data_AU_tmp=pd.DataFrame({"date":dates_AU,"country":data_AU.loc[0,"country"],"code":data_AU.loc[0,"code"]},index=dates_AU)
for c in columns:
	data_AU_tmp[c]=None
	if c in set(data_AU["indicator"].values):
		tmp=data_AU[data_AU["indicator"]==c][["date","value"]]
		tmp.index=tmp["date"]
		data_AU_tmp.loc[tmp["date"],c] = tmp["value"]
data_AU_tmp=data_AU_tmp.sort_values("date").reset_index().drop(columns=["index"])


data=pd.concat([data_AU_tmp, data_PL_tmp]).reset_index().drop(columns=["index"])
del data_AU_tmp
del data_PL_tmp
del data_AU
del data_PL
del tmp
gc.collect()

data.to_csv("./../data/COVID_hospital.csv",index=False)