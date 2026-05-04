import re
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif":['Times New Roman'],
    "font.size": 12,
    "axes.linewidth": 1.5,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "legend.frameon": False
})

def dist(lat1,lon1,lat2,lon2):
    R = 6371e3

    phi1,phi2 = np.radians(lat1),np.radians(lat2)

    dphi = np.radians(phi2-phi1)

    dlambda = np.radians(lon2-lon1)

    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2

    return 2*R*np.arcsin(np.sqrt(a))

def autocorrl(k,e):

    A = []
    e_mean = np.mean(e)
    e_var = np.var(e,ddof=1)

    for i in range(k):
        if i == 0:
            o = np.mean((e - e_mean) * (e - e_mean))
        else:
            o = np.mean((e[:-i] - e_mean) * (e[i:] - e_mean))
        
        A.append(o / e_var)
    
    return A

dists,times = [],[]

with open(r'\data\2026-04-14-135538.gpx', 'r', encoding='utf-8') as f:
    data = f.read()

pattern = r'lat="([-0-9.]+)" lon="([-0-9.]+)".*?<time>(.*?)</time>'
matches = re.findall(pattern,data)

lat = np.array([float(m[0]) for m in matches])
lon = np.array([float(m[1]) for m in matches])
time = np.array([datetime.fromisoformat(m[2].replace('Z','')) for m in matches])

for i in range(1,len(lat)):
    d = dist(lat[i-1],lon[i-1],lat[i],lon[i])

    t = (time[i]-time[i-1]).total_seconds()

    if t>0:
        dists.append(d)
        times.append(t)

dists = np.array(dists)
times = np.array(times)

cumdist = np.cumsum(dists)          
cumtime = np.cumsum(times) / 60 

marks = np.arange(0, cumdist[-1], 1)

time_marks = np.interp(marks, cumdist, cumtime)

pace = []

for i in range(1, len(marks)):
    d = (marks[i] - marks[i-1]) / 1000      
    t = (time_marks[i] - time_marks[i-1])  

    pace.append(t / d)

pace = np.array(pace)
print(np.mean(pace))
time_plot = time_marks[1:]

km = 100
acrr = autocorrl(km,pace)
kappa = np.arange(0,km,1)


plt.plot(kappa,acrr,marker='o',linestyle='--')
plt.xlabel('k')
plt.ylabel('A(k)')
plt.ylim(0,1.2)
plt.show()

