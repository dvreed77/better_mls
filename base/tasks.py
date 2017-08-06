# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task, group
from django.conf import settings
from .workers import *


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

params = get_params(settings.AID_KEY, settings.QUERY)

@shared_task
def scrape_all_listings_task():
    n_pages = get_n_pages(settings.MLS_URLS['results_url'], params)
    group(scrape_listings_task.s(pn) for pn in range(1, n_pages+1))()

@shared_task
def scrape_listings_task(pn):
    listings = scrape_listing_page(settings.MLS_URLS['results_url'], params, pn)
    process_listings_task.delay(listings)
    process_prices_task.delay(listings)

@shared_task
def process_listings_task(listings):
    processed = 0
    for l in filter(lambda x: not listing_exists(x['mls']), listings):
        listing = get_page_info(settings.MLS_URLS['details_url'],mls=l['mls'], aid=settings.AID_KEY)
        listing["mls"] = l['mls']
        added = save_listing(listing)
        if added:
            processed += 1

    # db.session.commit()

    print("Received %i listings. Added %i" % (len(listings), processed))

@shared_task
def process_prices_task(listings):
    processed = 0
    for l in listings:
        added = save_price(l)
        if added:
            processed += 1

    # db.session.commit()

    print("Received %i prices. Added %i" % (len(listings), processed))
