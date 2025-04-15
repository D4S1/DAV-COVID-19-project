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


data=data[data["wojewodztwo"].isin(["Cały kraj"]) == False]
data=data.groupby(["Date","wojewodztwo" ]).sum().reset_index()

# change numbers to int:

data["zgony"]=data["zgony"].astype('int')
data["liczba_przypadkow"]=data["liczba_przypadkow"].astype('int')
data["liczba_wykonanych_testow"]=data["liczba_wykonanych_testow"].astype('int')
data["liczba_testow_z_wynikiem_pozytywnym"]=data["liczba_testow_z_wynikiem_pozytywnym"].astype('int')
data["liczba_ozdrowiencow"]=data["liczba_ozdrowiencow"].astype('int')

# preprare lists:
date=[]
state=[]

deaths=[]
confirmed=[]
test=[]
positives=[]
recovered=[]

deaths_cum=[]
confirmed_cum=[]
test_cum=[]
positives_cum=[]
recovered_cum=[]

print(data)
print(data[["Date","zgony","wojewodztwo","liczba_przypadkow"]])
print(data.shape)
print(data.columns)
print(data["Date"].values)
print(data["wojewodztwo"].values)
#print(data.isna().sum())
print(data.isnull().sum(axis = 0))

print(f"{data['zgony']}")
print(f"{data['zgony_w_wyniku_covid_i_chorob_wspolistniejacych']+data['zgony_w_wyniku_covid_bez_chorob_wspolistniejacych']}")


for w in list(set(data["wojewodztwo"].values)):
	data_tmp=data[data["wojewodztwo"].isin([w]) == True].reset_index()


	deaths_cum.append(data_tmp["zgony"][0])
	confirmed_cum.append(data_tmp["liczba_przypadkow"][0])
	test_cum.append(data_tmp["liczba_wykonanych_testow"][0])
	positives_cum.append(data_tmp["liczba_testow_z_wynikiem_pozytywnym"][0])
	recovered_cum.append(data_tmp["liczba_ozdrowiencow"][0])

	date.extend(data_tmp["Date"].values)
	state.extend(data_tmp["wojewodztwo"].values)

	deaths.extend(data_tmp["zgony"].values)
	confirmed.extend(data_tmp["liczba_przypadkow"].values)
	positives.extend(data_tmp["liczba_testow_z_wynikiem_pozytywnym"].values)
	test.extend(data_tmp["liczba_wykonanych_testow"].values)
	recovered.extend(data_tmp["liczba_ozdrowiencow"].values)

	for i in range(1,data_tmp.shape[0]):
		deaths_cum.append(deaths_cum[-1]+data_tmp["zgony"][i])
		confirmed_cum.append(confirmed_cum[-1]+data_tmp["liczba_przypadkow"][i])
		test_cum.append(test_cum[-1]+data_tmp["liczba_wykonanych_testow"][i])
		positives_cum.append(positives_cum[-1]+data_tmp["liczba_testow_z_wynikiem_pozytywnym"][i])
		recovered_cum.append(recovered_cum[-1] + data_tmp["liczba_ozdrowiencow"][i])


#print(recovered_cum)

#print(f"length deaths: {len(deaths_cum)} {deaths_cum}")
#print(f"length confirmed: {len(confirmed_cum)} {confirmed_cum}")

codes=[]
for w in state:
	codes.append(state_code[w])

new_data=pd.DataFrame({"date":date,
	"state":state,
	"state_abbrev":codes,
	"confirmed":confirmed,
	"confirmed_cum":confirmed_cum,
	"deaths":deaths,
	"deaths_cum":deaths_cum,
	"tests":test,
	"tests_cum":test_cum,
	"positives":positives,
	"positives_cum":positives_cum,
	"recovered":recovered,
	"recovered_cum":recovered_cum
	})
new_data.sort_values(["date"]).reset_index()

print(new_data)

new_data.to_csv("./../data/COVID_PL_state.csv",index=False)

