import requests
import json
from pprint import pprint
from datetime import datetime, timedelta


def get_ticket():
    date = datetime.now()
    i = 0

    """ Makes use of Send API:
        https://developers.facebook.com/docs/messenger-platform/send-api-reference
    """
    while i < 30:
        f = open("data/data.txt", "a")
        i += 1
        date = date + timedelta(days=i)
        d = date.day
        m = date.month
        headers = {
            'content-type': 'application/json',
            'x-domain': 'flight',
            'cookie': '__cfduid=dce64cb0793a44f109f0e21d7cd19423d1558775359; _ga=GA1.2.87763926.1558775363; mp_648ea2fd71786d0051f45d9b9f13e756_mixpanel=%7B%22distinct_id%22%3A%20%2216aee4076b8313-07b437cf87314d-37647e03-232800-16aee4076b97bf%22%2C%22%24device_id%22%3A%20%2216aee4076b8313-07b437cf87314d-37647e03-232800-16aee4076b97bf%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D; cto_lwid=94fafdb1-4616-4854-81f5-270d07bf4ef5; _fbp=fb.1.1558775363544.2119175748; __flash={}; _gid=GA1.2.905737942.1559811402; lux_uid=155981140173998881; G_ENABLED_IDPS=google; tv-pnheader=1; tv-repeat-visit=true; tv-groupint=1; ajs_user_id=null; ajs_group_id=null; _gcl_au=1.1.548988354.1559811404; ajs_anonymous_id=%2257e60d33-57ec-4f04-92a6-f19ff0613667%22; __ssid=17e15f93c852d940c287b3a2d8c42a6; flightFlightType=ONE_WAY; flightNumOfAdults=1; flightNumChildren=0; flightNumInfants=0; flightSeatClassType=ECONOMY; flexibility=0; selectedLocale=vi_VN; tvCurrencyPrev=IDR; selectedCurrency=VND; _gat_UA-29776811-1=1; flightDepartureDate=20-6-2019; flightSourceAirport=DAD; flightDestinationAirport=SGN; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; tvs=aHiviipoLebGMEC5qT/rF2AASlrq0ThlTbE/jXVznJHbrA7GVHn/ftBaRvpFvWlhionMEHH6N5vSlHNgG0Qz0y4xZW9DATz5nZ74tCk3iQCFaPkdLGbRkqJFuV0RPWFqbY95iDWxCvaH/AgGMjI9DRcIQrJFnRdMHDaWLO1gEMVgkPtbOBKVLM8yxFYEDO4m3jW7f6f85zK7XA1xLrLbn3wpMY91AYFzJ6h8za/vSrnqDlY26eY/bwMK2Y7r9t1q; datadome=0W6jKQQH~4.OJ6TAe.dadX9cUXZfrEMXxZkMILNtztc; tvl=tD4M8lSFLbSk6p2nM9uegdffBJvvr797uULve6zQaW4HUhJKz+1BoXpjQ8ko3dXyrTdL1YS7qDoDx0tmaF8sqP6Y793srZ9QM4Avg2gKav2VM3NZGniuO+nqrMZ4iENdgYCdgBDk5mVbeBm48MivZuA0O7aHmuQCLHYhHjH1iJ7Sn0KvpAAf36wqmzcSinHUyjDKZfnBFQySog//2+De74yE87wO4wrv6Ckzkq+aFp2iAFSBkESSumIKzae1rc17'
        }
        payload = {
            'clientInterface': 'desktop',
            'data':
            {
                'currency': 'VND',
                'destinationAirportOrArea': "SGN",
                'flightDate': {'day': d, 'month': m, 'year': "2019"},
                'locale': 'en_VN',
                'newResult': True,
                'numSeats': {
                    'numAdults': '1',
                    'numChildren': '0',
                    'numInfants': '0',
                },
                'seatPublishedClass': 'ECONOMY',
                'seqNo': None,
                'sortFilter': {
                    'filterAirlines': [],
                    'filterArrive': [],
                    'filterDepart': [],
                    'filterTransit': [],
                    'selectedDeparture': '',
                    'sort': None,
                },
                'sourceAirportOrArea': "DAD",
                'searchId': None,
                'usePromoFinder': False,
                'useDateFlow': False,
            },
            'fields': [],
        }
        url = 'https://www.traveloka.com/api/v2/flight/search/oneway'
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        datas = response.json()['data']['searchResults']
        print(len(datas))
        for data in datas:
            price = data['agentFareInfo']['totalSearchFare']['amount']
            arrivalTime = data["connectingFlightRoutes"][0]['segments'][0]['arrivalTime']
            arrivalDate = data["connectingFlightRoutes"][0]['segments'][0]['arrivalDate']
            flightNumber = data["connectingFlightRoutes"][0]['segments'][0]['flightNumber']
            d = "{},{}-{}-{} {}:{}:00,{}".format(price, arrivalDate['day'], arrivalDate['month'], arrivalDate['year'],
                                                 arrivalTime['hour'], arrivalTime['minute'], flightNumber)
            f.write(d + "\n")
        f.close()
    return


if __name__ == '__main__':
    get_ticket()
