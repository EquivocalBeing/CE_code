These codes are used to analysis the data retrieved from the seismometer and magnetometer while site testing for Cosmic Explorer.
They are in the Jupyter Notebook format, so you'll need to download Anaconda to use the data offline.

Both of the codes are anotated with instructions on how to run the code. There is also basic example files that can be used to run the scripts.

###########################################################################################################################################################################################

For retrieving data from the WebDAQ, the data can be converted to csv inside the premade software.

For the Minimus, data can be download from the storage page. However, it only saves it as a mseed file.
If you do not have a way to convert it to a csv, this GitHub page is what I used to get the data

https://github.com/iris-edu/mseed2ascii

It creates an executable with C code. It has an user manual on all it's functions
I found this format to give the most user friendly data:

./mseed2ascii -G -f 2 -o outfile_name data/file/path
