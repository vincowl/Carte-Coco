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
        try:
            float(isFormateur)
            return None
        except:
            return folium.Icon(color='green', icon='ok-sign')
        
    
    def printMap(self):
        SF_COORDINATES = (10,0)
        # for speed purposes
        MAX_RECORDS = 1000
        # create empty map zoomed in on San Francisco
        attr = 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        tiles = 'https://korona.geog.uni-heidelberg.de/tiles/roads/x={x}&y={y}&z={z}'

        myMap = folium.Map(location=SF_COORDINATES, tiles=tiles, attr=attr, zoom_start=2)
        # myMap = folium.Map(location=SF_COORDINATES, zoom_start=2)
        marker_cluster = MarkerCluster().add_to(myMap)
        # add a marker for every record in the filtered data, use a clustered view
        for each in self._mergedData[0:MAX_RECORDS].iterrows():
            chaine = "<strong>"+each[1]['Nom']+"</strong><br/>"+each[1]['nom_commune']+'<br/><a href="https://www.facebook.com/messages/t/'+each[1]['identifiant FB']+'">Contacter</a>'
            folium.Marker(
                location=[float(each[1]['latitude']), float(each[1]['longitude'])],
                popup=chaine,
                icon=self.isMarkerFormateur(each[1]['Formateur']),
                ).add_to(marker_cluster)
        myMap.save('liste_coco.html') #save HTML
        #display(myMap)
        return

