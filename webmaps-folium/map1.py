import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(el):
    if el < 1000:
        return 'green'
    elif 1000<=el<3000:
        return 'orange'
    else:
        return 'red'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Mapbox Bright")
fg_v = folium.FeatureGroup(name = "Volcanoes")

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fg_v.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), fill_color=color_producer(el), color='grey', fill_opacity=0.7))

fg_p = folium.FeatureGroup(name="Population")
fg_p.add_child(folium.GeoJson(data=(open('world.json', 'r', encoding='utf-8-sig').read()),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000
else 'orange' if 10000000<=x['properties']['POP2005']<20000000 else 'red'}))
# x represents features
# geojson is a special type of json
map.add_child(fg_v)
map.add_child(fg_p)
map.add_child(folium.LayerControl())
#notice how we dont add it to the fg
# LayerControl considers fg as one single item of the layer control panel
# To have 2 items in the panel we need to make 2 fg children.
map.save("Map_html_popup_advanced.html")
