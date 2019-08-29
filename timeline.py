import locale
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

#print(matplotlib.style.available)
matplotlib.style.use("seaborn")

class event:
    l_count= 0
    def __init__(self, begin, text, end=None, duration=None, level=None):
        if end and duration:
            raise("Can't specify both end and duration")
        self.begin= begin
        if duration:
            self.duration= duration
        elif end:
            self.duration= end-begin
        else:
            raise("Need to specify end or duration")

        if level == None:
            self.level= event.l_count
            event.l_count+=1
        else:
            self.level= level
        self.text= text

class milestone:
    def __init__(self, date, text):
        self.date= date
        self.text= text

from typing import List, Tuple

class timeline:
    def __init__(self, evs: List[event], 
                        ms: List[milestone], 
                        title: str="",
                        figsize: Tuple[int,int]= (15,5)):
        """
            Create matplotlib figure
        """
        plt.figure(figsize=figsize)
        self.ax = plt.subplot(111)
        self.ax.grid(False)
        self.ax.set_facecolor((0,0,0,0))
        self.evs= evs
        self.ms= ms
        self.title= title

    def plot_evs(self):
        """
            Plot the events
        """
        for e in self.evs:
            rev_lab= len(self.evs)-e.level
            self.ax.barh(rev_lab, e.duration.total_seconds()/(60*60*24), left=e.begin, color=(0,0.5,0.5,1))
            self.ax.text(e.begin+e.duration, rev_lab, e.text, weight='bold')
            # self.ax.plot([e.begin+e.duration, e.begin+e.duration], [rev_lab,  0.4], c= (0.5,0.5,0.5,0.6))

            self.ax.text(e.begin, rev_lab, "{} - {}".format(e.begin.strftime("%b %d"), (e.begin+e.duration).strftime("%b %d")), ha="right")

    def plot_timebar(self):
        ini= min(self.evs,key=lambda x: x.begin)
        end= max(self.evs,key=lambda x: x.begin+x.duration)
        total_dur= int((end.begin+end.duration-ini.begin).total_seconds()/(60*60*24*365))
        
        if total_dur <= 0:
            self.ax.text(ini.begin, -0.1, ini.begin.year, color=(1,1,1,1))
            self.ax.barh(0, int((end.begin+end.duration-ini.begin).total_seconds()/(60*60*24)), left=ini.begin, color=(0.3,0.3,0.4,1))

        cur_date= ini.begin
        for i in range(total_dur):
            to_next_year= cur_date.replace(year=cur_date.year+1,day=1,month=1)-cur_date
            to_next_year= to_next_year.days
            self.ax.text(cur_date, -0.1, cur_date.year, color=(1,1,1,1))
            self.ax.barh(0, to_next_year, left=cur_date, color=(0.3,0.3,0.4,1))
            cur_date= cur_date+timedelta(days=to_next_year+1)
        
        if (end.begin+end.duration-ini.begin).total_seconds()/(60*60*24*365)-total_dur > 0:
            self.ax.text(cur_date, -0.1, cur_date.year, color=(1,1,1,1))
            self.ax.barh(0, (end.begin+end.duration-cur_date).total_seconds()/(60*60*24), 
                                left=cur_date, color=(0.3,0.3,0.4,1))
    
    def plot_today(self):
        ini= min(self.evs,key=lambda x: x.begin)
        self.ax.barh(0, (datetime.now()-ini.begin).total_seconds()/(60*60*24), left=ini.begin, color=(0.3,0.7,0.3,1))
        #self.ax.text(datetime.now(), 0.5, "Today", color=(0,0,0,1))
        self.ax.annotate("Today", xy=(datetime.now(), 0.0), xytext=(datetime.now(), 1.5), arrowprops=dict(width=1, headwidth= 5, facecolor='black', shrink=0.01))
    
    def plot_mstone(self):
        for i, m in enumerate(self.ms):
            self.ax.text(m.date+timedelta(days=30), -3-i*1.2, m.date.strftime("%d %b"), fontsize=8)
            self.ax.annotate(m.text, xy=(m.date, 0), xytext=(m.date+timedelta(days=30), -3.5-i*1.2), annotation_clip=False, weight='bold',
                                arrowprops=dict(linewidth = 1.5, color = (0,0,1,1),
                                connectionstyle="angle,angleA=180,angleB=90,rad=0", arrowstyle="<-, head_width=0.3"))

    def show(self):
        self.ax.xaxis_date()
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        self.ax.yaxis.set_ticks([])
        plt.title(self.title,fontsize=20)
        plt.tight_layout()
        plt.show()
        event.l_count=0