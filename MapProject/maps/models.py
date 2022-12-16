from email.policy import default

import json
from django.db import models
from .storage import MyStorage

'''
Admin boundaries updated by administrator.
'''
class AdminBoundary(models.Model):

    geojson = models.FileField(upload_to="geo_static/", storage=MyStorage(), unique=True)

    def get_abs_url(self):
        return f"/{self.geojson.name}"

'''
Data uploaded in json format.
'''
class Json(models.Model):

    geojson_file = models.FileField(upload_to="data/json/", storage=MyStorage(), unique=True)

    def get_abs_url(self):
        return f"/{self.geojson_file.name}"

'''
Data uploaded in csv format.
'''
class Table(models.Model):

    table_data = models.FileField(upload_to="data/csv/", storage=MyStorage(), unique=True)
    admin_level = models.IntegerField()     # Describes the admin level of the data (eg. district, state...)
    description = models.TextField()

    def get_abs_url(self):
        return f"/{self.table_data.name}"

