from django.shortcuts import get_object_or_404
from rest_framework import viewsets


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer