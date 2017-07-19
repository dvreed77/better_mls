import requests
import pandas as pd
import numpy as np
import lxml.html
from sqlalchemy import create_engine
import time
import datetime
import re
import logging
from logging.config import dictConfig



engine = create_engine('sqlite:///%smbta_stations.db' % ROOT_DIR)
mbtadf2 = pd.read_sql_table('mbta_stations', engine,)
pts = list(mbtadf2.apply(lambda x: (x.latitude, x.longitude), axis=1).values)
pts = np.array(pts)




def get_ll(row):
    time.sleep(0.1)
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': row['address'],
        'key': GOOGLE_KEY
    }

    r = requests.get(url, params=params)
    results = r.json()

    try:
        return pd.Series(results['results'][0]['geometry']['location'])
    except:
        return pd.Series({'lat': np.nan, 'lng': np.nan})


def get_feature(html, f):
    for idx, a in enumerate(html.xpath('//td[@class="Details"]')):
        if not len(a.xpath('b/text()')):
            continue
        if f in a.xpath('b/text()')[0]:
            t = ''.join(a.xpath('text()'))
            return t.strip(' \r\n\t:')


def get_ll(row):
    time.sleep(0.1)
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': row['address'],
        'key': GOOGLE_KEY
    }

    r = requests.get(url, params=params)
    results = r.json()

    try:
        return pd.Series(results['results'][0]['geometry']['location'])
    except:
        return pd.Series({'lat': np.nan, 'lng': np.nan})


def get_feature(html, f):
    for idx, a in enumerate(html.xpath('//td[@class="Details"]')):
        if not len(a.xpath('b/text()')):
            continue
        if f in a.xpath('b/text()')[0]:
            t = ''.join(a.xpath('text()'))
            return t.strip(' \r\n\t:')


