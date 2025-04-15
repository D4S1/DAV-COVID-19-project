import pandas as pd
import numpy as np

"""
pow_df_full = pd.read_csv("https://raw.githubusercontent.com/Polkas/coronaPL/main/gov/data/pow_df_full.csv.gz", encoding_errors='ignore')
pow_df_full.to_csv("./../data/COVID_PL_national_full.csv")
"""


data=pd.read_csv("./../data/COVID_PL_national_full.csv")

if_STATES=False

#print(list(set(data["wojewodztwo"].values)))
state_code={'kujawsko-pomorskie':"KP",
 'mazowieckie':"MZ", 
 'opolskie':"OP", 
 'wielkopolskie':"WP",
 'świętokrzyskie':"SK", 
 'warmińsko-mazurskie':"WN",
 'podlaskie':"PD", 
 'małopolskie':"MA",
 'podkarpackie':"PK", 
 'pomorskie':"PM", 
 'śląskie':"SL", 
 'zachodniopomorskie':"ZP", 
 'dolnośląskie':"DS", 
 'łódzkie':"LD", 
 'lubuskie':"LB", 
 'lubelskie':"LU"}

### to make COVID_PL_national.csv
if if_STATES:
	data=data[data["wojewodztwo"].isin(["Cały kraj"]) == False]
	data=data.groupby(["Date","wojewodztwo" ]).sum()
else :
	data=data[data["wojewodztwo"].isin(["Cały kraj"]) == True]




data=data.reset_index()
print(data)
print(data[["Date","zgony","wojewodztwo","liczba_przypadkow"]])
print(data.shape)
print(data.columns)
print(data["Date"].values)
print(data["wojewodztwo"].values)
#print(data.isna().sum())
print(data.isnull().sum(axis = 0))
data["zgony"]=data["zgony"].astype('int')
data["liczba_przypadkow"]=data["liczba_przypadkow"].astype('int')
data["liczba_wykonanych_testow"]=data["liczba_wykonanych_testow"].astype('int')
data["liczba_testow_z_wynikiem_pozytywnym"]=data["liczba_testow_z_wynikiem_pozytywnym"].astype('int')
print(f"{data['zgony']}")
print(f"{data['zgony_w_wyniku_covid_i_chorob_wspolistniejacych']+data['zgony_w_wyniku_covid_bez_chorob_wspolistniejacych']}")

print(f"{data['liczba_przypadkow']}")
deaths_cum=[data["zgony"][0]]
confirmed_cum=[data["liczba_przypadkow"][0]]
test_cum=[data["liczba_wykonanych_testow"][0]]
positives_cum=[data["liczba_testow_z_wynikiem_pozytywnym"][0]]
if np.isnan(data["liczba_ozdrowiencow"][0]):
	recovered=[np.nan]
	recovered_cum=[np.nan]	
else:
	recovered=[data["liczba_ozdrowiencow"][0].astype(int).item()]
	recovered_cum=[data["liczba_ozdrowiencow"][0].astype(int).item()]
print(recovered_cum)
#print(data["zgony"][5])
for i in range(1,data.shape[0]):
	deaths_cum.append(deaths_cum[-1]+data["zgony"][i])
	confirmed_cum.append(confirmed_cum[-1]+data["liczba_przypadkow"][i])
	test_cum.append(test_cum[-1]+data["liczba_wykonanych_testow"][i])
	positives_cum.append(positives_cum[-1]+data["liczba_testow_z_wynikiem_pozytywnym"][i])
	if np.isnan(data["liczba_ozdrowiencow"][i]) and np.isnan(recovered_cum[-1]):
		recovered_cum.append(np.nan)
		recovered.append(data["liczba_ozdrowiencow"][i])
	elif not np.isnan(data["liczba_ozdrowiencow"][i]) and np.isnan(recovered_cum[-1]):
		recovered_cum.append(data["liczba_ozdrowiencow"][i].astype(int).item())
		recovered.append(data["liczba_ozdrowiencow"][i].astype(int).item())
	elif np.isnan(data["liczba_ozdrowiencow"][i]) and not np.isnan(recovered_cum[-1]):
		recovered_cum.append(recovered_cum[-1])
		recovered.append(data["liczba_ozdrowiencow"][i])
	else:
		recovered_cum.append(recovered_cum[-1]+data["liczba_ozdrowiencow"][i].astype(int).item())
		recovered.append(data["liczba_ozdrowiencow"][i].astype(int).item())

#print(recovered_cum)

#print(f"length deaths: {len(deaths_cum)} {deaths_cum}")
#print(f"length confirmed: {len(confirmed_cum)} {confirmed_cum}")

new_data=pd.DataFrame({"date":data["Date"].values,
	"confirmed":data["liczba_przypadkow"],
	"confirmed_cum":confirmed_cum,
	"deaths":data["zgony"].values,
	"deaths_cum":deaths_cum,
	"tests":data["liczba_wykonanych_testow"].values,
	"tests_cum":test_cum,
	"positives":data["liczba_testow_z_wynikiem_pozytywnym"].values,
	"positives_cum":positives_cum,
	"recovered":pd.Series(recovered, dtype=object),
	"recovered_cum":pd.Series(recovered_cum, dtype=object)
	})
if if_STATES:
	new_data["state"]=data["wojewodztwo"]
	codes=[]
	for w in data["wojewodztwo"].values:
		codes.append(state_code[w])
	new_data["state_abbrev"]=codes

print(new_data)
if if_STATES:

	new_data.to_csv("./../data/COVID_PL_state.csv",index=False)
else:
	new_data.to_csv("./../data/COVID_PL_national.csv",index=False)	

