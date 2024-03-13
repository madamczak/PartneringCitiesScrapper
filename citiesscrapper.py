import requests
from bs4 import BeautifulSoup
import json


def get_soup(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, features="html.parser")
    return soup


def get_geo_dms_coords(link):
    soup = get_soup(link)
    geo_dms = soup.findAll('span', {'class': 'geo-dms'})

    if len(geo_dms) > 2:
        lat, lon = geo_dms[1].text.replace('\xa0', " ").replace(",", ".").split(" ")
        return float(lat), float(lon)

    return 0.0, 0.0


def get_nominatim_coords(city_name):
    searchlink = f"https://nominatim.openstreetmap.org/search?q={city_name}+Polska&format=json&addressdetails=1&limit=1"
    nominatim_respone = requests.get(searchlink)
    city_list = json.loads(nominatim_respone.text)
    city_dictionary = city_list[0]
    return float(city_dictionary.get("lat")), float(city_dictionary.get('lon'))


def get_partnering_cities_locations_with_nominatim(wiki_link):
    cities_dictionary = {}
    soup = get_soup(wiki_link)
    all_h2 = soup.findAll("h2")[1:]

    for h2 in all_h2:
        city_name = h2.text.replace("[edytuj | edytuj kod]", "")
        lat, lon = get_nominatim_coords(city_name)
        cities_dictionary.update({city_name: (lat, lon)})

    return cities_dictionary


def get_partnering_cities_locations_with_geo_dms(wiki_link):
    soup = get_soup(wiki_link)
    all_h2 = soup.findAll("h2")[1:]

    another_cities_dictionary = {}

    for h2 in all_h2:
        all_a_tags = h2.findAll('a')
        city_a_tag = all_a_tags[0]
        city_name = city_a_tag.text
        city_href = city_a_tag['href']
        city_link = f'https://pl.wikipedia.org{city_href}'
        lat, lon = get_geo_dms_coords(city_link)

        another_cities_dictionary.update({city_name: (lat, lon)})

    return another_cities_dictionary


def get_cities_with_partnering_cities(wiki_link):
    soup = get_soup(wiki_link)

    all_h2 = soup.findAll("h2")[1:]
    all_tables = soup.findAll("table")

    cities_with_parnering_cities = {}

    for table, h2 in zip(all_tables, all_h2):
        main_city_name = h2.text.replace("[edytuj | edytuj kod]", "")
        main_city_lat, main_city_lon = get_nominatim_coords(main_city_name)

        partnering_cities_dict = {}
        all_rows = table.findAll("tr")
        for row in all_rows[1:]:
            if row.findAll('a') != []:
                all_td = row.findAll("td")
                city_cell = all_td[0]
                city_name = city_cell.text.replace('\xa0', '')
                city_link = "https://pl.wikipedia.org" + city_cell.findAll('a')[0]['href']
                city_lat, city_lon = get_geo_dms_coords(city_link)

                #partnering_cities_dict[city_name] = city_link
                partnering_cities_dict[city_name] = [city_lat, city_lon]

        #cities_with_parnering_cities[main_city_name] = partnering_cities_dict
        cities_with_parnering_cities[main_city_name] = {'coords': [main_city_lat, main_city_lon],
                                                        'partnering_cities': partnering_cities_dict}

    return cities_with_parnering_cities
