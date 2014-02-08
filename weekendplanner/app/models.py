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
    website = models.CharField(max_length=300)
    price = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name + " " + self.address
    @classmethod
    def create(cls,name,latitude,longitude,address,ranking, photo_reference,reference,website,price):
        location = cls(name=name,latitude=latitude,longitude=longitude,address=address,ranking=ranking,photo_reference=photo_reference,reference=reference,website=website,price=price)
        return location

class Event(models.Model):
    name = models.CharField(max_length=100)
    event_id = models.CharField(max_length=20)
    link = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name + " " + self.location
    @classmethod
    def create(cls,name,event_id,link,location,telephone,street_address,city,state,postal_code):
        event = cls(name=name,event_id=event_id,link=link,location=location,telephone=telephone,street_address=street_address,city=city,state=state,postal_code=postal_code)
        return event

class Trip(models.Model):
    user = models.ForeignKey(FacebookUser)
    location = models.ForeignKey(Location)
    event = models.ForeignKey(Event)
    restaurant = models.ForeignKey(Restaurant)
    event_link = models.CharField(max_length=200)
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.location.name
    @classmethod
    def create(cls,user,location,event,restaurant,event_link):
        trip = cls(user=user,location=location,event=event,restaurant=restaurant,event_link=event_link)
        return trip