class MLS(object):
    """docstring for ClassName"""

    def __init__(self):
        super(MLS, self).__init__()
        self.base_url = "http://vow.mlspin.com/idx/rslts.aspx"
        self.df = pd.DataFrame()
        self.main_table = 'mls'
        self.status_table = 'status'
        self.temp_table = 'temp'
        self.db_url = 'sqlite:///%smls_listings.db' % ROOT_DIR
        self.query_table = 'queries'

    def add_new(self, query_name):
        """
        Scrape MLS listing page.
        3 cases:
        * New MLS listing, get info like address, etc from page
        * Old MLS listing, new status
        * MLS in old table, not in new table. MLS is off-market
        """
        self.scrape_all_main_pages(query_name)

        engine = create_engine(self.db_url)

        query = """
        SELECT
            mls
        FROM %s
        EXCEPT
        SELECT
            mls
        FROM %s
        """ % (self.temp_table, self.main_table)

        # contains all MLS listing we don't already have
        df = pd.read_sql_query(query, engine)

        logger.info("Added %i new entries" % len(df))

        if len(df):
            df2 = df.mls.apply(self.get_page_info)

            df = pd.merge(df, df2, left_index=True, right_index=True)
            df['date_collected'] = datetime.datetime.now()

            df = self.get_ll(df)
            df = self.get_stations(df)

            cols_mls = [
                'mls',
                'address',
                'living_area',
                'n_beds',
                'n_baths',
                'total_rooms',
                'lat',
                'lng',
                'distance',
                'station'
            ]

            df_mls = df[cols_mls]
            df_mls.to_sql(
                self.main_table, engine, index=False, if_exists="append")

        cols_status = [
            'mls',
            'status',
            'price'
        ]

        df_status = pd.read_sql_table(self.temp_table, engine)
        df_status = df_status[cols_status]
        df_status['date_collected'] = datetime.datetime.now()
        df_status.to_sql(
            self.status_table, engine, index=False, if_exists="append")

        self.set_off_market()

    def set_off_market(self):
        query = """
        SELECT
            a.mls
        FROM {status} a
        WHERE a.date_collected = (
            SELECT MAX(date_collected)
            FROM {status} WHERE a.mls={status}.mls
        ) AND a.status IS NOT 'OM'

        EXCEPT

        SELECT
            mls
        FROM {temp}
        """.format(status=self.status_table, temp=self.temp_table)

        engine = create_engine(self.db_url)
        df = pd.read_sql_query(query, engine)

        logger.info("Set %i records to 'Off-Market'" % len(df))
        df['status'] = 'OM'
        df['price'] = ''
        df['date_collected'] = datetime.datetime.now()
        df.to_sql(self.status_table, engine, index=False, if_exists='append')

    def drop_main_table(self):
        engine = create_engine(self.db_url)
        engine.execute('DROP TABLE %s;' % self.main_table)

    def get_all_save(self):
        self.get_all()
        self.get_ll()
        self.save()

    def save(self):
        engine = create_engine(self.db_url)
        self.df.to_sql('mls_listing', engine, index=False, if_exists="append")

    def load(self):
        engine = create_engine(self.db_url)
        self.df = pd.read_sql_table('mls_listing', engine)

    def get_ll(self, df):
        df[['lat', 'lng']] = df.apply(get_ll, axis=1)
        return df

    def split_street(self):
        def tmp(r):
            t = r.street.split(' - ')
            street = t[0]
            try:
                unit = t[1]
            except:
                unit = ''
            return pd.Series({'street2': street, 'unit': unit})
        self.df[['street', 'unit']] = mls.df.apply(tmp, axis=1)

    def get_n_pages(self, query):
        r = requests.get(
            self.base_url,
            params=query)

        html = lxml.html.fromstring(r.text)
        A = html.xpath('//td[@class="ResultsRow"]/text()')
        grps = re.match('Records (\d+) through (\d+) of (\d+)', A[0]).groups()
        n_records = int(grps[2])
        n_pages = int(np.ceil(n_records / 50.))
        return n_pages

    def set_query(self, key, query):
        for k, v in query.iteritems():
            if type(v) is list:
                query[k] = ','.join(v)

        df = pd.DataFrame([query], index=[key])
        engine = create_engine(self.db_url)
        df.to_sql(self.query_table, engine, index=True, if_exists='append')

    def get_query(self, key):
        engine = create_engine(self.db_url)
        query = """
        SELECT * FROM %s
        WHERE "index"='%s';
        """ % (self.query_table, key)
        df = pd.read_sql_query(query, engine)
        df.set_index('index', inplace=True)

        query = df.ix[0].to_dict()
        for k, v in query.iteritems():
            tmp = v.split(',')
            if len(tmp) > 1:
                query[k] = tmp
            else:
                query[k] = v

        return query

    def get_page_info(self, mls):
        base_url = 'http://vow.mlspin.com/idx/details.aspx'
        params = {
            'mls': mls,
            'aid': 'BB805183'
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
                n_beds = np.nan
                n_baths = np.nan

            out = {
                'address': tmp.groups()[1],
                'price': price,
                'total_rooms': total_rooms,
                'n_beds': n_beds,
                'n_baths': n_baths,
                'living_area': living_area
            }
            time.sleep(np.random.uniform(0.2, 2))
            return pd.Series(out)
        except Exception, e:
            logger.error('Error with MLS: %s (%s)' % (mls, e))
            out = {
                'address': np.nan,
                'price': np.nan,
                'total_rooms': np.nan,
                'n_beds': np.nan,
                'n_baths': np.nan,
                'living_area': np.nan
            }
            return pd.Series(out)

    def get_stations(self, df):
        def get_closest_stop(r, n_stops=1):
            pt = np.array((r.lat, r.lng))
            dx = (pts[:, 0] - pt[0])**2
            dy = (pts[:, 1] - pt[1])**2
            dd = np.sqrt(dx + dy)
            sidx = np.argsort(dd)

            out = {
                'station': mbtadf2.ix[sidx[0]].title,
                'distance': dd[sidx[0]]
            }
            return pd.Series(out)
        df[['distance', 'station']] = df.apply(get_closest_stop, axis=1)
        return df

    def get_info(self, prop):
        out = {
            "mls": int(prop[0].xpath('td[4]/a/text()')[0]),
            "status": prop[0].xpath('td[6]/text()')[0].strip(),
            "price": prop[0].xpath('td[8]/text()')[0].strip(),
            "street": prop[1].xpath('td[1]/text()')[0],
            "city": prop[2].xpath('td[1]/text()')[0]
        }
        return out

    def scrape_all_main_pages(self, query_name):
        query = self.get_query(query_name)
        tmpdf = pd.DataFrame()
        for pn in range(1, self.get_n_pages(query) + 1):
            df = self.scrape_main_page(pn, query)
            tmpdf = pd.concat([tmpdf, df], ignore_index=True)

        engine = create_engine(self.db_url)
        tmpdf.to_sql(self.temp_table, engine, index=False, if_exists="replace")
        return tmpdf

    def scrape_main_page(self, pn, query):
        time.sleep(np.random.uniform(0.2, 2))
        params = query
        params['currentpage'] = str(pn)
        r = requests.get(
            self.base_url,
            params=params)

        P1 = r.text
        html = lxml.html.fromstring(P1)
        allR = html.xpath('//tr[@class="ResultsRow"]')
        out = []
        for idx in range(0, len(allR), 4):
            out.append(self.get_info(allR[idx:idx + 4]))

        return pd.DataFrame(out)


def get_mbta_stations():
    url = 'http://erikdemaine.org/maps/mbta/mbta.js'
    r = requests.get(url)
    results = r.text

    def get_node(r):
        groups = re.match(
            'root\[(\d+)\]\.stations\[(\d+)\]\.(\w+) = (.+)', r).groups()
        return '%s-%s' % (groups[0], groups[1]), groups[2], groups[3]

    out = []
    for r in results.split('\n'):
        try:
            out.append(get_node(r))
        except:
            pass

    mbtadf = pd.DataFrame(out, columns=['station', 'key', 'value'])
    mbtadf.head(20)

    mbtadf2 = mbtadf.pivot(index='station', columns='key', values='value')
    mbtadf2.latitude = mbtadf2.latitude.apply(lambda x: float(x.strip(';')))
    mbtadf2.longitude = mbtadf2.longitude .apply(lambda x: float(x.strip(';')))
    mbtadf2.dropna(inplace=True)

    pts = list(
        mbtadf2.apply(lambda x: (x.latitude, x.longitude), axis=1).values)
    pts = np.array(pts)

    mbtadf2.title = mbtadf2.title.apply(lambda x: x.strip("';"))
    engine = create_engine(
        'sqlite:///mbta_stations.db')

    mbtadf2.to_sql('mbta_stations', engine, index=False, if_exists="replace")


if __name__ == '__main__':
    mls = MLS()
    mls.add_new('q1')
