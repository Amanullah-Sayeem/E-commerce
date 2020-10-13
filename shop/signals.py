from django.dispatch import receiver
from  django.db.models.signals import post_save
from .models import Description, Product, Customer
from django.contrib.auth.models import User


@receiver(post_save, sender=Product)
def create_des(sender, instance, created, **kwargs):
    if created:
        Description.objects.create(product=instance)
        print('Description created')


@receiver(post_save, sender=Product)
def update_des(sender, instance, created, **kwargs):
    if not created:
        instance.description.save()
        print('updated Description')






@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        print('Customer profile created created')