import argparse
import os
import pathlib
from statsmodels.tsa.arima.model import ARIMA

def parse_args(name):
	WORKING_DIR=pathlib.Path(os.getcwd()).parent

	parser = argparse.ArgumentParser(description=f'Script gerating plor from task {name[4:]}',
		formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument('-AUn','--PATH_TO_AU_national',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing daly information about whole Australia; default: ./../data/COVID_AU_national.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_AU_national.csv")))
	parser.add_argument('-AUs','--PATH_TO_AU_states',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing daly information about states in Australia; default: ./../data/COVID_AU_state.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_AU_state.csv")))
	parser.add_argument('-AUy','--PATH_TO_AU_years',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing general weekly information about the whole  Australia; default: ./../data/COVID_AU_years.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_AU_years.csv")))

	parser.add_argument('-AUe','--PATH_TO_AU_excess',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing estimated excess ceath count for Australia; default: ./../data/COVID_AU_excess.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_AU_excess.csv")))
	parser.add_argument('-AUt','--PATH_TO_AU_tests',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about tests in Australia states; default: ./../data/COVID_AU_test_states.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_AU_test_states.csv")))
	parser.add_argument('-AUvs','--PATH_TO_AU_vac_states',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about tests in Australia states; default: ./../data/COVID_AU_vac_states.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_AU_vac_states.csv")))
	parser.add_argument('-AUv','--PATH_TO_AU_vac',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about tests in whole Australia; default: ./../data/COVID_AU_vac.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_AU_vacc.csv")))


	parser.add_argument('-PLn','--PATH_TO_PL_national',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing daly information about whole Poland; default: ./../data/COVID_PL_national.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_national.csv")))
	parser.add_argument('-PLs','--PATH_TO_PL_states',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing daly information about states in Poland; default: ./../data/COVID_PL_state.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_state.csv")))
	parser.add_argument('-PLy','--PATH_TO_PL_years',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing general weekly information about the whole  Poland; default: ./../data/COVID_PL_years.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_years.csv")))

	parser.add_argument('-PLe','--PATH_TO_PL_excess',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing estimated excess ceath count for Poland; default: ./../data/COVID_PL_excess.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_excess.csv")))
	parser.add_argument('-PLv','--PATH_TO_PL_vac',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about tests in whole Poland; default: ./../data/COVID_PL_vacc.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_vacc.csv")))


	parser.add_argument('-t','--PATH_TO_tests',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about tests in Poland and Australia; default: ./../data/COVID_test.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_test.csv")))	
	parser.add_argument('-hosp','--PATH_TO_hosp',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about hospitalised patients in Poland and Australia; default: ./../data/COVID_hospital.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_hospital.csv")))

	parser.add_argument('-nc','--PATH_TO_new_cases_per_m',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about new cases per milion in Poland and Australia; default: ./../data/COVID_new_cases_per_milion.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_new_cases_per_milion.csv")))
	parser.add_argument('-tc','--PATH_TO_total_cases_per_m',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about new cases per milion in Poland and Australia; default: ./../data/COVID_total_cases_per_milion.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_total_cases_per_milion.csv")))
	parser.add_argument('-nd','--PATH_TO_new_deaths_per_m',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about new cases per milion in Poland and Australia; default: ./../data/COVID_new_deaths_per_milion.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_new_deaths_per_milion.csv")))
	parser.add_argument('-td','--PATH_TO_total_deaths_per_m',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing information about new cases per milion in Poland and Australia; default: ./../data/COVID_total_deaths_per_milion.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_total_deaths_per_milion.csv")))

	parser.add_argument('-o','--PATH_TO_OUTPUT',metavar='OUTPUT_PATH',  action='store',nargs=1,type=pathlib.Path,
		help=f"""Path where output image will be saved, if s = 1;
		default: ./../images/{name}.[png/html/gif]""",default=None)
	parser.add_argument('s',nargs=1, help="""Selec mode:
* 0 - show interactive output image (default)
* 1 - save output static image(s) .png
* 2 - save interactive .html
* 3 - save animation .gif""",default=0,choices = [0,1,2,3],type=int,action='store')
	args = parser.parse_args()

	if isinstance(args.s, int):
		s=args.s
	else:
		s=args.s[0]
	# input check:
	if isinstance(args.PATH_TO_AU_national, pathlib.Path):
		data_AUn=args.PATH_TO_AU_national
	else:
		data_AUn=args.PATH_TO_AU_national[0]
	if not ( os.path.isfile(data_AUn) or os.path.isfile(os.path.abspath(data_AUn))):
		print(f"Input file not found, check if path is correct:\n{data_AUn}")
		data_AUn=None

	if isinstance(args.PATH_TO_AU_states, pathlib.Path):
		data_AUs=args.PATH_TO_AU_states
	else:
		data_AUs=args.PATH_TO_AU_states[0]
	if not ( os.path.isfile(data_AUs) or os.path.isfile(os.path.abspath(data_AUs))):
		print(f"Input file not found, check if path is correct:\n{data_AUs}")
		data_AUs=None

	if isinstance(args.PATH_TO_AU_years, pathlib.Path):
		data_AUy=args.PATH_TO_AU_years
	else:
		data_AUy=args.PATH_TO_AU_years[0]
	if not ( os.path.isfile(data_AUy) or os.path.isfile(os.path.abspath(data_AUy))):
		print(f"Input file not found, check if path is correct:\n{data_AUy}")
		data_AUy=None

	if isinstance(args.PATH_TO_PL_national, pathlib.Path):
		data_PLn=args.PATH_TO_PL_national
	else:
		data_PLn=args.PATH_TO_PL_national[0]
	if not ( os.path.isfile(data_PLn) or os.path.isfile(os.path.abspath(data_PLn))):
		print(f"Input file not found, check if path is correct:\n{data_PLn}")
		data_PLn=None

	if isinstance(args.PATH_TO_PL_states, pathlib.Path):
		data_PLs=args.PATH_TO_PL_states
	else:
		data_PLs=args.PATH_TO_PL_states[0]
	if not ( os.path.isfile(data_PLs) or os.path.isfile(os.path.abspath(data_PLs))):
		print(f"Input file not found, check if path is correct:\n{data_PLs}")
		data_PLs=None

	if isinstance(args.PATH_TO_PL_years, pathlib.Path):
		data_PLy=args.PATH_TO_PL_years
	else:
		data_PLy=args.PATH_TO_PL_years[0]
	if not ( os.path.isfile(data_PLy) or os.path.isfile(os.path.abspath(data_PLn))):
		print(f"Input file not found, check if path is correct:\n{data_PLy}")
		data_PLy=None


### new part
	if isinstance(args.PATH_TO_AU_excess, pathlib.Path):
		data_AUe=args.PATH_TO_AU_excess
	else:
		data_AUe=args.PATH_TO_AU_excess[0]
	if not ( os.path.isfile(data_AUe) or os.path.isfile(os.path.abspath(data_AUe))):
		print(f"Input file not found, check if path is correct:\n{data_AUe}")
		data_AUe=None
	if isinstance(args.PATH_TO_PL_excess, pathlib.Path):
		data_PLe=args.PATH_TO_PL_excess
	else:
		data_PLe=args.PATH_TO_PL_excess[0]
	if not ( os.path.isfile(data_PLe) or os.path.isfile(os.path.abspath(data_PLe))):
		print(f"Input file not found, check if path is correct:\n{data_PLe}")
		data_PLe=None

	if isinstance(args.PATH_TO_AU_vac, pathlib.Path):
		data_AUv=args.PATH_TO_AU_vac
	else:
		data_AUv=args.PATH_TO_AU_vac[0]
	if not ( os.path.isfile(data_AUv) or os.path.isfile(os.path.abspath(data_AUv))):
		print(f"Input file not found, check if path is correct:\n{data_AUv}")
		data_AUv=None
	if isinstance(args.PATH_TO_PL_vac, pathlib.Path):
		data_PLv=args.PATH_TO_PL_vac
	else:
		data_PLv=args.PATH_TO_PL_vac[0]
	if not ( os.path.isfile(data_PLv) or os.path.isfile(os.path.abspath(data_PLv))):
		print(f"Input file not found, check if path is correct:\n{data_PLv}")
		data_PLv=None
	if isinstance(args.PATH_TO_AU_vac_states, pathlib.Path):
		data_AUvs=args.PATH_TO_AU_vac_states
	else:
		data_AUvs=args.PATH_TO_AU_vac_states[0]
	if not ( os.path.isfile(data_AUvs) or os.path.isfile(os.path.abspath(data_AUvs))):
		print(f"Input file not found, check if path is correct:\n{data_AUvs}")
		data_AUvs=None
	if isinstance(args.PATH_TO_AU_tests, pathlib.Path):
		data_AUt=args.PATH_TO_AU_tests
	else:
		data_AUt=args.PATH_TO_AU_tests[0]
	if not ( os.path.isfile(data_AUt) or os.path.isfile(os.path.abspath(data_AUt))):
		print(f"Input file not found, check if path is correct:\n{data_AUt}")
		data_AUt=None

### new part - together
	if isinstance(args.PATH_TO_tests, pathlib.Path):
		data_t=args.PATH_TO_tests
	else:
		data_t=args.PATH_TO_tests[0]
	if not ( os.path.isfile(data_t) or os.path.isfile(os.path.abspath(data_t))):
		print(f"Input file not found, check if path is correct:\n{data_t}")
		data_t=None
	if isinstance(args.PATH_TO_hosp, pathlib.Path):
		data_h=args.PATH_TO_hosp
	else:
		data_h=args.PATH_TO_hosp[0]
	if not ( os.path.isfile(data_h) or os.path.isfile(os.path.abspath(data_h))):
		print(f"Input file not found, check if path is correct:\n{data_h}")
		data_h=None

	if isinstance(args.PATH_TO_new_cases_per_m, pathlib.Path):
		data_nc=args.PATH_TO_new_cases_per_m
	else:
		data_nc=args.PATH_TO_new_cases_per_m[0]
	if not ( os.path.isfile(data_nc) or os.path.isfile(os.path.abspath(data_nc))):
		print(f"Input file not found, check if path is correct:\n{data_nc}")
		data_nc=None
	if isinstance(args.PATH_TO_total_cases_per_m, pathlib.Path):
		data_tc=args.PATH_TO_total_cases_per_m
	else:
		data_tc=args.PATH_TO_total_cases_per_m[0]
	if not ( os.path.isfile(data_tc) or os.path.isfile(os.path.abspath(data_tc))):
		print(f"Input file not found, check if path is correct:\n{data_tc}")
		data_tc=None

	if isinstance(args.PATH_TO_new_deaths_per_m, pathlib.Path):
		data_nd=args.PATH_TO_new_deaths_per_m
	else:
		data_nd=args.PATH_TO_new_deaths_per_m[0]
	if not ( os.path.isfile(data_nd) or os.path.isfile(os.path.abspath(data_nd))):
		print(f"Input file not found, check if path is correct:\n{data_nd}")
		data_nd=None
	if isinstance(args.PATH_TO_total_deaths_per_m, pathlib.Path):
		data_td=args.PATH_TO_total_deaths_per_m
	else:
		data_td=args.PATH_TO_total_deaths_per_m[0]
	if not ( os.path.isfile(data_td) or os.path.isfile(os.path.abspath(data_td))):
		print(f"Input file not found, check if path is correct:\n{data_td}")
		data_td=None

	# output check:
	if args.PATH_TO_OUTPUT is None:
		if s==1:
			out=pathlib.Path(os.path.join(WORKING_DIR,f"images/{name}.png"))
		elif s==2:
			out=pathlib.Path(os.path.join(WORKING_DIR,f"images/{name}.html"))
		else:
			out=pathlib.Path(os.path.join(WORKING_DIR,f"images/{name}.gif"))
	elif isinstance(args.PATH_TO_OUTPUT, pathlib.Path):
		out=args.PATH_TO_OUTPUT
	else:
		out=args.PATH_TO_OUTPUT[0]
	if not ( os.path.isdir(out.parent) or os.path.isfile(os.path.abspath(out.parent))):
		print(f"Output directory not found, check if path is correct:\n{out}")
		out=None

	if out and data_AUn and data_AUy and data_AUs and data_PLn and data_PLy and data_PLs:
		return [out,s, data_AUn, data_AUs, data_AUy, data_PLn, data_PLs, data_PLy,
		 data_AUe, data_PLe, 			# 8, 9 		 - excess deaths
		 data_AUv, data_PLv, data_AUvs, # 10, 11, 12 - vaccinations
		 data_AUt, data_t, 				# 13, 14	 - tests
		 data_h,						# 15		 - hospitalised
		 data_nc, data_tc,				# 16, 17	 - new / total cases per milion
		 data_nd, data_td,				# 18, 19	 - new / total deaths per milion
		 ]

	else:

		return None
	
def get_mode():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Plot mode: 0 - show, 1 - save PNG, 2 - save HTML", type=int)
    args = parser.parse_args()
    return args.mode


def make_SARIMA(df_diff, p,s,d,w=0,t="c"):
	if w:
		if s:
			model = ARIMA(df_diff,seasonal_order=(p,s,d,w))
		else:
			model = ARIMA(df_diff,seasonal_order=(p,s,d,w),trend=t) 
	else:
		if s:
			model = ARIMA(df_diff,order=(p,s,d))
		else:
			model = ARIMA(df_diff,order=(p,s,d),trend=t) 
	model_fit = model.fit() 
	print(model_fit.summary())
	code = ""
	if s:
		code=f"ARIMA({p},{s},{d})"
	else:
		if p and d:
			code=f"ARMA({p},{d})"
		elif p:
			code=f"AR({p})"
		else:
			code=f"MA({d})"
	if w:
		code=f"S{code}".replace(")",f",{w})")
	return model_fit,code
