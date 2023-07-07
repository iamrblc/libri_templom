
###########################################
##       KRITIKUS TÁVOLSÁGÚ LIBRIK       ##
## LIBRI STORES WITHIN CRICITAL DISTANCE ##
###########################################

'''
FIGYELEM:
Egyáltalán nem gondolom, hogy a Librinek vagy bármi más könyvesboltnak tartózkodnia kellene bármilyen
könyv árusításától. Sőt! 
Ezt a kódot az elmúlt időszak abszurd híreire reagálva raktam össze. A Libri helyettesíthető bármely más
könyvesbolttal. De leginkább nem kellene egyik könyvesboltnak sem itt szerepelnie. 

Továbbá: a távolságszámítás erősen hozzávetőleges, valamint a címkézett pontok sem feltétlenül aktív
vallásgyakorlási helyszínek (néhány esetben ezt utánajárással megerősítettem, de volt, ahol egyértelműen
téves vagy elavult volt a címke.)

DISCLAIMER:
I strongly believe that neither Libri nor any other bookstore should refrain from selling any
books of any kind. On the contrary!
I put this code together in response to the absurd news of recent times. Libri could be replaced by any other
bookstore in the code. Or rather: no bookstore should be listed here.

Also: the distance calculation is only approximate and the labelled points are not necessarily active
places of worship (in some cases I confirmed this by checking but some labels might be incorrect or deprecated.)
'''

##################### IMPORT PACKAGES #####################
import requests
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import pandas as pd

##################### LIBRI BOLTOK KOORDINÁTÁI A LIBRI HONLAPJA ALAPJÁN #####################
##################### LIBRI STORES' COORDINATES FROM LIBRI'S WEBSITE #####################
libri_boltok = {
    'Mammut': (47.50908144618073, 19.0269507607113),
    'Hűvösvölgy': (47.53800329189616, 18.96607147353021),
    'Bécsi út': (47.54411998758937, 19.02877276447556),
    'Flórián tér': (47.542418394233785, 19.04086191534027),
    'Ferenciek tere (Antikvárium)': (47.49391146792732, 19.05687662698959),
    'Nyugati tér': (47.510065346587254, 19.05595628835068),
    'Oktogon': (47.506303837319905, 19.06207008465973),
    'West End': (47.51318164887298, 19.058774523875122),
    'Rákóczi út': (47.49557496131232, 19.063294626989595),
    'Aréna': (47.49862796394881, 19.091236100576474),
    'Corvin': (47.48646351215681, 19.074462764475562),
    'Árkád': (47.50343242654524, 19.140940597694097),
    'Árkád aluljáró szint': (47.503569835962196, 19.14106866897508),
    'Etele': (47.46505042057899, 19.024008663899085),
    'MOM Park': (47.49089049042988, 19.024072886044777),
    'Duna Pláza': (47.54944231291618, 19.072690269274588),
    'Sugár': (47.50478284156879, 19.138464034371495),
    'Pólus': (47.55349419145007, 19.14213566136109),
    'Köki': (47.463393723196674, 19.14613426989594),
    'Shopmark': (47.46419884881357, 19.129235645444336),
    'Csepel': (47.42415196496203, 19.06769696562851),
    'Campona': (47.406573120285, 19.015961997462),
    'Békéscsaba': (46.67696777678609, 21.090459220914752),
    'Budaörs': (47.45080071449938, 18.96360392983123),
    'Debrecen Fórum': (47.53283364872632, 21.62938107016877),
    'Dunaújváros': (46.97516177484419, 18.927293644182953),
    'Eger': (47.900864597294124, 20.368272086012453),
    'Győr Árkád': (47.6908897275265, 17.644883220914753),
    'Győr Plaza': (47.66970784130106, 17.65108064418295),
    'Kaposvár Korzó': (46.35576369227219, 17.787006850612837),
    'Kaposvár Plaza': (46.356201809505855, 17.78471420235345),
    'Kecskemét': (46.90856020567641, 19.69269581349023),
    'Kecskemét Malom': (46.90797971505145, 19.688936694431607),
    'Miskolc': (48.10273363508551, 20.78656637166073),
    'Miskolc Plaza': (48.10688357864317, 20.78855777908525),
    'Nagykanizsa': (46.45373603769817, 17.012103964236207),
    'Nyíregyháza Korzó': (47.95839663044216, 21.717216913987546),
    'Nyír Plaza': (47.955099740961565, 21.732511747397893),
    'Pécs Árkád': (46.07218859230572, 18.232343525124328),
    'Pécs': (46.075140681064035, 18.22813781349023),
    'Pécs Plaza': (46.04985481570616, 18.210973556811688),
    'Salgótarján': (48.106418151520145, 19.80940366002663),
    'Savaria Plaza': (47.222485683311504, 16.618125712992914),
    'Sopron Plaza': (47.69766707135632, 16.579845966953837),
    'Szeged Árkád': (46.25478822898022, 20.13894211769981),
    'Szeged Plaza': (46.266824354814446, 20.128865474875674),
    'Alba Plaza': (47.190176819475454, 18.40759395111015),
    'Szolnok': (47.17800139332624, 20.19410466274425),
    'Szolnok Plaza': (47.17770292682154, 20.19153081349023),
    'Szombathely': (47.23147212976262, 16.62262883205153),
    'Tatabánya': (47.58663536587684, 18.394439631056894),
    'Balaton Plaza': (47.09604905855249, 17.918340863738894),
    'Veszprém': (47.084187167359204, 17.92687684789521),
    'Zala Plaza': (46.84772234986528, 16.85222812041743)
}

