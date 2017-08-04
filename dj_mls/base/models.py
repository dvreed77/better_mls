from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField


class MLSListing(models.Model):
    mls = models.IntegerField(primary_key=True)
    address = models.TextField()
    living_area = models.FloatField()
    n_beds = models.FloatField()
    n_baths = models.FloatField()
    total_rooms = models.FloatField()
    created = models.DateTimeField()
    lat = models.FloatField()
    lng = models.FloatField()

    price = JSONField()

    walking_duration = models.FloatField()
    transit_duration = models.FloatField()

    class Meta:
        managed = False
        db_table = 'feature_view'

    def __repr__(self):
        return '<MLS %r: %s>' % (self.mls, self.address)


class MLSPrice(models.Model):
    # mls = models.IntegerField()
    mls = models.ForeignKey(
    MLSListing,
    db_column='mls',
    on_delete=models.DO_NOTHING,
    related_name='prices'
    )
    status = models.CharField(max_length=20)
    price = models.IntegerField()
    datetime = models.DateTimeField()


    class Meta:
        managed = False
        db_table = 'mls_price'

    def __repr__(self):
        return '<MLSPrice %r: %s>' % (self.mls, self.price)
