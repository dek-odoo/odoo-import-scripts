
The import scripts depend on OCA/geospatial repository (https://github.com/OCA/geospatial).

It imports the polygon/multipolygon data from geojson file.
Geojson file can be exported from QGIS or any other GIS software you use.
You can have a look at the sample_geo.geojson file of this repository.


You can create your own model with fields you need. e.g. 'custom.gis'

Special features for GIS can be created as following

	govt_land = geo_fields.GeoMultiPolygon('Government land')
	security_checkpoint = geo_fields.GeoPoint('Security checkpoint')
	power_supply_line = geo_fields.GeoLine('Power supply line', index=True)
