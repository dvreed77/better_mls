import requests
import numpy as np

from mls_scraper.models import LatLngEntry, LatLngGrid
from mls_scraper.settings import GOOGLE_KEY
from mls_scraper import db

NULL_VALUE = 99999.
def get_distance_duration(origin, destination, mode='walking'):
    url = 'https://maps.googleapis.com/maps/api/directions/json'

    params = {
        'origin': '%f,%f' % (origin[0], origin[1]),
        'destination': '%f,%f' % (destination[0], destination[1]),
        'key': GOOGLE_KEY,
        'mode': 'transit'
    }

    r = requests.get(url, params)
    out = r.json()

    if out['status'] == 'ZERO_RESULTS':
        distance = NULL_VALUE
        duration = NULL_VALUE
    else:
        try:
            distance = out['routes'][0]['legs'][0]['distance']['value']
            duration = out['routes'][0]['legs'][0]['duration']['value']
        except:
            print(out)
            distance = None
            duration = None

    return distance, duration


def get_grid(label, mode, metric):
    llg = LatLngGrid.query.get(label)

    lles = LatLngEntry.query.filter(
        LatLngEntry.label==label
    ).order_by(LatLngEntry.idx).all()


    lnr = [x.lng for x in lles[:llg.n_points]]
    ltr = [x.lat for x in lles[::llg.n_points]]

    Z = np.empty((llg.n_points, llg.n_points))
    for i in range(len(lles)):
        Z[int(i/llg.n_points), int(i%llg.n_points)] = lles[i].__dict__['%s_%s'%(mode, metric)]

    m = np.median(Z[Z != NULL_VALUE])
    # Assign the median to the zero elements
    Z[Z == NULL_VALUE] = m

    return lnr, ltr, Z


def create_grid(label, bounds, n_points):

    llg = LatLngGrid(
        label=label,
        n_points=n_points,
        bounds=bounds
    )

    db.session.add(llg)

    lng_bounds = bounds[:2]
    lat_bounds = bounds[2:]
    dlng = np.abs(lng_bounds[1] - lng_bounds[0]) / n_points
    dlat = np.abs(lat_bounds[1] - lat_bounds[0]) / n_points

    lnr = np.arange(min(lng_bounds), max(lng_bounds), dlng)[:n_points]
    ltr = np.arange(min(lat_bounds), max(lat_bounds), dlat)[:n_points]

    for idx in range(n_points * n_points):
        iy = int(idx / n_points)
        ix = int(idx % n_points)

        lle = LatLngEntry(
            idx=idx,
            lat=ltr[iy],
            lng=lnr[ix],
            label=label
        )
        db.session.add(lle)
    db.session.commit()


def fill_grid(label, destination, mode):
    if mode == 'walking':
        lles = LatLngEntry.query.filter(
            LatLngEntry.label==label,
            LatLngEntry.walking_distance == None
        ).all()
    else:
        lles = LatLngEntry.query.filter(
            LatLngEntry.label==label,
            LatLngEntry.transit_distance == None
        ).all()

    for lle in lles:
        try:
            distance, duration = get_distance_duration([lle.lat, lle.lng], destination, mode)
            if distance == None:
                print("Error, exited filling grid")
                break
            if mode == 'walking':
                lle.walking_distance = distance
                lle.walking_duration = duration
            else:
                lle.transit_distance = distance
                lle.transit_duration = duration

        except Exception as e:
            print("Error, exited filling grid", e)
            break

    db.session.commit()


def get_ll(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': address,
        'key': GOOGLE_KEY
    }

    r = requests.get(url, params=params)
    results = r.json()

    try:
        return results['results'][0]['geometry']['location']
    except:
        return {'lat': np.nan, 'lng': np.nan}
