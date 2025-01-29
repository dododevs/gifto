import random
import uuid

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gifto.models import GiftoUser, Category, CategoryFeedback, Product
from gifto.rest.serializers import CategorySerializer, CategoryFeedbackSerializer, ProductSerializer, GiftRequestSerializer
from gifto.ml_model.recommend import recommend 


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


class RandomProduct(views.APIView):
  def get(self, request):
    products = Product.objects.all()
    product = random.choice(products)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


class FindGift(views.APIView):
  def post(self, request):
    serializer = GiftRequestSerializer(
      data=request.data
    )
    if serializer.is_valid():
      top_products = recommend(
        user_age=serializer.validated_data["age"],
        user_gender={
          "M": "male",
          "F": "female",
          "O": "male"
        }[serializer.validated_data["gender"]],
        user_hobbies=",".join([
          h.slug for h in serializer.validated_data["hobbies"]
        ])
      )
      top_products = [Product.objects.get(asin=asin) for asin in top_products]
      # top_products = random.sample(list(Product.objects.all()), k=5)
      serializer = ProductSerializer(
        top_products,
        many=True
      )
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)