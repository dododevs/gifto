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

  __str__ = lambda self: f"Hobby({self.name})"

  class Meta:
    verbose_name = _("Hobby")
    verbose_name_plural = _("Hobbies")


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

  __str__ = lambda self: f"GiftoUser({self.user.username})"

  class Meta:
    verbose_name = _("Gifto User")
    verbose_name_plural = _("Gifto Users")


class Category(models.Model):
  category_id = models.IntegerField(
    verbose_name=_("Category ID from the original dataset")
  )

  name = models.CharField(
    max_length=256,
    verbose_name=_("Category name")
  )

  __str__ = lambda self: f"Category({self.category_id}, {self.name})"

  class Meta:
    verbose_name = _("Category")
    verbose_name_plural = _("Categories")


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

  __str__ = lambda self: f"Product({self.asin}, {self.name})"

  class Meta:
    verbose_name = _("Product")
    verbose_name_plural = _("Products")


class CategoryFeedback(models.Model):
  user = models.ForeignKey(
    GiftoUser,
    on_delete=models.CASCADE,
    verbose_name=_("User who submitted this feedback")
  )

  category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    verbose_name=_("Category this feedback refers to")
  )

  feedback = models.BooleanField(
    verbose_name=_("Approve/reject decision")
  )

  __str__ = lambda self: f"CategoryFeedback({self.user} said {'yes' if self.feedback else 'no'} to {self.category.name})"