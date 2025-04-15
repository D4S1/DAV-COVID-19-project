import argparse
import os
import pathlib

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

	parser.add_argument('-PLn','--PATH_TO_PL_national',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing daly information about whole Poland; default: ./../data/COVID_PL_national.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_national.csv")))
	parser.add_argument('-PLs','--PATH_TO_PL_states',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing daly information about states in Poland; default: ./../data/COVID_PL_state.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_state.csv")))
	parser.add_argument('-PLy','--PATH_TO_PL_years',metavar='DATA_PATH',  type=pathlib.Path, action='store',nargs=1,
	  help="""Path to file containing general weekly information about the whole  Poland; default: ./../data/COVID_PL_years.csv""",
	  default=pathlib.Path(os.path.join(WORKING_DIR,"data/COVID_PL_years.csv")))

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
	if not ( os.path.isfile(data_PLy) or os.path.isfile(os.path.abspath(data_PLny))):
		print(f"Input file not found, check if path is correct:\n{data_PLy}")
		data_PLy=None

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
		return [out,s, data_AUn, data_AUs, data_AUy, data_PLn, data_PLs, data_PLy]

	else:

		return None