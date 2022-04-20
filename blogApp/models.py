from django.db import models
from django.contrib.auth.models import User
from users.models import Author
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage
# Create your models here.


class Categories(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class Post(models.Model):
    title = models.CharField(max_length= 255)
    title_tag = models.CharField(max_length=255, default='Blog post')
    slug = models.SlugField( null=True,blank= True)
    author = models.ForeignKey(Author,on_delete= models.CASCADE)
    img = models.ImageField(upload_to='blogsite',null=True)
    body = models.TextField(blank=True,null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Categories,null=True,related_name='categories')
    featured = models.BooleanField(default =False)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={"slug":self.slug})

    def get_update_url(self):
        return reverse("post_update",kwargs={"slug":self.slug})

    def get_delete_url(self):
        return reverse("post_delete",kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.img:
            img = Image.open(default_storage.open(self.img.name))
            if img.height > 1080 or img.width > 1920:  # pragma:no cover
                output_size = (1920, 1080)
                img.thumbnail(output_size)
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                default_storage.save(self.img.name, buffer)


class PostComment(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comment")

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return f'{self.sender.username}'


class Newsletter(models.Model):

    email = models.EmailField(_("Email"), max_length=254)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=True)

    class Meta:
        verbose_name = _("newsletter")
        verbose_name_plural = _("newsletters")

    def __str__(self):
        return self.email