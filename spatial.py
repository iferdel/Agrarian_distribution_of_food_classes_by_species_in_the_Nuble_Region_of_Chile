import geopandas as gdp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyproj import Proj


class RegionMap():

    def __init__(self, shp_file, region):
        self.shp_file = shp_file
        self.geodf = gdp.read_file(shp_file, dtype={'geometry': 'geometry'})
        region_idx = np.where(self.geodf.loc[:, 'Region'].str.lower().str.contains(region.lower()))
        self.df = self.geodf.iloc[region_idx].to_crs("EPSG:4326") #crs: Coordinate Reference System. This method allows us to transform from utm to lat-lon
        self.region = self.df.loc[:, 'Region'].unique()
        
    def __str__(self):
        return 'Región: ', np.array2string(self.region),  'Coordinate Reference System (CRS): ', self.df.crs
    
    def df_polygon(self):
        self.df_geo = self.df.loc[:, ['Comuna', 'geometry']]
        self.df_geo.set_index('Comuna', inplace=True)
        return self.df_geo

    def map_display(self, label_display=False):
        if label_display:
            self.df['coords'] = self.df.loc[:, 'geometry'].apply(lambda x: x.representative_point().coords[:])
            self.df['coords'] = [coords[0] for coords in self.df.loc[:, 'coords']]
            
            ax = self.df.plot(color='white', edgecolor='black', figsize = (7,5))
            for idx, row in self.df.iterrows():
                plt.annotate(text=row['Comuna'], xy=row['coords'], horizontalalignment='center', fontsize=6)
            return ax
        else:
            ax = self.df.plot(color='white', edgecolor='black', figsize = (7,5))
            return ax


class SpatialTransform():

    def __init__(self):
        pass

    def utm_to_latlon(self, dataframe, east, north):
        self.dataframe = dataframe
        self.east = east
        self.north = north
        #transformation of coordinates from UTM coordinates to longitude, latitude data based on https://ocefpaf.github.io/python4oceanographers/blog/2013/12/16/utm/
        x = self.dataframe.loc[:, self.east]
        y = self.dataframe.loc[:, self.north]
        df_utm = pd.DataFrame(np.c_[x, y], columns=['Meters East', 'Meters South'], index=self.dataframe.index)
        #Proj element to classify the projection of the data from the input
        myProj = Proj(proj='utm', zone='18', south=True, ellps='WGS84', units='m')
        lon, lat = myProj(df_utm.loc[:,'Meters East'].values, df_utm.loc[:,'Meters South'].values, inverse=True) 
        #inverse=True referst to the conversion UTM-> lat,lon. inverse=False would mean lat,lon->UTM transformation
        df_lat_lon = pd.DataFrame(np.c_[lat, lon], columns=['Lat', 'Lon'], index=df_utm.index)
        return self.dataframe.merge(df_lat_lon, how='outer', left_on=self.dataframe.index, right_on=df_lat_lon.index)
        

def main():
    region = RegionMap(shp_file='Comunas.shp', region='ñuble')
    print(region.geodf.head())
    print(region.__str__())
    region.map_display(label_display=False)
    plt.show()

if __name__ == '__main__':
    main()