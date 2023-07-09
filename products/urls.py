from django.urls import path
from .views import item_list, item_detail,create_item,delete_item, update_item,add_to_wishlist,wishlist_items,wishlist,remove_from_wishlist,create_payment, payment_callback
from . import views

app_name = 'products'


urlpatterns = [

    path('items/all/', item_list, name='item_list'),
    path('item/', item_detail, name='item_detail'),
    path('items/create/', create_item, name='createitem'),#New Ads
    path('items/delete/', delete_item, name='item_delete'),#Delete an Ads
    path('items/user/', views.user_items, name='user_items'),#My Ads
    path('items/update/', update_item, name='item_update'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/items/', wishlist_items, name='wishlist-items'),
    path('remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),

     # Endpoint to create a payment
    path('create-payment/', create_payment, name='create-payment'),

    # Endpoint to receive payment callbacks
    path('payment-callback/', payment_callback, name='payment-callback'),

]

