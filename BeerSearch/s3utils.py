from storages.backends.s3boto import S3BotoStorage
from django.core.files.storage import get_storage_class

MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')


class StaticRootS3BotoStorage(S3BotoStorage):
    def __init__(self):
        super().__init__(
            location="static"
        )


class CachedS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


CompressorS3BotoStorage = lambda: CachedS3BotoStorage(
    location='compressor')