from django.urls import path, include
from rest_framework import routers

from gifto.rest.views import RandomFeedback, RandomProduct
from gifto.rest.viewsets import ProductViewSet


urlpatterns = [
  path('catfeedback/random', RandomFeedback.as_view(), name="rest-random-feedback"),
  path('products', ProductViewSet.as_view({"get": "list"}), name="products"),
  path('products/random', RandomProduct.as_view(), name="random-product")
]