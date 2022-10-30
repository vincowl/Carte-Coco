# coding: utf8
# Import pandas
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from IPython.core.display import display

class MapGenerator:

    def __init__(self):
        self._filename = 'liste-membres.xlsx'
        self._path_villes_geom = 'villes.csv'
        return
    
    def readXLS(self):
        # Load spreadsheet
        xl = pd.ExcelFile(self._filename)
        #print(xl.sheet_names)
        # Load a sheet into a DataFrame by name: df1
        self._data = xl.parse(xl.sheet_names[0])
        return
        
    def readVilles(self):
        # Load spreadsheet
        df2 = pd.read_csv(self._path_villes_geom, sep=';') 
        col_out = ['EU_circo','code_région','nom_région','chef-lieu_région','préfecture','numéro_circonscription','éloignement']
        self._villes = df2.drop(col_out, axis=1).copy()
        #self._villes = df2.copy()
        return
    
    def mergeData(self):
        self._mergedData = self._data.join(self._villes.set_index('code_insee'), on='code insee', how='left')
        col_out = ['Commune', 'Code Postal']
        self._mergedData = self._mergedData.drop(col_out, axis=1).copy()
        return
    
    def printData(self):
        print(self._mergedData.head())
        print('Done')
        return
       
    def isMarkerFormateur(self, isFormateur):
#          Parameters
#     ----------
#     color : str, default 'blue'
#         The color of the marker. You can use:
#             ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
#              'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
#              'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
#              'gray', 'black', 'lightgray']
#     icon_color : str, default 'white'
#         The color of the drawing on the marker. You can use colors above,
#         or an html color code.
#     icon : str, default 'info-sign'
#         The name of the marker sign.
#         See Font-Awesome website to choose yours.
#         Warning : depending on the icon you choose you may need to adapt
#         the `prefix` as well.
#     angle : int, default 0
#         The icon will be rotated by this amount of degrees.
#     prefix : str, default 'glyphicon'
#         The prefix states the source of the icon. 'fa' for font-awesome or
#         'glyphicon' for bootstrapp3.
        return folium.Icon(color='blue', icon='comment', icon_color='white', prefix='fa')
        #try:
        #    float(isFormateur)
        #    return None
        #except:
        #    return folium.Icon(color='green', icon='ok-sign')
        
    
    def printMap(self):
        SF_COORDINATES = (10,0)
        # for speed purposes
        MAX_RECORDS = 1000
        # create empty map zoomed in on San Francisco
        attr = 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        tiles = 'https://korona.geog.uni-heidelberg.de/tiles/roads/x={x}&y={y}&z={z}'

        myMap = folium.Map(location=SF_COORDINATES, tiles=None, zoom_start=2)
        myMap.add_tile_layer(tiles='OpenStreetMap',  name='OpenStreetMap')
        myMap.add_tile_layer(tiles=tiles, attr=attr, name='Heidelberg Uni')
        # myMap = folium.Map(location=SF_COORDINATES, zoom_start=2)
        marker_cluster_parents = MarkerCluster(name='Parents',
                                       overlay=True,
                                       control=False,
                                       icon_create_function=None)
        marker_cluster_parents.add_to(myMap)
        marker_cluster_formateurs = MarkerCluster(name='Formateurs',
                                       overlay=True,
                                       control=False,
                                       icon_create_function=None)
        marker_cluster_formateurs.add_to(myMap)
        
        # add a marker for every record in the filtered data, use a clustered view
        for each in self._mergedData[0:MAX_RECORDS].iterrows():
            chaine = "<strong>"+each[1]['Nom']+"</strong><br/>"+each[1]['nom_commune']+'<br/><a href="https://www.facebook.com/messages/t/'+each[1]['identifiant FB']+'">Contacter</a>'
            icone = self.isMarkerFormateur(each[1]['Formateur'])
            marker = folium.Marker(
                location=[float(each[1]['latitude']), float(each[1]['longitude'])],
                popup=chaine,
                icon=icone,
                )
            if icone:
                marker.add_to(marker_cluster_formateurs)
            else:
                marker.add_to(marker_cluster_parents)
        folium.LayerControl().add_to(myMap)
        myMap.save('liste_coco.html') #save HTML
        #display(myMap)
        return


