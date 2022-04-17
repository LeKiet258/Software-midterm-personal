from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer
from django.contrib.auth.models import Group

def customer_profile(sender, instance, created, **kwargs):
	if created:
        # automatically assign users signing up as a customer
		group = Group.objects.get(name='customer')
		instance.groups.add(group) # associate a user with a group
        
        # Added username because of error returning customer name if not added
		Customer.objects.create(
			user=instance,
			name=instance.username,
        )
		print('Profile created!')

post_save.connect(customer_profile, sender=User)