##################### EZ A SZAKASZ SZEDI ÖSSZE A TÉRKÉPES ADATOKAT #####################
##################### THIS CHUNK COLLECTS MAP DATA #####################


# Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Templomok és vallásgyakorlási helyszínek lekérdezése

'''
Per pillanat csak a keresztény templomokra szűrtem, de elhagyható a religion="christian" feltétel és akkor
mindent megmutat. (A jogszabály szerint a vallásgyakorlási helyszíneknek nem kell feltétlenül kereszténynek
lenniük.)

Továbbá a lekérdezés kiegészíthető iskolákkal, óvodákkal, ifjúságvédelmi intézményekkel, hogy jobban megfeleljen
a jogszabályi előrásoknak.

For now it's only Christian places of worship. Can be extended by removing the religion="christian" condition.
Also the code can be extended by schools, kindergartens, youth protection institutions to better fit the legal
requirements.
'''

overpass_query = """
[out:json];
area["name"="Magyarország"]->.searchArea;
(
  node["amenity"="place_of_worship"]["religion"="christian"](area.searchArea);
  way["amenity"="place_of_worship"]["religion"="christian"](area.searchArea);
  relation["amenity"="place_of_worship"]["religion"="christian"](area.searchArea);
);
out center;
"""

# Lekérdezés futtatása / Run the query
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

# A templomok koordinátáira, illetve egyedi azonosítóikra van szükségünk / We need the coordinates and unique IDs of the churches
church_points = []
church_ids = []

for element in data['elements']:
    if element['type'] == 'node':
        lon = element['lon']
        lat = element['lat']
    elif 'center' in element:
        lon = element['center']['lon']
        lat = element['center']['lat']
    church_points.append(Point(lon, lat))
    church_ids.append(element['id'])

# A templomokat GeoDataFrame-be tettem... / Put the churches into a GeoDataFrame...
gdf_churches = gpd.GeoDataFrame(church_ids, columns=['id'], geometry=church_points)

# ...a könyvesboltokat szintén / ...and the bookstores too
bookstore_points = [Point(coord[::-1]) for coord in libri_boltok.values()]
bookstore_names = list(libri_boltok.keys())
gdf_bookstores = gpd.GeoDataFrame(bookstore_names, columns=['name'], geometry=bookstore_points)

##################### A KÖNYVESBOLTOKHOZ LEGKÖZELEBBI TEMPLOMOK KISZÁMÍTÁSA #####################
##################### CALCULATING THE NEAREST CHURCHES TO THE BOOKSTORES #####################

# Ez a függvény végzi a számítást / This function does the calculation

def calculate_nearest(row, destination, val, col="geometry"):
    distances = destination["geometry"].distance(row[col])
    idx_min = distances.idxmin()
    nearest_point = destination.loc[idx_min, "geometry"]
    nearest_id = destination.loc[idx_min, "id"]
    nearest_distance = distances.min()
    return pd.Series({f"nearest_{val}_id": nearest_id, f"nearest_{val}_point": nearest_point, f"distance_to_nearest_{val}": nearest_distance})

# A számítás futtatása (hozzávetőleges) / Run the calculation (approximation)
gdf_bookstores[["nearest_church_id", "nearest_church_point", "distance_to_nearest_church"]] = gdf_bookstores.apply(calculate_nearest, destination=gdf_churches, val="church", axis=1)
gdf_bookstores["distance_to_nearest_church_m"] = gdf_bookstores["distance_to_nearest_church"] * 111139

# A 200 méteres körzetben lévő könyvesboltok kiválasztása / Select the bookstores within 200 meters
nearby_bookstores = gdf_bookstores[gdf_bookstores['distance_to_nearest_church_m'] < 200]

# Ábrázolás / Plotting
fig, ax = plt.subplots(figsize=(12, 8))

ax.set_title("Vallásgyakorlási helyektől 200 méteren belül lévő Libri üzletek", fontweight='bold', fontsize=14)
gdf_churches.plot(ax=ax, color='white', edgecolor='gray', markersize=10, marker='o', label='Churches')
nearby_bookstores.plot(ax=ax, color='magenta', edgecolor='pink', markersize=50, marker='o', label='Bookstores')
ax.tick_params(colors='white')
plt.show()

# A 200 méteres körzetben lévő könyvesboltok listája / List of bookstores within 200 meters
print(gdf_bookstores[gdf_bookstores["distance_to_nearest_church_m"] < 200])
