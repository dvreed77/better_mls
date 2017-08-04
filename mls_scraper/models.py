from mls_scraper import db

class MLSListing(db.Model):
    __tablename__ = 'mls'

    mls = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    living_area = db.Column(db.Float)
    n_beds = db.Column(db.Float)
    n_baths = db.Column(db.Float)
    total_rooms = db.Column(db.Float)
    created = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __repr__(self):
        return '<MLS %r: %s>' % (self.mls, self.address)


class MLSListingFeature(db.Model):
    __tablename__ = 'mls_feature'

    mls = db.Column(db.Integer, primary_key=True)
    walking_distance = db.Column(db.Float)
    walking_duration = db.Column(db.Float)
    transit_distance = db.Column(db.Float)
    transit_duration = db.Column(db.Float)

    def __repr__(self):
        return '<MLS Feature %r>' % (self.mls)


class MLSPrice(db.Model):
    __tablename__ = 'mls_price'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mls = db.Column(db.Integer)
    status = db.Column(db.String)
    price = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)


    def __repr__(self):
        return '<MLS %s: %s>' % (self.mls, self.price)


class LatLngGrid(db.Model):
    __tablename__ = 'lat_lng_grid'

    label = db.Column(db.String, primary_key=True)
    n_points = db.Column(db.Integer)
    bounds = db.Column(db.ARRAY(db.Float))


class LatLngEntry(db.Model):
    __tablename__ = 'lat_lng_entry'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idx = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    walking_distance = db.Column(db.Float)
    walking_duration = db.Column(db.Float)
    transit_distance = db.Column(db.Float)
    transit_duration = db.Column(db.Float)
    label = db.Column(db.String)
