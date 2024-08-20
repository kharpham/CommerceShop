from django.core.files.storage import FileSystemStorage
from django.conf import settings

class CKEditor5Storage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.MEDIA_ROOT + '/ckeditor_uploads/'
        kwargs['base_url'] = settings.MEDIA_URL + 'ckeditor_uploads/'
        super().__init__(*args, **kwargs)