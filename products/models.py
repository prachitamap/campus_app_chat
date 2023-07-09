from django.db import models
from logs.models import CUser

class Item(models.Model):
    BOOKS = 'books'
    EQUIPMENTS = 'equipments'
    TECHNICAL_GADGETS = 'technical gadgets'
    OTHER = 'other'
    CATEGORY_CHOICES = [ 
        (BOOKS, 'Books'),
        (EQUIPMENTS, 'Equipments'),
        (TECHNICAL_GADGETS, 'Technical Gadgets'),
        (OTHER, 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/')
    posted_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    seller = models.ForeignKey(CUser, on_delete=models.CASCADE,blank=True)



    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
