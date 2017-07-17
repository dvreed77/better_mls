from utils import *
import settings
from query import QUERY
import requests
import lxml.html

QUERY


settings.SQLALCHEMY_DATABASE_URI

url = 'http://vow.mlspin.com/idx/rslts.aspx?aid=BB805183&id=13818&twn=ANDO%2C&type=SF&min=0&max=99999999&beds=1&baths=1&gla=&lot='

r = requests.get(url)
html = lxml.html.fromstring(r.text)

class MLSQuery(object):
    """docstring for MLSQuery."""
    def __init__(self, arg):
        super(MLSQuery, self).__init__()
        self.arg = arg




def scrape_listing_page(mobj):
    def get_info(prop):
        try:
            out = {
                "mls": int(prop[0].xpath('td[4]/a/text()')[0]),
                "status": prop[0].xpath('td[6]/text()')[0].strip(),
                "price": prop[0].xpath('td[8]/text()')[0].strip(),
                "street": prop[1].xpath('td[1]/text()')[0],
                "city": prop[2].xpath('td[1]/text()')[0]
            }
            return out
        except:
            return {}

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



def create_query_string(query=QUERY):


def get_main_page(mls_url=None):


    return r

def get_page_info(self, mls):
    base_url = 'http://vow.mlspin.com/idx/details.aspx'
    params = {
        'mls': mls,
        'aid': AID_KEY
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
