from django.db import models

# Create your models here.

class ImageModel(models.Model):
    image = models.ImageField(upload_to= 'static/landmarkWeb/images/media/user_uploaded_images')

    def get_image_url(self):
        return self.image.url

class landmarkModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 255)
    content = models.TextField()
    image_path = models.CharField(max_length = 255)

    