import random
import uuid

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gifto.models import GiftoUser, Category, CategoryFeedback
from gifto.rest.serializers import CategorySerializer, CategoryFeedbackSerializer


class RandomFeedback(views.APIView):
  def get(self, request):
    gpusers = GiftoUser.objects.filter(
      user__username__startswith="_gp_"
    )
    gpuser = random.choice(gpusers)
    categories = Category.objects.all()
    category = random.choice(categories)
    return Response(CategoryFeedbackSerializer(
      CategoryFeedback(
        user=gpuser,
        category=category
      )
    ).data)

  def post(self, request):
    serializer = CategoryFeedbackSerializer(
      data=request.data
    )
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)