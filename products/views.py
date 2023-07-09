from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Item, CUser, Wishlist
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import razorpay
from django.conf import settings


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_detail(request):
    pk = request.GET.get('pk')
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"message": "item not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(item)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    seller = request.user
    #serializer = ItemSerializer(data=request.data)
    serializer = ItemSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save(seller=seller)
        return Response({"message": "Item created Successfully"}, status=status.HTTP_201_CREATED)
    return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request):
    pk = request.data.get("pk")
    try:
        item = Item.objects.get(pk=pk, seller=request.user)
        item.delete()
        return Response({"message": "item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        return Response({"message": "item not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_items(request):
    user = request.user
    items = Item.objects.filter(seller=user)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request):
    pk = request.data.get("pk")
    data = request.data.copy()
    del data['seller']
    try:
        item = Item.objects.get(pk=pk, seller=request.user)
    except Item.DoesNotExist:
        return Response({"message": "item not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(instance=item, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "item updated", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    user = request.user
    item_id = request.data.get("item_id")
    try:
        item = Item.objects.get(pk=item_id)
        user_wishlist, created = Wishlist.objects.get_or_create(user=user)
        user_wishlist.items.add(item)
        user_wishlist.save()
        return Response({"message": "Item added to wishlist successfully"}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({"message": "item not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist_items(request):
    user = request.user
    try:
        wishlist = Wishlist.objects.get(user=user)
        items = wishlist.items.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    except Wishlist.DoesNotExist:
        return Response({"message": "Wishlist not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist(request):
    user = request.user
    user_wishlist, created = Wishlist.objects.get_or_create(user=user)
    items = user_wishlist.items.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
        


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request):
    user = request.user
    item_id = request.data.get("item_id")
    try:
        item = Item.objects.get(pk=item_id)
        user_wishlist, created = Wishlist.objects.get_or_create(user=user)
        user_wishlist.items.remove(item)
        user_wishlist.save()
        return Response({"message": "Item removed from wishlist successfully"}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({"message": "item not found"}, status=status.HTTP_404_NOT_FOUND)

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

import hmac
import hashlib

def generate_signature(payment_order_id, order_id):
    # Concatenate the payment_order_id and order_id with a pipe (|)
    payload = f'{payment_order_id}|{order_id}'

    # Replace 'YOUR_API_SECRET' with your actual Razorpay API secret key
    secret = 'mxYY2FZ2JPDFuhRkdPizhvJY'

    # Generate the signature using HMAC-SHA256 algorithm
    signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    
    return signature

@api_view(['POST'])
def create_payment(request):
    # Extract payment details from the request
    amount = request.data.get('amount')
    currency = request.data.get('currency')
    order_id = request.data.get('order_id')

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    # Create payment order
    payment_order = client.order.create({'amount': amount, 'currency': currency, 'receipt': order_id})

    # Generate the signature using your logic
    your_payment_order_id = payment_order['id']
    your_order_id = order_id
    your_signature = generate_signature(your_payment_order_id, your_order_id)

    # Return the payment order details and signature to the Flutter app
    return Response({
        'payment_order_id': your_payment_order_id,
        'order_id': your_order_id,
        'signature': your_signature,
        'amount': amount,
        'currency': currency
    })


# @api_view(['POST'])
# def create_payment(request):
#     # Extract payment details from the request
#     amount = request.data.get('amount')
#     currency = request.data.get('currency')
#     order_id = request.data.get('order_id')

#     # Initialize Razorpay client
#     client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

#     # Create payment order
#     payment_order = client.order.create({'amount': amount, 'currency': currency, 'receipt': order_id})

#     # Return the payment order details to the Flutter app
#     return Response({'payment_order_id': payment_order['id'], 'amount': amount, 'currency': currency})



@api_view(['POST'])
def payment_callback(request):
    # Extract payment callback data from the request
    payment_id = request.data.get('razorpay_payment_id')
    order_id = request.data.get('razorpay_order_id')
    signature = request.data.get('razorpay_signature')
    print("Payment ID:", payment_id)
    print("Order ID:", order_id)
    print("Signature:", signature)

    # Verify the payment callback data with Razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    try:
        client.utility.verify_payment_signature({'razorpay_payment_id': payment_id, 'razorpay_order_id': order_id, 'razorpay_signature': signature})
        # Payment is successful, update your database or perform other actions
        return Response(status=200)
    except razorpay.errors.SignatureVerificationError:
        # Payment verification failed
        return Response(status=400)
