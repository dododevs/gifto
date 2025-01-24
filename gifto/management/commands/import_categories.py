import csv
from django.core.management import BaseCommand

from gifto.models import Category


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument("csv_path", type=str)

  def handle(self, csv_path, *args, **options):
    with open(csv_path, newline="") as src:
      r = csv.reader(src)
      header = next(r)
      for line in r:
        Category.objects.create(
          category_id=int(line[0]),
          name=line[1]
        )