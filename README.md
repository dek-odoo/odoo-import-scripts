# Summary
1. downloadGdrive_uploadodoo

These scripts download images from a given google drive folder following authentication, and uploads the downloaded images to configured odoo server using xmlrpclib.

2. gis_geojson_odoo_import

This will help migrate/export data from GIS softwares like QGIS to Odoo. The expected expected format is geojson, which is supported by most of the GIS Softwares.
These are script basically creates shape objects like polygons, it reads the geojson export file and creates shape objects in odoo database.

3. tangled

Converts xml to python objects.
Can be used to create records on odoo server from an xml file
It uses "untangle library" to read and parse xml records.
