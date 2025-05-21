import pandas as pd
import plotly.graph_objects as go
from utils import *
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import seaborn as sns

codes={
	"NSW":"New South Wales",
	"VIC":"Victoria",
	"QLD":"Queensland",
	"WA" :"Western Australia",
	"SA" :"South Australia",
	"TAS":"Tasmania",
	"ACT":"Australia Capital Territory",
	"NT" :"Northern Territory"
}

def main():
	args = parse_args("plot19")
	if args:

		ylabel="Number of new vaccinations"
		ptitle="Number of new vaccinations by state of Australia"
		data=pd.read_csv(args[12])
		todrop=[f"{key}_cum" for key in list(codes.keys())]
		torename=dict(zip([f"{key}_new" for key in list(codes.keys())],list(codes.values())))
		data=data.drop(columns=todrop)
		data=data.rename(columns=torename)
		ymin=0
		ymax=max(data[list(codes.values())].max())

		if args[1]<3 :



			fig = go.Figure()
			for c,n in codes.items(): 
				fig.add_trace(go.Scatter(x=data["date"], y=data[n],
						mode='lines',
						name=n,
						hovertext=c,
				))

			# Add waves of COVID
			d=10
			"""
			fig.add_vline(x='2020-11-1', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			"""
			fig.add_vline(x='2021-6-16', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			fig.add_vline(x='2021-12-14', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			fig.add_vline(x='2023-12-14', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			"""
			fig.add_trace(go.Scatter(x=['2020-11-1','2020-11-1'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='End of wave 2',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2021-6-16','2021-6-16'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='Start of Delta Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2021-12-14','2021-12-14'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='End of Delta Wave\nStart of Omicron Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2023-12-14','2023-12-14'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='End of Omicron Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			"""
			## add retrangulars 
			fig.add_vrect(x0 = '2021-6-16',x1 = '2021-12-14',  
					annotation_text="Delta Wave",annotation_position="top right",
					fillcolor="blue", opacity=0.25, line_width=0,
					annotation=dict(font_size=20  ), #, font_family="Times New Roman")
					)
			fig.add_vrect(x0 = '2021-12-14',x1 = '2023-12-14',  
					annotation_text="Omicron Wave",annotation_position="top right",
					fillcolor="yellow", opacity=0.25, line_width=0,
					annotation=dict(font_size=20) # , font_family="Times New Roman")
					)
			fig.update_layout(
				xaxis=dict(
					title=dict(text='Date'),
					tickfont = dict(size=15),
				),
				yaxis=dict(
					title=dict(text=ylabel),
					tickfont = dict(size=15)
				),
				legend=dict(
					title=dict(
						text="State"
					)
				),
				font=dict(
					size=20,
				),
				title=dict(
					text=ptitle,
					font=dict(size=30),
					x=0.5,
					xanchor='center',
				),			
			)

		else:
			values=data[list(codes.values())] # [data[c].values for c in list(codes.values())]
			names=list(codes.values())
			code =list(codes.keys())
			dates=data["date"].copy().values
			xs =data["date"].copy().values
			for d in range(len(dates)):
				dates[d] = mdates.datestr2num(dates[d])
				xs[d]=str(xs[d])
			xdata = []
			ydata=[[] for i in range(len(names))]

			omi_w_start = mdates.datestr2num('2021-12-14')
			omi_w_end = mdates.datestr2num('2023-12-14')
			delta_w_start = mdates.datestr2num('2021-6-16')
			last=[0 for x in range(len(ydata))]

			sns.set_theme(style="darkgrid")
			fig, ax = plt.subplots(figsize=(15,7.5),layout='constrained')   


			lplot = ax.plot(np.array(dates[0]),np.array([[0] for x in range(len(code))]).T,label=names)
			fig.legend(loc = 'outside right center',title="States",fontsize=15,title_fontsize=18) # bbox_to_anchor=(0.32,0.87)
			ymin=ymin-100
			ymax=ymax*1.1
			yval=[]
			ylab=["0"]
			for i in range(10):
				yval.append(i*20000)
				if i:
					ylab.append(f"{i*20}k")
			def init():
				ax.set_ylim(ymin, ymax)
				ax.set_xlim(dates[0],dates[-1]+60)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel(ylabel,size=18)
				del xdata[:]
				for i in range(len(ydata)):
					del ydata[i][:]

				t = ax.text(dates[65], yval[-1]*0.68  ,xs[0], size=30, va="center", ha="center",)
				last=[0 for x in range(len(ydata))]
				return lplot,t

			def update(frame):
				ax.cla()

				xdata.append(dates[frame])
				for i in range(len(ydata)):
					ydata[i].append(values.loc[frame,names[i]])
					ax.text(xdata[-1]+0.5, ydata[i][-1] ,code[i], size=15, va="center", ha="left")
				
				wplot1 = ax.fill_betweenx([ymin,ymax],delta_w_start,omi_w_start,alpha=0.3,color="tab:green")
				wplot2 = ax.fill_betweenx([ymin,ymax],omi_w_start,omi_w_end,alpha=0.3,color='tab:olive')
				ax.text((delta_w_start+omi_w_start)/2, yval[-1]*1.04 ,f"Delta\nWave", size=15, va="center", ha="center",)
				ax.text((omi_w_end+omi_w_start)/2, yval[-1]*1.05 ,f"Omicron Wave", size=15, va="center", ha="center",)
				for i in range(len(ydata)):
					tmp=np.array(ydata[i]).astype(np.double)
					mask = np.isfinite(tmp)
					lplot = ax.plot(np.array(xdata)[mask],tmp[mask],linestyle='-', marker='o',label=names[i],ms=0.5)
				ax.set_title(ptitle,size=20)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel(ylabel,size=18)
				ax.set(ylim=[ymin, ymax])
				ax.set_xlim(dates[0],dates[-1]+120)
				ax.set_yticks(np.array(yval), ylab,size=12)
				t=ax.text(dates[10], yval[-1]-1e4 ,f"{xs[frame]}", size=25, va="center", ha="left",)
				
				# you can not use grid:
				ax.grid()  
				ax.grid(axis="both",which='major', color='white', linewidth=1.2)
				ax.grid(axis="both",which='minor', color='white', linewidth=0.5)
				ax.minorticks_on()
				# Now hide the minor ticks (but leave the gridlines).
				ax.xaxis.set_major_locator(mdates.YearLocator())
				ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
				ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%Y'))
				ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

				return (lplot,t)
				
			ani = animation.FuncAnimation(fig=fig, func=update, frames=len(dates), interval=100,init_func=init)
			plt.show()


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
			writergif = animation.PillowWriter(fps=13)
			ani.save(args[0], writer=writergif)
		else:
	#		fig.write_html(f'{args[1]}', auto_open=True)
			fig.show()	

if __name__ == "__main__":
	main()