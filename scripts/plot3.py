import pandas as pd
import plotly.graph_objects as go
from utils import *
import plotly.express as px
import io
import PIL

def main():
	args = parse_args("plot3")
	if args:
		data=pd.read_csv(args[3])
		if args[1]==2 or args[1]==0 :
			
			

			fig = px.bar(data, x="state", y="confirmed", color="state",
			  animation_frame="date", animation_group="state", range_y=[0,data["confirmed"].max()+20]) # 

			new_xticks=data["state_abbrev"][:len(set(data["state"].values))].values
			fig.update_layout(
			xaxis_tickangle=0,
			xaxis=dict(
				title=dict(text='State'),
				tickfont = dict(size=15),
				tickmode = 'array',
				tickvals = [x for x in range(len(new_xticks))],
				ticktext=new_xticks
			))

		elif args[1]==1:
			fig = px.line(data, x = 'date',y="confirmed", color="state",
				range_x=[data["date"].min(),data["date"].max()],range_y=[0,data["confirmed"].max()+20])

			fig.update_layout(
			xaxis=dict(
				title=dict(text='Date'),
				tickfont = dict(size=15),

			))

		fig.update_layout(

			yaxis=dict(
				title=dict(text='Number of new confirmed cases'),
				tickfont = dict(size=15)
			),
			legend=dict(
				title=dict(
					text="State of Australia"
				)
			),
			font=dict(
				size=20,
			),
			title=dict(
				text='Daily number of new cases per state',
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
		elif args[1]==3:

			"""
			# create animated GIF
			frames[0].save(
					f"{args[0]}",
					save_all=True,
					append_images=frames[1:],
					optimize=True,
					duration=500,
					loop=0,
				)
			"""
			fig.show()
		else:
	#		fig.write_html(f'{args[1]}', auto_open=True)
			fig.show()	



if __name__ == "__main__":
	main()