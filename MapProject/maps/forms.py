from django import forms
from .models import *


class GeoJsonForm(forms.ModelForm):
    geojson_file = forms.FileField(required=False)

    class Meta:
        model = Json
        fields = ["geojson_file"]

    def clean_geojson_file(self):
        geojson_file = self.cleaned_data.get("geojson_file")

        if geojson_file is None:
            raise forms.ValidationError("Choose a file to upload!")
        return geojson_file

class TableForm(forms.ModelForm):
    # table_data = forms.FileField(required=False)
    description = forms.CharField(required=False, 
                                  widget=forms.Textarea(
            attrs={"placeholder": "Add a description about your data!",}
        ))

    class Meta:
        model = Table
        fields = ["table_data", "admin_level", "description"]

    def clean_table(self):
        table_data = self.cleaned_data.get("table_data")

        if table_data is None:
            raise forms.ValidationError("Choose a file to upload!")
        return table_data