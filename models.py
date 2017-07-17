from models2 import db

class MLSListing(db.Model):
    __tablename__ = 'mls'

    mls = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    living_area = db.Column(db.String)
    n_beds = db.Column(db.String)
    n_baths = db.Column(db.String)
    total_rooms = db.Column(db.String)
    lat = db.Column(db.String)
    lng = db.Column(db.String)
    distance = db.Column(db.String)
    station = db.Column(db.String)

    def __repr__(self):
        return '<MLS %r: %s>' % (self.mls, self.address)
