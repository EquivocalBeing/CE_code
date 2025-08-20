# Read Me

This is the analysis code for the data retrieved when conducting CE site testing. Everything for the magnetometer and seismometer analysis is contained this is code. There is a .py version, which will run on any system that can run python. As well as a .ipynb, if you are using jupyter notebook. The code operates via a GUI and user inputs, so you shouldn't have to manually check variable values and names.

Additionally, there are LIGO data files. These are so you can compare the field data to what is recorded at ligo. You will need to put these data files in the same directory as the code(s). The code should run with and without the data files downloaded.

------------------------------------------------------------------------------------------------------

To install the packages, you will need to either use **pip install** or **conda install conda-forge::**. There is a terminal (Qt Console) built into anaconda navigator, this is where you will want to download the packages.
After downloading the packages, go to **Environments** and check that the packages are installed. If they are not appearing, you will need to select **Update Index**. You will then need to select the package(s) and install them, this may take a bit. Once everything is installed the codes should run properly

------------------------------------------------------------------------------------------------------
# Read Me (this time for the site evaluation API)

This is an API for Cosmic Explorer site evaluation, developed for ArcGIS in Python. 

You will have to install the following libraries before running the code. 
- arcgis
- geopandas
- shapely
- pyproj

Here is how to install them in your Jupyter terminal.
```
pip install arcgis arcgis-mapping geopandas shapely pyproj
```

Start with the file titled "setting_up." There are two ways of logging into your ArcGIS online account, and the comments in "setting_up" will walk you through it. The code in "setting_up" will convert the KML files of the Cosmic Explorer sites to hosted feature layers, and publish them to your ArcGIS Online web map. KMLs must be converted to feature layers for ArcGIS to run any spatial analysis on them.

The file titled "buildings_and_kml_filtering" will identify, count, and extract the coordinates of all the buildings within a certain distance of the two x- and y-arms that compose a site. The output will include two csv files, one with just the building counts for each site within a KML file, and another with both counts and coordinates for all the buildings near a site. Then, the code will filter the original KMLs down to include only those sites that have zero buildings nearby, after which it will output another csv of the total sites and sites with zero buildings for each KML.

The file titled "mapping_roads" will output a csv with the kilometers of roads within a certain radius of the three end stations (the x-end, y-end, and corner station) of each site. You will need to define the URL to the roads dataset that you want the code to map. The [Transportation](https://www.arcgis.com/home/item.html?id=f42ecc08a3634182b8678514af35fac3) dataset provided by Esri is perfect for this purpose. Be aware, however, that you need to retrieve the URL of the line layer within the dataset. Scroll down on the page, and within the "Layers" section, click on, for example, the [local roads](https://www.arcgis.com/home/item.html?id=f42ecc08a3634182b8678514af35fac3&sublayer=8) line layer. The [URL](https://services2.arcgis.com/FiaPA4ga0iQKduv3/arcgis/rest/services/Transportation_v1/FeatureServer/8) can be copied from the strip on the right. I used "mapping_roads" as a second stage of site evaluation, running it only on the KMLs with zero-building sites. If you intend to do that, head back to "setting_up" and publish your zero-building KMLs as layers first.

You will see that my code often generates "buffers" and publishes them to your web map. Essentially, the buffer you define will be the area of interest within which all your buildings and road data will be collected. 

Some things to note when running my code: 
- You will need to define file paths. Places where file paths need to be defined are clearly delineated with a comment in the code.
- When running spatial analysis on content available on your ArcGIS account, the code first essentially "searches" for content on your ArcGIS Online. To find layers that you want to buffer, you can filter by title, tags, or feature type. This is why appropriate, distinct naming and tagging is so important in generating content for your account. The more content you publish, the more you want to make sure that names are distinguishable between, say, buffers for road mapping and and buffers for building extraction. For example, when running my code to map roads on zero-building sites, I look for the buffers I am interested in as follows:
```
circles = gis.content.search(
    f"title: 10km, zero, Idaho, Buffer AND owner:{gis.properties.user.username}",
    item_type="Feature Layer",
    max_items=10000
)
```
- If you have problems, feel free to shoot me an email! I would be happy to help. You know my name, so you should be able to find my email. 
