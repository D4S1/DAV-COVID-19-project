import pandas as pd
import plotly.graph_objects as go
from utils import *
import plotly.express as px
import io
import PIL

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
		else:
			data=pd.read_csv(args[4])

			data=data.drop(['new_cases', 'new_deaths',  'total_deaths'],axis=1)
			data=data.rename(columns={"total_cases":"Australia (weekly)"})
			data2=pd.read_csv(args[7])
			data2=data2.drop(['new_cases', 'new_deaths',  'total_deaths'],axis=1)
			data2=data2.rename(columns={"total_cases":"Poland (weekly)"})
			data = pd.merge(data, data2,how="left", on=["date"])

			data2=pd.read_csv(args[2])
			data2=data2.drop(['confirmed' ,'deaths' ,'deaths_cum', 'tests', 'tests_cum', 'positives' ,'positives_cum' ,'recovered', 'recovered_cum',
				'hosp', 'hosp_cum', 'icu' ,'icu_cum' ,'vent', 'vent_cum', 'vaccines', 'vaccines_cum'],axis=1)
			data2=data2.rename(columns={"confirmed_cum":"Australia (daily)"})
			data = pd.merge(data, data2,how="outer", on=["date"])

			data2=pd.read_csv(args[5])
			data2=data2.drop(['confirmed' ,'deaths' ,'deaths_cum', 'tests', 'tests_cum', 'positives' ,'positives_cum' ,'recovered', 'recovered_cum'],axis=1)
			data2=data2.rename(columns={"confirmed_cum":"Poland (daily)"})

			data = pd.merge(data, data2,how="outer", on=["date"])
			data=data.sort_values("date")
			data['date'] = pd.to_datetime(data['date'])

			ymax=max(data[['Australia (weekly)', 'Australia (daily)', 'Poland (weekly)', 'Poland (daily)']].max())+1000000

			df = pd.DataFrame() # container for df with new datastructure
			for i in range(len(data["date"])):
				dfa = data.head(i).copy()
#				print(dfa)
				dfa['ix']=i
				df = pd.concat([df, dfa],  ignore_index=True)
			df=df.sort_values(["ix","date"]).reset_index()
#			print(df['ix']==155)
			fig = px.line(df, x = 'date', y = ['Australia (weekly)', 'Australia (daily)', 'Poland (weekly)', 'Poland (daily)'],
						  animation_frame='ix',
						  width=1200, height=900,range_x=[data["date"].min(),data["date"].max()],range_y=[0,ymax])
			fig.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True
			""" # works very slowly, looking for other options to save gif.
			frames = []
			for s, fr in enumerate(fig.frames):
				print(f"{s}/{len(data)}")
				# set main traces to appropriate traces within plotly frame
				fig.update(data=fr.data)
				# move slider to correct place
				fig.layout.sliders[0].update(active=s)
				# generate image of current state
				frames.append(PIL.Image.open(io.BytesIO(fig.to_image(format="png"))))
				
			"""


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