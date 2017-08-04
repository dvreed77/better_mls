import requests
from mls_scraper.settings import GOOGLE_KEY
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from mls_scraper.models import MLSListingFeature, MLSListing
from mls_scraper import db
from scipy import interpolate
from mls_scraper.analysis import get_distance_duration, get_ll

%matplotlib inline

copley = [42.3502089,-71.0768681]
home = [42.3369546,-71.0751955]

a = MLSListing.query.join(MLSListingFeature).filter()
a.feature

db.session.rollback()

n = MLSListing.query.outerjoin(
    (MLSListingFeature, MLSListing.mls == MLSListingFeature.mls)
).filter(
    MLSListingFeature.transit_distance == None
).first()

n.feature.transit_distance




# Create All Models
db.create_all()

mls_listings = MLSListing.query.all()
get_ll(mls_listings[0].address)

for mls_listing in mls_listings:
    d = get_ll(mls_listing.address)
    mls_listing.lat = d['lat']
    mls_listing.lng = d['lng']
db.session.commit()

# Setup bounds
e = 42.3379544,-70.9878652
w = 42.3264574,-71.1767246
n = 42.3827608,-71.1050284
s = 42.2916585,-71.0993726
bounds = [w[1],e[1],s[0],n[0]]

create_grid(label='grid_10', bounds=bounds, n_points=10)
create_grid(label='grid_100', bounds=bounds, n_points=100)

fill_grid('grid_10', copley, 'walking')
fill_grid('grid_100', copley, 'walking')

x,y,Z = get_grid('grid_10', 'walking', 'duration')

X, Y = np.meshgrid(x, y)

plt.figure()
CS = plt.contour(X, Y, Z, 20)
plt.clabel(CS, inline=1, fontsize=10)

copley = [42.3502089,-71.0768681]
mls_listings = MLSListing.query.all()
mode = 'transit'
for mls_listing in mls_listings:

    distance, duration = get_distance_duration([mls_listing.lat, mls_listing.lng], copley, mode)
    if distance == None:
        print("Error, exited filling grid")
        break
    if mode == 'walking':
        mlsf = MLSListingFeature(
        mls=mls_listing.mls,
        walking_distance = distance,
        walking_duration = duration
        )

    else:
        mlsf = MLSListingFeature(
        mls=mls_listing.mls,
        transit_distance = distance,
        transit_duration = duration
        )
    db.session.merge(mlsf)

db.session.commit()
# determine thresholds
# 0     = Very Good
# 0.25  = Good
# 0.5   = Could if you had to
# 0.75  = Won't do it
# 1.0   = Not in a million years

{}

42.3369546,-71.0751955

scores = [
{
    'score': 0,
    'address': 'marlborough and fairfield',
    'lat_lng': (42.3513729,-71.0827601)
},
{
    'score': 0.25,
    'address': 'home',
    'lat_lng': (42.3369362,-71.0751953)
},
{
    'score': 0.5,
    'address': 'andrew_square',
    'lat_lng': (42.3298499,-71.0574433)
},
{
    'score': 0.75,
    'address': 'edge of south boston',
    'lat_lng': (42.3360805,-71.0259475)
},
{
    'score': 1,
    'address': 'dorchester',
    'lat_lng': (42.2907913,-71.0744908)
}
]



# Interpolate Point
f = interpolate.interp2d(x, y, Z, kind='cubic')

f(scores[0]['lat_lng'][1], scores[0]['lat_lng'][0])/60

f(scores[1]['lat_lng'][1], scores[1]['lat_lng'][0])/60

f(scores[2]['lat_lng'][1], scores[2]['lat_lng'][0])/60

f(scores[3]['lat_lng'][1], scores[3]['lat_lng'][0])/60

f(scores[4]['lat_lng'][1], scores[4]['lat_lng'][0])/60
