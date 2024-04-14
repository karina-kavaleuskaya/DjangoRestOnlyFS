from django.db import models
from users.models import CustomUser
from PIL import Image, ImageFilter
from django.conf import settings
import os


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}"


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return f"{self.name} {self.percent}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    is_blurred = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)

        if self.is_blurred:
            img = Image.open(self.image)
            img.save(os.path.join(settings.MEDIA_ROOT, self.image.name))
            blurred_img = img.filter(ImageFilter.GaussianBlur(radius=3))
            name_parts = self.image.name.split('/')
            new_name = name_parts[0] + '/blurred_' + name_parts[1]
            blurred_img.save(os.path.join(settings.MEDIA_ROOT, new_name))


class Stock(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    if_notif_sent = models.BooleanField(default=False)


