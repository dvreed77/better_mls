from celery import group

from mls_scraper.query import QUERY
from mls_scraper.settings import MLS_URLS, AID_KEY
from mls_scraper.workers import *
from mls_scraper import celery

params = get_params(AID_KEY, QUERY)

@celery.task(name='mls_scraper.scrape_all_listings_task')
def scrape_all_listings_task():
    n_pages = get_n_pages(MLS_URLS['results_url'], params)
    group(scrape_listings_task.s(pn) for pn in range(1, n_pages+1))()

@celery.task(name='mls_scraper.scrape_listings_task')
def scrape_listings_task(pn):
    listings = scrape_listing_page(MLS_URLS['results_url'], params, pn)
    process_listings_task.delay(listings)
    process_prices_task.delay(listings)

@celery.task(name='mls_scraper.process_listings_task')
def process_listings_task(listings):
    processed = 0
    for l in filter(lambda x: not listing_exists(x['mls']), listings):
        listing = get_page_info(MLS_URLS['details_url'],mls=l['mls'], aid=AID_KEY)
        listing["mls"] = l['mls']
        added = save_listing(listing)
        if added:
            processed += 1

    db.session.commit()

    print("Received %i listings. Added %i" % (len(listings), processed))

@celery.task(name='mls_scraper.process_prices_task')
def process_prices_task(listings):
    processed = 0
    for l in listings:
        added = save_price(l)
        if added:
            processed += 1

    db.session.commit()

    print("Received %i prices. Added %i" % (len(listings), processed))
