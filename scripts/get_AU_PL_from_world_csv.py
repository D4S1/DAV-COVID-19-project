import pandas as pd
import gc

types = ["new_cases","new_deaths","total_cases","total_deaths"]

for t in types:
	data=pd.read_csv(f"./../data/{t}_per_million.csv",header=0)

	data=data[["date","World","Australia","Poland"]]
	ind=data[data["World"]>0].index
	"""
	for i,idx in enumerate(ind[1:]):
		if idx!=ind[i]+7:
			print(f"last date: {data.loc[idx,'date']}, current idx: {idx}\tlast idx: {ind[i]+7}" )
	"""
	tmp=data.loc[ind[0]:ind[-1],:]

	tmp.loc[((tmp["World"] == 0) & (tmp["Australia"] == 0) & (tmp["Poland"] == 0)),["World","Poland","Australia"]]=None
	data.loc[ind[0]:ind[-1],:]=tmp

	del tmp
	gc.collect()

	data.to_csv(f"./../data/COVID_{t}_per_milion.csv",index=False)
