from mls_scraper.query import QUERY
from mls_scraper.settings import BASE_URL, AID_KEY
from mls_scraper.workers import *
from mls_scraper import db
from mls_scraper import tasks as t

params = get_params(AID_KEY, QUERY)
params

t.scrape_listings_task(1)
n_pages = get_n_pages(BASE_URL, params)
n_pages

listings = scrape_listing_page(BASE_URL, params, 1)
listings

processed = 0
for l in filter(lambda x: not listing_exists(x['mls']), listings):
    listing = get_page_info('http://vow.mlspin.com/idx/details.aspx',mls=l['mls'], aid=AID_KEY)
    listing["mls"] = l['mls']
    added = save_listing(listing)
    if added:
        processed += 1

print("Received %i listings. Added %i" % (len(listings), processed))

processed = 0
for l in listings:
    added = save_price(l)
    if added:
        processed += 1

print("Received %i prices. Added %i" % (len(listings), processed))

db.session.commit()




db.create_all()



mobj = MLSQuery(QUERY, AID_KEY)
# mobj.get_n_pages()

out = mobj.scrape_listing_page()

for _ in range(10):
    print(len(mobj.results))
    time.sleep(.2)
