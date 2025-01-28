from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from gifto.models import GiftoUser, Product, Hobby, Category, CategoryFeedback


class HobbySerializer(serializers.ModelSerializer):
  class Meta:
    model = Hobby
    fields = '__all__'


class GiftoUserSerializer(serializers.ModelSerializer):
  hobbies = HobbySerializer(many=True)

  class Meta:
    model = GiftoUser
    fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
  category = CategorySerializer()
  
  class Meta:
    model = Product
    fields = '__all__'


class CategoryFeedbackSerializer(serializers.ModelSerializer):
  category = CategorySerializer()
  user = GiftoUserSerializer()

  def create(self, validated_data):
    c = Category.objects.get(category_id=validated_data.pop("category")["category_id"])
    u = GiftoUser.objects.get(user=validated_data.pop("user")["user"])
    return CategoryFeedback.objects.create(
      user=u,
      category=c,
      feedback=validated_data["feedback"]
    )

  class Meta:
    model = CategoryFeedback
    fields = '__all__'


class GiftRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = GiftoUser
    exclude = ['user']