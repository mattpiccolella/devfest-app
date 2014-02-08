from django.db import models

# Create your models here.
class FacebookUser(models.Model):
    facebook_id = models.CharField(max_length = 80)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    def __unicode__(self):
        return self.first_name + " " + self.last_name
    @classmethod
    def create(cls,facebook_id,first_name,last_name):
        user = cls(facebook_id=facebook_id,first_name=first_name,last_name=last_name)
        return user

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    ranking = models.CharField(max_length=10)
    photo_reference = models.CharField(max_length=500)
    location_type = models.CharField(max_length=30)
    reference = models.CharField(max_length=500)
    website = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name + " " + self.address
    @classmethod
    def create(cls,name,latitude,longitude,address,ranking,photo_reference,location_type,reference,website):
        location = cls(name=name,latitude=latitude,longitude=longitude,address=address,ranking=ranking,photo_reference=photo_reference,location_type=location_type,reference=reference,website=website)
        return location

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    ranking = models.CharField(max_length=10)
    photo_reference = models.CharField(max_length=500)
    reference = models.CharField(max_length=500)
    website = models.CharField(max_length=100)
    food_type = models.CharField(max_length=100)
    price = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name + " " + self.address
    @classmethod
    def create(cls,name,latitude,longitude,address,ranking, photo_reference,reference,website,food_type,price):
        location = cls(name=name,latitude=latitude,longitude=longitude,address=address,ranking=ranking,photo_reference=photo_reference,reference=reference,website=website,food_type=food_type,price=price)
        return location
