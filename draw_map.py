import json
import folium

mymap = folium.Map(location=[52.2337172, 21.0714322], zoom_start=7)


with open("geo_dms.json") as nm_fl:
    cities = json.load(nm_fl)


for city in cities:
    folium.Marker(location=cities.get(city), popup=city).add_to(mymap)
    folium.PolyLine(locations=[cities.get(city), [52.2337172, 21.0714322]], color='blue').add_to(mymap)


mymap.save("map.html")

# napisać funkcję która narysuje czerwony marker dla miasta głównego, niebieskie markery dla miast partnerskich
# i linie łączące te miasta

# petla for przez miasta główne
# pobranie koordynatów i listy miast partnerskich
# pętla przez miasta partnerskie
# pobranie koordynatów miasta partnerskiego