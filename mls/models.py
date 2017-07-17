from mls import db

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
