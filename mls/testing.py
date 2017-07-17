from mls.query import QUERY
from mls.settings import BASE_URL, AID_KEY
from mls.workers import *
from mls import db

params = get_params(AID_KEY, QUERY)
params

listings = scrape_listing_page(BASE_URL, params)
listings

a = get_page_info('http://vow.mlspin.com/idx/details.aspx',mls=listings[0]['mls'], aid=AID_KEY)
a


for l in listings:
    listing = get_page_info('http://vow.mlspin.com/idx/details.aspx',mls=l['mls'], aid=AID_KEY)
    listing["mls"] = l['mls']
    save_listing(listing)

db.session.commit()

db.create_all()



mobj = MLSQuery(QUERY, AID_KEY)
# mobj.get_n_pages()

out = mobj.scrape_listing_page()

for _ in range(10):
    print(len(mobj.results))
    time.sleep(.2)
