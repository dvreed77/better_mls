import requests
from mls_scraper.settings import GOOGLE_KEY

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

%matplotlib inline

copley = [42.3502089,-71.0768681]
home = [42.3369546,-71.0751955]

def get_distance_duration(origin, destination):
    url = 'https://maps.googleapis.com/maps/api/directions/json'

    params = {
        'origin': '%f,%f' % (origin[0], origin[1]),
        'destination': '%f,%f' % (destination[0], destination[1]),
        'key': GOOGLE_KEY,
        'mode': 'walking'
    }

    r = requests.get(url, params)
    out = r.json()
    distance = out['routes'][0]['legs'][0]['distance']
    duration = out['routes'][0]['legs'][0]['duration']
    return distance['value'], duration['value']


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


from mls_scraper.models import LatLngGrid
from mls_scraper import db

db.create_all()

# idx = db.Column(db.Integer)
# lat = db.Column(db.Float)
# lng = db.Column(db.Float)
# distance = db.Column(db.Float)
# duration = db.Column(db.Float)
# label = db.Column(db.String)
def create_grid(label, bounds, n_points):
    lng_bounds = bounds[0]
    lat_bounds = bounds[1]
    dlng = np.abs(lng_bounds[1] - lng_bounds[0])/n_points
    dlat = np.abs(lat_bounds[1] - lat_bounds[0])/n_points

    lnr = np.arange(min(lng_bounds), max(lng_bounds), dlng)[:n_points]
    ltr = np.arange(min(lat_bounds), max(lat_bounds), dlat)[:n_points]

    for idx in range(n_points*n_points):
        iy = int(idx/n_points)
        ix = int(idx%n_points)
        llg = LatLngGrid(
        idx=idx,
        lat=ltr[iy],
        lng=lnr[ix],
        label=label
        )
        db.session.add(llg)
    db.session.commit()


lng_bounds = [-71.1249301, -71.0235092]
lat_bounds = [42.3767355, 42.3145089]
create_grid('grid_10', [lng_bounds, lat_bounds], 10)

llgs = LatLngGrid.query.filter(
    LatLngGrid.label=='grid_10',
    LatLngGrid.distance == None
).all()

for llg in llgs:
    distance, duration = get_distance_duration([llg.lat, llg.lng], copley)
    llgs[0].distance = distance
    llgs[0].duration = duration

db.session.commit()


llgs = LatLngGrid.query.filter(
    LatLngGrid.label=='grid_10'
).order_by(LatLngGrid.idx).all()


lnr = [x.lng for x in llgs[:10]]
ltr = [x.lat for x in llgs[::10]]

ltr
lnr
n_points = 10
Z = np.empty((10, 10))
for i in range(len(llgs)):
    Z[int(i/n_points), int(i%n_points)] = llgs[i].distance

from scipy import interpolate

f = interpolate.interp2d(lnr, ltr, Z, kind='cubic')

f(home[1], home[0])
