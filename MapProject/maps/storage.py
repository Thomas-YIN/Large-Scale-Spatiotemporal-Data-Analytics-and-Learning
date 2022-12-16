from django.core.files.storage import FileSystemStorage
from django import forms


class MyStorage(FileSystemStorage):
    def _save(self, name, content, max_length=None):
        print(name)
        if self.exists(name):

            raise forms.ValidationError("Cannot upload a duplicated file!")

        return super(MyStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name
