import pandas as pd
import plotly.graph_objects as go
from utils import *

def main():
	args = parse_args("plot1")
	if args:
		if args[1]<3 :
			
			data=pd.read_csv(args[4])

			fig = go.Figure()
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["total_cases"].values,
					mode='lines',
					name='Australia (weekly)'))
			data=pd.read_csv(args[2])
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["confirmed_cum"].values,
					mode='lines',
					name='Australia (daily)'))
			data=pd.read_csv(args[7])	
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["total_cases"].values,
					mode='lines',
					name='Poland (weekly)'))
			data=pd.read_csv(args[5])
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["confirmed_cum"].values,
					mode='lines',
					name='Poland (daily)'))

			fig.update_layout(
				xaxis=dict(
					title=dict(text='Date'),
					tickfont = dict(size=15),
				),
				yaxis=dict(
					title=dict(text='Cumulative number of noted cases'),
					tickfont = dict(size=15)
				),
				legend=dict(
					title=dict(
						text="Country"
					)
				),
				font=dict(
					size=20,
				),
				title=dict(
					text='Total number of noted cases (cumulative)',
					font=dict(size=30),
					x=0.5,
					xanchor='center',
				),			
			)


			if args[1]==2:
				fig.update_layout(
					width=1200,
					height=900)
				fig.write_html(f'{args[0]}', auto_open=False)
				print(args[0])
			elif args[1]==1:
				fig.update_layout(
					width=1500,
					height=1000)
				fig.write_image(f"{args[0]}")
			else:
	#			fig.write_html(f'{args[1]}', auto_open=True)
				fig.show()			


if __name__ == "__main__":
	main()