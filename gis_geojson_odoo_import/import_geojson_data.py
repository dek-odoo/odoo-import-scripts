# -*- coding: utf-8 -*-

import json
import xmlrpclib

# EPSG format of Geojson file should match with the odoo EPSG format

from shapely.geometry import shape, MultiPolygon
import geojson

url = 'http://localhost:8071/xmlrpc'
username = 'admin'
password = 'admin'
dbname = 'db_name'

sock_common = xmlrpclib.ServerProxy(url + '/common')
uid = sock_common.login(dbname, username, password)
print "logged in as uid %s " % uid
sock = xmlrpclib.ServerProxy(url + '/object')

# Mapping of attributes in geojson file and related field name in odoo model
# mapping = {'attribute_nameingeojsonfile':'odoo_field_name'}

mapping = {'SNO': 'sno', 'NAME': 'name', 'VNAME': 'village_name'}
target_model = 'custom.gis'


with open('./sample_geo.geojson') as fread:
    features = json.load(fread)['features']

    for feature in features:

        if not feature['geometry']['coordinates']:
            continue
        if feature['geometry']['type'] == 'MultiPolygon':
            geo_fieldname = 'the_geom_multi'
        else:
            geo_fieldname = 'the_geom'  # its a polygon

        feature_json = json.dumps(feature['geometry'])
        feature_geo = geojson.loads(feature_json)
        geo_shape = shape(feature_geo)
        create_feature = {}
        create_feature[geo_fieldname] = geo_shape.wkt
        feature_properties = feature['properties']

        for feature_prop in feature_properties:
            try:
                if feature_properties[feature_prop] != None:
                    create_feature[mapping[feature_prop]] = feature_properties[feature_prop]
            except Exception, e:
                print "Exception %s " % (e)

        try:
            feature_id = sock.execute(dbname, uid, password, target_model, 'create', create_feature)
        except Exception, e:
            print "Failed creating Feature:\n %s " % (create_feature)
            print "Exception %s " % (e)
