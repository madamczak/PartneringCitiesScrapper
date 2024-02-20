import json
from citiesscrapper import get_partnering_cities_locations_with_geo_dms, get_partnering_cities_locations_with_nominatim


if __name__ == '__main__':
    geo_dms = get_partnering_cities_locations_with_geo_dms(
        'https://pl.wikipedia.org/wiki/Wikiprojekt:Miasta_Partnerskie/lista')
    nominatim = get_partnering_cities_locations_with_nominatim(
        'https://pl.wikipedia.org/wiki/Wikiprojekt:Miasta_Partnerskie/lista')

    with open("geo_dms.json", "w") as geo_dms_file:
        json.dump(geo_dms, geo_dms_file)

    with open("nominatim.json", "w") as nominatim_file:
        json.dump(nominatim, nominatim_file)
