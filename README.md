# Read Me
## Data Analysis Code

This is the analysis code for the data retrieved when conducting CE site testing. Everything for the magnetometer and seismometer analysis is contained in this is code. There is a .py version, which will run on any system that can run python. As well as a .ipynb, if you are using jupyter notebook. The code operates via a GUI and user inputs, so the user will not have to maunally go into the code and change variables.

Additionally, there are LIGO data files. These are so you can compare the field data to what is recorded at ligo. You will need to put these data files in the same directory as the code(s). The code should run with and without the data files downloaded.

In order for the code to operate properly, you'll need to install a package. To this in Jupyter, you'll need to go into the Qt Console; the built in terminal for anaconda navigator. There you can install the package via the method below.
```
conda install conda-forge::obspy
```
If that doesn't work, then you may need touse **pip install**
```
pip install obspy
```

After downloading the packages, you'll need to go to **Environments** and check that the packages are installed. If they are not appearing, you will need to select **Update Index**. You will then need to select the package and install it; this may take a bit. If any other packages are missing you can install them via the same method. Once everything is installed the codes should run properly

### FIle Section
Once you've started the code and selected magnetometer or seismometer, you will be greeted with a GUI. If you are using Windows, the icon will appear in your task bar. The icon will be the same as a file document with the top right corner folded. Once you click on that, it will bring up the GUI for fill selection. After you've found your desired file, you will need to close the GUI window in order to proceed in the code.

### Code Functions
The code has three primary plotting functions.
- Time series
- Amplitude Spectral Density Plot (ASD Plot)
- Spectrogram

There is a menu to go in between these functions. As well as additional menus to change the parameters of each plot and to further the data analysis process. Each function/option is denoted by a number. So, you simply need to type in the number an hit enter. 

If you have any questions or confusion, this is a video going through the data acquisition process as well as using the code.
https://www.youtube.com/watch?v=Re8FvCaCeBg
------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------
## Site Evaluation API

### Libraries

This is an API for Cosmic Explorer site evaluation, developed for ArcGIS in Python. 

You will have to install the following libraries before running the code. 
- arcgis
- geopandas
- shapely
- gdal
- pyproj
- pykml

Paste the following codeblock in your terminal to install them:
```
pip install arcgis arcgis-mapping geopandas shapely pyproj pykml
```
```
conda install -c conda-forge gdal
```

### Usage

Start with the file titled "setting_up." There are two ways of logging into your ArcGIS Online account, and the comments in "setting_up" will walk you through it. The code in "setting_up" will convert the KML files of the Cosmic Explorer sites to hosted feature layers, and publish them to your ArcGIS Online web map. KMLs must be converted to feature layers for ArcGIS to run any spatial analysis on them.

The file titled "buildings_and_kml_filter" will identify, count, and extract the coordinates of all the buildings within a certain distance of the two x- and y-arms that compose a site. The output will include two csv files, one with just the building counts for each site within a KML file, and another with both counts and coordinates for all the buildings near a site. Then, the code will filter the original KMLs down to include only those sites that have zero buildings nearby, after which it will output another csv of the number of total sites and sites with zero buildings for each KML.

The file titled "mapping_transportation" will output a csv with the kilometers of transportation lines within a certain radius of the three end stations (the x-end, y-end, and corner station) of each site. The transportation lines of interest to us include gravel roads, federal highways, and rail tracks. You will need to define the URL to the transportation lines dataset that you want the code to map. The [Transportation](https://www.arcgis.com/home/item.html?id=f42ecc08a3634182b8678514af35fac3) dataset provided by Esri is perfect for this purpose. Be aware, however, that you need to retrieve the URL of the line layer within the dataset. Scroll down on the page, and within the "Layers" section, click on, for example, the [local roads](https://www.arcgis.com/home/item.html?id=f42ecc08a3634182b8678514af35fac3&sublayer=8) line layer. The [URL](https://services2.arcgis.com/FiaPA4ga0iQKduv3/arcgis/rest/services/Transportation_v1/FeatureServer/8) can be copied from the strip on the right. I used "mapping_transportation" as a second stage of site evaluation, running it only on the KMLs with zero-building sites. If you intend to do that, head back to "setting_up" and publish your zero-building KMLs as layers first.

You will see that my code often generates "buffers" and publishes them to your web map. Essentially, the buffer you define will be the area of interest within which all your buildings and road data will be collected. 

Some things to note when running the code: 
- You will need to define file paths. Places where file paths need to be defined are clearly delineated with a comment in the code.
- When running spatial analysis on content available on your ArcGIS Online account, the code first essentially "searches" for content on your account. To find layers that you want to buffer, you can filter by title, tags, or feature type. This is why appropriate, distinct naming and tagging is so important in generating content for your account. The more content you publish, the more you want to make sure that names are distinguishable between, say, buffers for road mapping and and buffers for building extraction. For example, when running my code to map roads on zero-building sites, I look for the buffers I am interested in as follows:
```
circles = gis.content.search(
    f"title: 10km, zero, Idaho, Buffer AND owner:{gis.properties.user.username}",
    item_type="Feature Layer",
    max_items=10000
)
```
- If you have problems, feel free to shoot me an email! I would be happy to help. If you're using this code, you should know my name and you should be able to find my email address.
