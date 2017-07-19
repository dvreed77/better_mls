import requests
from mls_scraper.settings import GOOGLE_KEY

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

%matplotlib inline

copley = [42.3502089,-71.0768681]
home = [42.3369546,-71.0751955]



lng_bounds = [-71.1249301, -71.0235092]
lat_bounds = [42.3767355, 42.3145089]
n_points = 10
dlat = np.abs(lat_bounds[1] - lat_bounds[0])/n_points
dlng = np.abs(lng_bounds[1] - lng_bounds[0])/n_points

out = []

lnr = np.arange(min(lng_bounds), max(lng_bounds), dlng)[:n_points]
ltr = np.arange(min(lat_bounds), max(lat_bounds), dlat)[:n_points]

X, Y = np.meshgrid(lnr, ltr)

for i in range(n_points):
    for j in range(n_points):
        out.append((ltr[i], lnr[j]))

out2 = []

for o in out:
    t = get_distance_duration(o, copley)
    out2.append((o, t))

Z = np.empty((n_points, n_points))
for i in range(len(out2)):
    Z[int(i/n_points), int(i%n_points)] = out2[i][1][0]['value']



plt.figure()
CS = plt.contour(X, Y, Z, 20)
plt.clabel(CS, inline=1, fontsize=10)


from mls_scraper.models import LatLngGrid, MLSListing
from mls_scraper import db

db.create_all()




lng_bounds = [-71.1249301, -71.0235092]
lat_bounds = [42.3767355, 42.3145089]
create_grid('grid_10', [lng_bounds, lat_bounds], 10)






from scipy import interpolate

f = interpolate.interp2d(lnr, ltr, Z, kind='cubic')

f(-71.025135, 42.3357757)


url = 'https://maps.googleapis.com/maps/api/directions/json'

params = {
    'origin': '%f,%f' % (42.3357757,-71.025135),
    'destination': '%f,%f' % (copley[0], copley[1]),
    'key': GOOGLE_KEY,
    # 'mode': 'walking',
    'mode': 'transit'
}

r = requests.get(url, params)
out = r.json()
distance = out['routes'][0]['legs'][0]['distance']
duration = out['routes'][0]['legs'][0]['duration']

duration


e = 42.3379544,-70.9878652
w = 42.3264574,-71.1767246
n = 42.3827608,-71.1050284
s = 42.2916585,-71.0993726
bounds = [w[1],e[1],s[0],n[0]]


from mls_scraper.analysis import create_grid, fill_grid, get_grid
copley = [42.3502089,-71.0768681]


create_grid(label='grid_10', bounds=bounds, n_points=10)

fill_grid('grid_10', copley, 'walking')

x,y,Z = get_grid('grid_10', 'walking', 'duration')

X, Y = np.meshgrid(x, y)

plt.figure()
CS = plt.contour(X, Y, Z, 20)
plt.clabel(CS, inline=1, fontsize=10)
