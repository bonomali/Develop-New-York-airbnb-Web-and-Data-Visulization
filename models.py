from mongoengine import *
from mongoengine import connect
connect('airbnb', host='127.0.0.1', port=27017)

# ORM

class ItemInfo(Document):
    Title = StringField()
    Place = StringField()
    Guests_num = IntField()
    Price = IntField()
    Cost_per_guest = IntField()

    meta = {'collection':'room_infoX'}



