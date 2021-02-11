'''
This is VERY quick and Dirty. 

Good luck trying to understand it! I don't.

'''

import folium
from folium.plugins import HeatMapWithTime
import csv,datetime,os,pytz
import pandas
data=[]
d=[]
times=[]
t=[]
donme=[]
with open("ParlerVideoFromCapitol.csv","r") as csvf:
    csvf.seek(0)
    readCSV = csv.reader(csvf, delimiter=',')
    for x in readCSV:
        try:
            d.append([float(x[1]),float(x[0]),datetime.datetime.strptime(x[2],"%Y-%m-%d %H:%M:%S").replace(
                tzinfo=pytz.utc).astimezone(pytz.timezone("EST5EDT"))])
        except Exception as e:
            print(e)
    oldt=d[0][2]
    temp=[]
    print(oldt)
    ct=None
    eday=oldt-datetime.timedelta(hours=oldt.hour,minutes=oldt.minute)
    oday = oldt-datetime.timedelta(hours=oldt.hour,minutes=oldt.minute)
    while(oday.day==eday.day):
        oday=oday+datetime.timedelta(minutes=15)
        for p in d:
            if (p[2]-oday).seconds>=0 and (p[2]-oday).seconds<=15*60:
                print("td c")
                ct = datetime.datetime.strftime(oday, "%H:%M")
                if ct in donme:
                    print("ct in donme")
                    temp.append([p[0],p[1]])
                else:
                    print('no ct in dm')
                    if len(temp)>0:
                        print("t fil")
                        data.append(temp)
                        times.append(datetime.datetime.strftime(oday, "%H:%M"))
                        temp=[]
                    temp.append([p[0],p[1]])
                    donme.append(ct)
                    d.remove(p)
    
    #https://www.reddit.com/r/dataisbeautiful/comments/kvx88n
    #See this Reddit post for the output :)
    hmap = folium.Map(location=[38.88, -77.02], zoom_start=2)
    hm_wide = HeatMapWithTime(data=data,index=times,min_opacity=0.2,auto_play=True,max_speed=3)
    hmap.add_child(hm_wide)
    hmap.save('parlerVideoData.html')
