import csv
from django.core.management import BaseCommand

from gifto.models import Hobby


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument("csv_path", type=str)

  def handle(self, csv_path, *args, **options):
    with open(csv_path, newline="") as src:
      r = csv.reader(src)
      header = next(r)
      for line in r:
        Hobby.objects.create(
          name=line[0],
          icon_id=line[1] if len(line) > 1 else None
        )