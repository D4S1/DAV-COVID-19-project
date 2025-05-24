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

def main():
	args = parse_args("plot12")
	if args:
		if args[1]<3 :
			
			data=pd.read_csv(args[19])

			ymin=0
			ymax=max([data["Poland"].max(),data["World"].max(),data["Australia"].max()])
			fig = go.Figure()
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["Poland"].values,
					mode='lines',
					name='Poland',
					line=dict(color='rgb(0,0,250)'),))
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["World"].values,
					mode='lines',
					name='World',
					line=dict(color='rgb(250,0,0)'),))
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["Australia"].values,
					mode='lines',
					name='Australia',
					line=dict(color='rgb(0,100,0)'),))

			# Add waves of COVID
			d=10
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
					title=dict(text='Cumulative deaths per milion'),
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
					text='Total number of deaths per milion of population',
					font=dict(size=30),
					x=0.5,
					xanchor='center',
				),			
			)

		else:
			data=pd.read_csv(args[19])
			ymin=0
			ymax=max([data["Poland"].max(),data["World"].max(),data["Australia"].max()])
			data = data.loc[((data["Poland"].isna()==False) & (data["World"].isna()==False) & (data["Australia"].isna()==False))]
			values=data[["Australia","Poland","World"]].values
			names=["Australia","Poland","World"]
			code = ["AUS","POL","ALL"]
			dates=data["date"].copy().values
			xs =data["date"].copy().values
			for d in range(len(dates)):
				dates[d] = mdates.datestr2num(dates[d])
				xs[d]=str(xs[d])
			xdata = []
			ydata=[[] for i in range(len(names))]
			yCIdata=[[[],[]] for i in range(len(names))]
			omi_w_start = mdates.datestr2num('2021-12-14')
			omi_w_end = mdates.datestr2num('2023-12-14')
			delta_w_start = mdates.datestr2num('2021-6-16')
			last=[0 for x in range(len(ydata))]

	#		print(f"number of steps: {len(dates)}\nshape of values:\t{values.shape}\t\n" )#shape of CI:\t{CI[0].shape}\t{CI[1].shape}\nymin = {ymin}\tymax = {ymax}")
			sns.set_theme(style="darkgrid")
			fig, ax = plt.subplots(figsize=(10,7.5))   


			lplot = ax.plot(np.array(dates[0]),np.array([[0],[0],[0]]).T,label=names)
#			fplot1 = ax.fill_between(np.array(dates[0]),np.array([0]),np.array([0]))
#			fplot2 = ax.fill_between(np.array(dates[0]),np.array([0]),np.array([0]))
			fig.legend(bbox_to_anchor=(0.32,0.87),title="Countries",fontsize=15,title_fontsize=18) # 
			ymin=ymin-100
			ymax=ymax*1.1
			yval=[]
			ylab=["0"]
			for i in range(7):
				yval.append(i*500)
				if i:
					ylab.append(f"{i*0.5}k")
			def init():
				ax.set_ylim(ymin, ymax)
				ax.set_xlim(dates[0],dates[-1]+60)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel('Cumulative cases per milion',size=18)
				del xdata[:]
				for i in range(len(ydata)):
					del ydata[i][:]
#					for j in range(len(yCIdata[i])):
#						del yCIdata[i][j][:]
				t = ax.text(dates[65], yval[-1]*0.68  ,xs[0], size=30, va="center", ha="center",)
				last=[0,0,0]
				return lplot,t

			def update(frame):
				ax.cla()

				xdata.append(dates[frame])
				for i in range(len(ydata)):
					ydata[i].append(values[frame][i])
					
					if ydata[i] is None:
						y=last[i]
					else:
						y=ydata[i][-1]
						last[i] =ydata[i][-1]
					ax.text(xdata[-1]+0.5, y ,code[i], size=15, va="center", ha="left")

#					for j in range(2):
#						yCIdata[i][j].append(CI[i][frame][j])

#				print(f"x = {xdata}\ny = {ydata}\nCI: {yCIdata}")
				
#				fplot1 = ax.fill_between(np.array(xdata),np.array(yCIdata[0][0]),np.array(yCIdata[0][1]),alpha=0.3,color="C0")
#				fplot2 = ax.fill_between(np.array(xdata),np.array(yCIdata[1][0]),np.array(yCIdata[1][1]),alpha=0.3,color="C1")
				wplot1 = ax.fill_betweenx([ymin,ymax],delta_w_start,omi_w_start,alpha=0.3,color="tab:green")
				wplot2 = ax.fill_betweenx([ymin,ymax],omi_w_start,omi_w_end,alpha=0.3,color='tab:olive')
				ax.text((delta_w_start+omi_w_start)/2, yval[-1]*1.04 ,f"Delta\nWave", size=15, va="center", ha="center",)
				ax.text((omi_w_end+omi_w_start)/2, yval[-1]*1.05 ,f"Omicron Wave", size=15, va="center", ha="center",)
				for i in range(len(ydata)):
					tmp=np.array(ydata[i]).astype(np.double)
					mask = np.isfinite(tmp)
#					print(f"frame = {frame},\ti = {i}\ntmp = {tmp.shape}\nmask = {mask.shape}\ndata={len(xdata)}\nnewY = {tmp[mask]}")
					lplot = ax.plot(np.array(xdata)[mask],tmp[mask],linestyle='-', marker='o',label=names[i],ms=0.5)
				ax.set_title('Total number of deaths per milion of population',size=20)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel('Cumulative deaths per milion',size=18)
				ax.set(ylim=[ymin, ymax])
				ax.set_xlim(dates[0],dates[-1]+120)
				ax.set_yticks(np.array(yval), ylab,size=12)
				t=ax.text(dates[10], yval[-1]*0.75 ,f"{xs[frame]}", size=25, va="center", ha="left",)
				
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