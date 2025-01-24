from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Hobby(models.Model):
  name = models.CharField(
    max_length=64,
    verbose_name=_("Name")
  )

  icon_id = models.CharField(
    max_length=16,
    blank=True,
    null=True,
    verbose_name=_("Icon name")
  )


class GiftoUser(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name=_("System user")
  )

  age = models.PositiveSmallIntegerField(
    verbose_name=_("Age")
  )

  gender = models.CharField(
    max_length=1,
    choices=[
      ("M", "Male"),
      ("F", "Female"),
      ("O", "Other")
    ],
    verbose_name=_("Gender")
  )

  hobbies = models.ManyToManyField(
    Hobby,
    verbose_name=_("Hobbies")
  )


class Category(models.Model):
  category_id = models.IntegerField(
    verbose_name=_("Category ID from the original dataset")
  )

  name = models.CharField(
    max_length=32,
    verbose_name=_("Category name")
  )


class Product(models.Model):
  asin = models.CharField(
    max_length=10,
    verbose_name=_("ASIN code")
  )

  name = models.CharField(
    max_length=256,
    verbose_name=_("Name")
  )

  image_url = models.TextField(
    blank=True,
    null=True,
    verbose_name=_("Image URL")
  )

  product_url = models.TextField(
    blank=True,
    null=True,
    verbose_name=_("Amazon URL")
  )

  stars = models.PositiveIntegerField(
    blank=True,
    null=True,
    verbose_name=_("10x Star rating")
  )

  price = models.PositiveIntegerField(
    verbose_name=_("Item price in cents")
  )

  category = models.ForeignKey(
    Category,
    on_delete=models.PROTECT,
    verbose_name=_("Category")
  )

  is_bestseller = models.BooleanField(
    default=False,
    verbose_name=_("Amazon bestseller/choice")
  )