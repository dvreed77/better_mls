import requests
import lxml.html
import re
import time
import datetime
from math import ceil
from sqlalchemy import desc

from mls_scraper.models import MLSListing, MLSPrice
from mls_scraper import db


def get_params(aid, query):
    params = {
        "aid": aid,
        "twn": query["towns"],
        "type": query["types"],
        "min": query["price"][0],
        "max": query["price"][1]
    }
    return params


def get_n_pages(base_url, params):
    r = requests.get(base_url, params=params)

    html = lxml.html.fromstring(r.text)
    A = html.xpath('//td[@class="ResultsRow"]/text()')
    grps = re.match(
        'Records (\d+) through (\d+) of (\d+)', A[0]).groups()
    n_records = int(grps[2])
    n_pages = int(ceil(n_records / 50.))

    return n_pages


def scrape_listing_page(base_url, params, pn=1):
    def get_info(prop):
        try:
            out = {
                "mls": int(prop[0].xpath('td[4]/a/text()')[0]),
                "status": prop[0].xpath('td[6]/text()')[0].strip(),
                "price": int(prop[0].xpath('td[8]/text()')[0].strip().replace('$', '').replace(',', '')),
                "street": prop[1].xpath('td[1]/text()')[0],
                "city": prop[2].xpath('td[1]/text()')[0]
            }
            return out
        except:
            return {}

    params['currentpage'] = pn
    r = requests.get(base_url, params=params)

    html = lxml.html.fromstring(r.text)
    allR = html.xpath('//tr[@class="ResultsRow"]')
    out = []
    for idx in range(0, len(allR), 4):
        out.append(get_info(allR[idx:idx + 4]))

    print('done with page %i (%i)' % (pn, len(out)))

    return out


def get_page_info(base_url, mls, aid):
    def get_feature(html, f):
        for idx, a in enumerate(html.xpath('//td[@class="Details"]')):
            if not len(a.xpath('b/text()')):
                continue
            if f in a.xpath('b/text()')[0]:
                t = ''.join(a.xpath('text()'))
                return t.strip(' \r\n\t:')

    params = {
        'mls': mls,
        'aid': aid
    }
    r = requests.get(base_url, params=params)
    html = lxml.html.fromstring(r.text)
    try:
        A = html.xpath(
            '//td[@class="Details"]/b/text()')
        A = A[0].strip(' \r\n\t').replace(u'\xa0', u' ')
        tmp = re.match(
            "MLS # (\d+)[\r\n\t ]+(\w[#A-Za-z0-9-',. ]+[a-zA-Z])$", A)

        price = get_feature(html, 'List Price')
        total_rooms = get_feature(html, 'Total Rooms')
        beds_baths = get_feature(html, 'Beds/Baths')
        living_area = get_feature(html, 'Living Area')

        try:
            n_beds = beds_baths.split('/')[0]
            n_baths = beds_baths.split('/')[1]
        except:
            n_beds = None
            n_baths = None

        out = {
            'address': tmp.groups()[1],
            'price': float(price.replace('$', '').replace(',', '')),
            'total_rooms': float(total_rooms),
            'n_beds': float(n_beds),
            'n_baths': float(n_baths),
            'living_area': float(re.match('(\d+)sqft', living_area).groups()[0])
        }
        return out
    except Exception as e:
        msg = 'Error with MLS: %s (%s)' % (mls, e)
        print(msg)
        # logger.error('Error with MLS: %s (%s)' % (mls, e))
        out = {
            'address': None,
            'price': None,
            'total_rooms': None,
            'n_beds': None,
            'n_baths': None,
            'living_area': None
        }
        return out

def listing_exists(mls):
    mls_listing = MLSListing.query.get(mls)
    if mls_listing:
        return True
    else:
        return False


def save_price(listing):
    mls_price = MLSPrice.query.filter(
        MLSPrice.mls == listing['mls']
    ).order_by(desc(MLSPrice.datetime)).first()

    if (mls_price is None) or (mls_price.price!=listing['price']) or (mls_price.status!=listing['status']):
        mls_price = MLSPrice(
        mls=listing['mls'],
        price=listing['price'],
        status=listing['status'],
        datetime=datetime.datetime.now()
        )
        db.session.add(mls_price)
        return True

    return False


def process_listing(mls):
    listing = get_page_info('http://vow.mlspin.com/idx/details.aspx', mls=mls, aid=AID_KEY)
    listing["mls"] = mls
    return save_listing(listing)


def process_price(listing):
    return save_price(listing)

def save_listing(listing):

    mls_listing = MLSListing.query.get(listing['mls'])

    if mls_listing is None:
        mls_listing = MLSListing(
            mls=listing['mls'],
            address=listing['address'],
            living_area=listing['living_area'],
            n_beds=listing['n_beds'],
            n_baths=listing['n_baths'],
            total_rooms=listing['total_rooms'],
            created=datetime.datetime.now()
        )

        db.session.add(mls_listing)
        return True
    return False
