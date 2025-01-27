import random
import uuid
import numpy as np
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from gifto.models import GiftoUser, Hobby


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument("--count", action="store", default=30)
    parser.add_argument("--replace", action="store_true")

  def handle(self, count, replace, *args, **options):
    if replace:
      GiftoUser.objects.filter(
        user__username__startswith="_gp_"
      ).delete()
      User.objects.filter(
        username__startswith="_gp_"
      ).delete()

    hobbies = Hobby.objects.all()
    for _ in range(int(count)):
      guser = GiftoUser.objects.create(
        user=User.objects.create(
          username=f"_gp_{str(uuid.uuid4())}"
        ),
        age=random.choice(
          [i for i in range(1, 10)] +
          [i for i in range(10, 35)] * 4 +
          [i for i in range(35, 60)] * 2 +
          [i for i in range(61, 90)]
        ),
        gender=random.choice(["M"] * 10 + ["F"] * 10 + ["O"])
      )
      for _ in range(2, random.randrange(3, 6)):
        hobby = random.choice(hobbies)
        if not guser.hobbies.filter(name=hobby.name).exists():
          guser.hobbies.add(hobby)
      guser.save()