# DAV-COVID-19-project

## Articles about stituation in Australia
* [www.aihw.gov.au](https://www.aihw.gov.au/reports/australias-health/covid-19)
* [covidbaseau.com](https://covidbaseau.com/timeline/) - timeline of epidemy described by days/weeks

## paths to data repositories:
* Australia: [https://github.com/M3IT/COVID-19_Data](https://github.com/M3IT/COVID-19_Data)
* Australia: [https://covidbaseau.com/](https://covidbaseau.com/)
* Poland: [https://github.com/Polkas/coronaPL/tree/main](https://github.com/Polkas/coronaPL/tree/main)
* general dataset: [https://github.com/owid/covid-19-data/tree/master](https://github.com/owid/covid-19-data/tree/master)
## selected data tables:
(because some tables are merged and lack some informations)

### General:
* [test](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_test.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/testing/covid-testing-all-observations.csv)\)
* [new_cases_per_milion](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_new_cases_per_milion.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/new_cases_per_million.csv)\)
* [new_deaths_per_milion](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_new_deaths_per_milion.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/new_deaths_per_million.csv)\)
* [total_cases_per_milion](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_total_cases_per_milion.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/total_cases_per_million.csv)\)
* [total_deaths_per_milion](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_total_deaths_per_milion.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/total_deaths_per_million.csv)\)
* [hospitalized](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_hospital.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/hospitalizations/covid-hospitalizations.csv)\)


### Australia:
* [states](https://github.com/M3IT/COVID-19_Data/blob/master/Data/COVID_AU_state.csv)
* [country](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_AU_national.csv), \(corrected from [source](https://github.com/M3IT/COVID-19_Data/blob/master/Data/COVID_AU_national.csv) delated negative new cases\)
* [general counts](https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/full_data.csv)
* [excess deaths](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_AU_excess.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/excess_mortality/excess_mortality.csv), selecting only Australia \)
* [vaccination](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_AU_vacc.csv) \(Adapted from [source](https://raw.githubusercontent.com/owid/covid-19-data/refs/heads/master/public/data/vaccinations/vaccinations.csv), selecting only Australia \)
* [vaccination per state](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_AU_vac_states.csv) \(Adapted from [source](https://covidbaseau.com/historical/?title=Jurisdiction%20Doses%20Administered&return=https://covidbaseau.com/vaccinations/)\)
 
### Poland:
* [states](https://github.com/Polkas/coronaPL/blob/main/gov/data/pow_df_full.csv.gz)
* [country](https://github.com/Polkas/coronaPL/blob/main/gov/data/pow_df_full.csv.gz)
* [general counts](https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/full_data.csv)
* [excess deaths](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_PL_excess.csv) \(Adapted from [source](https://github.com/owid/covid-19-data/blob/master/public/data/excess_mortality/excess_mortality.csv), selecting only Poland \)
* [vaccination](https://github.com/D4S1/DAV-COVID-19-project/blob/main/data/COVID_PL_vacc.csv) \(Adapted from [source](https://raw.githubusercontent.com/owid/covid-19-data/refs/heads/master/public/data/vaccinations/vaccinations.csv), selecting only Poland \)

(data from daily datasets for country separatly except cases and case_cum have some worring behavior - check plot5)

## Plots

- (Basic) Poland vs Australia (cases) line  plot animated \[ \], inteactive \[+\], static \[+\]
- (Basic) Poland vs Australia (deaths) line  plot animated \[ \], inteactive \[+\], static \[+\]
- (Basic) Warsaw vs Austrialia states bar plot (new cases)- animated / beg and end (or static lineplot)
- (Basic) Warsaw vs Austrialia states bar plot (...)- animated / beg and end 
- (Basic) Map plot with concentration of COVID cases
- (Basic) Map plot with concentration of COVID death
- (Stats) Histogram X  - number of people in hospital Y -  number of days
- (Stats) Regression ? 
- (Stats) Trend line based on linear model (split to 2 periods)
