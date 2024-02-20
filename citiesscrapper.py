import requests
from bs4 import BeautifulSoup
import json


def get_partnering_cities_locations_with_nominatim(wiki_link):
    cities_dictionary = {}

    response = requests.get(wiki_link)
    soup = BeautifulSoup(response.text, features="html.parser")

    all_h2 = soup.findAll("h2")[1:]

    for h2 in all_h2:
        city_name = h2.text.replace("[edytuj | edytuj kod]", "")
        searchlink = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&addressdetails=1&limit=1"

        nominatim_respone = requests.get(searchlink)
        city_list = json.loads(nominatim_respone.text)
        city_dictionary = city_list[0]

        # cities_dictionary[city_name] = (city_dictionary.get("lat"), city_dictionary.get('lon'))
        cities_dictionary.update({city_name: (city_dictionary.get("lat"), city_dictionary.get('lon'))})

    return cities_dictionary


def get_partnering_cities_locations_with_geo_dms(wiki_link):
    response = requests.get(wiki_link)
    soup = BeautifulSoup(response.text, features="html.parser")
    all_h2 = soup.findAll("h2")[1:]


    another_cities_dictionary = {}

    for h2 in all_h2:
        all_a_tags = h2.findAll('a')
        city_a_tag = all_a_tags[0]
        city_name = city_a_tag.text
        city_href = city_a_tag['href']
        city_link = f'https://pl.wikipedia.org{city_href}'

        city_link_response = requests.get(city_link)
        city_soup = BeautifulSoup(city_link_response.text, features="html.parser")
        geo_dms = city_soup.findAll('span', {'class': 'geo-dms'})
        decimal_degrees = geo_dms[1]
        lat, lon = decimal_degrees.text.replace('\xa0', " ").replace(",", ".").split(" ")
        lat_float = float(lat)
        lon_float = float(lon)
        another_cities_dictionary.update({city_name: (lat_float, lon_float)})

    return another_cities_dictionary
