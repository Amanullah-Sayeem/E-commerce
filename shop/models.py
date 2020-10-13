from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.user:
            name = self.user.username
        else:
            name = self.device
        return str(name)


class Product(models.Model):
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Description(models.Model):
    LARGE = 'L'
    EXTRA_LARGR = 'XL'
    MEDIM = 'M'
    SMALL = 'SM'
    PRODUCT_SIZE = (
        (LARGE, 'Large'),
        (EXTRA_LARGR, 'Extra Large'),
        (MEDIM, 'Median'),
        (SMALL, 'Small'),

    )
    BRAND_TYPE = (
        ('Richman', 'Richman'),
        ('Infinity', 'Infinity'),
        ('easy', 'easy'),

    )
    PRODUCT_FORMAT = (
        ('T_Shirt', 'T-Shirt'),
        ('Pant', 'Pant'),
        ('Shirt', 'shirt'),
    )
    USER_TYPE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    product = models.OneToOneField(Product, on_delete=models.CASCADE,null= True )
    brand = models.CharField(max_length=20, choices=BRAND_TYPE, null=True, blank=True, )
    size = models.CharField(max_length=255, choices=PRODUCT_SIZE, blank=True, null=True)
    format = models.CharField(max_length=10, choices=PRODUCT_FORMAT, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, blank=True, null=True)

    def __str__(self):
        return str(self.product.code)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address