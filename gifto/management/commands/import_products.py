import csv
import random
from django.core.management import BaseCommand

from gifto.models import Product, Category


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument("csv_path", type=str)
    parser.add_argument("--limit", action="store", default=None)
    parser.add_argument("--replace", action="store_true", default=False)
    parser.add_argument("--shuffle", action="store_true", default=False)

  def handle(self, csv_path, limit, replace, shuffle, *args, **options):
    if replace:
      Product.objects.all().delete()
    products = []
    with open(csv_path, newline="") as src:
      r = csv.reader(src)
      header = next(r)
      for i, line in enumerate(r):
        if shuffle:
          products.append(dict(
            name=line[1],
            asin=line[0],
            image_url=line[2],
            product_url=line[3],
            stars=int(float(line[4]) * 10),
            price=int(float(line[5]) * 100),
            category_id=line[6],
            is_bestseller=line[7]
          ))
        else:
          Product.objects.create(
            name=line[1],
            asin=line[0],
            image_url=line[2],
            product_url=line[3],
            stars=int(float(line[4]) * 10),
            price=int(float(line[5]) * 100),
            category=Category.objects.get(category_id=line[6]),
            is_bestseller=line[7]
          )
          if limit and int(limit) == i + 1:
            break
    if shuffle:
      random.shuffle(products)
      for i, product in enumerate(products):
        category_id = product.pop("category_id")
        Product.objects.create(
          category=Category.objects.get(category_id=category_id),
          **product
        )
        if limit and int(limit) == i + 1:
          break