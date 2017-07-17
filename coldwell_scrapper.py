import requests
import lxml.html

mls = 72197941


def get_history(mls):

    url = 'https://www.coldwellbankerhomes.com/new-england/mls_%i/all/' % mls

    r = requests.get(url)



    url = r.url
    url

    html = lxml.html.fromstring(r.text)
    e = html.xpath('.//h3[contains(text(),"Property History")]/following-sibling::ul/li')

    history = [x.text_content() for x in e[1:]]
    return history

mls = [
71922826,
71944844,
71921781,
71946126,
71950530,
71851659
]

out = []
for m in mls:
    h = get_history(m)
    out.append((m, h))

get_history(71922826)
out




name = "1 Greenwich Ct - Unit 1	Boston, MA : South End 02120-2203"

url = "https://www.zillow.com/homes/%s" % (name)

r = requests.get(url)

r.status_code
r.url

html = lxml.html.fromstring(r.text)

html
