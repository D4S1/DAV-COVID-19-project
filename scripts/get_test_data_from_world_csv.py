import pandas as pd
import gc

data=pd.read_csv("./../data/covid-testing-all-observations.csv",header=0)
data=data.rename(columns={"Entity":"country","ISO code":"code","Date":"date"})

print(data.columns.values)

data=data.drop(columns=['Source URL', 'Source label', 'Notes'])

data_AU=data[data["code"]=="AUS"].reset_index().drop(columns=["index"])
data_PL=data[data["code"]=="POL"].reset_index().drop(columns=["index"])

data_PL["country"]="Poland"
data_AU["country"]="Australia"

print(data_PL)
print(data_AU)




data=pd.concat([data_AU, data_PL]).reset_index().drop(columns=["index"])
del data_AU
del data_PL
gc.collect()

print(data)

data.to_csv("./../data/COVID_test.csv",index=False)
