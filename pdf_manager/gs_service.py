from google.cloud import storage
from django.conf import settings
#returns a refernce to file in google cloud storage
def get_blob(filename):
    # Get a reference to the Cloud Storage bucket
        client = storage.Client.from_service_account_json(settings.GS_CREDENTIALS)
        bucket = client.get_bucket(settings.GS_BUCKET_NAME)

        return bucket.blob(filename)
