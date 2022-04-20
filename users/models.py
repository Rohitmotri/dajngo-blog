from django.db import models
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
from django.utils.text import gettext_lazy as _
from PIL import Image


class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile",default = "profilepic.jpeg",blank=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural =  _("Authors")

    def __str__(self):
        return self.user.username

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.picture:
            image  = Image.open(default_storage.open(self.picture.name))
            if image.height >300 or image.width >300:
                output_size = (300,300)
                image.thumbnail(output_size)
                buffer = BytesIO()
                image.save(buffer,format = "JPEG")
                default_storage.save(self.picture.name,buffer)