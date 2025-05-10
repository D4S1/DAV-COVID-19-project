import pandas as pd
import gc

data=pd.read_csv("./../data/Total Tests By State And Territory.csv",header=1)
data=data.rename(columns={"Date":"date"})
columns=data.columns.values[1:]

for i in range(int(len(columns)/2)):
	data.loc[data[columns[2*i]]=="-",columns[2*i]]=None
	data[columns[2*i]]=data[columns[2*i]].apply(lambda x: str(x).replace(",",""))
	data.loc[data[columns[2*i+1]]=="-",columns[2*i+1]]=None
	data[columns[2*i+1]]=data[columns[2*i+1]].apply(lambda x: str(x).replace(",",""))
	data=data.rename(columns={columns[i*2]:f"{columns[i*2]}_cum",f"{columns[i*2+1]}":f"{columns[i*2]}_new"})

data["date"]=pd.to_datetime(data["date"],dayfirst=True)
print(data)

data.to_csv("./../data/COVID_AU_test_states.csv",index=False)