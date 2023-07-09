# from rest_framework import serializers
# from .models import Item

# # class ItemSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Item
# #         fields = '__all__'


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ['pk','name', 'description', 'price', 'image', 'posted_on', 'category']
#         extra_kwargs = {
#             'image': {'required': False},
#         }

from rest_framework import serializers
from .models import Item, Wishlist

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        # Get the seller instance from the request
        seller = self.context['request'].user

        # Set the seller field value in the validated data
        validated_data['seller'] = seller

        # Call the create method of the model manager to create a new instance
        instance = Item.objects.create(**validated_data)
        return instance





# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ['pk', 'name', 'description', 'price', 'image', 'posted_on', 'category']
#         extra_kwargs = {
#             'image': {'required': False},
#         }


class WishlistSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'items']





