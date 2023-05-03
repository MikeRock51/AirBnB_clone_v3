#!/usr/bin/python3
"""The place model"""


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models import storage
from os import getenv


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey(
                          'places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey(
                          'amenities.id'), primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """The place class"""
    __tablename__ = 'places'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []

        reviews = relationship('Review', backref='place',
                               cascade='all, delete')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initializes a Place instance"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Returns a list of Review instances"""
            reviewList = []
            allReviews = storage.all(Review)
            for instance in allReviews.values():
                if instance.place_id == self.id:
                    reviewList.append(instance)

            return reviewList

        @property
        def amenities(self):
            """Returns a list of amenity instances based on amenity_ids"""
            from models.amenity import Amenity

            amenityList = []
            allAmenities = storage.all(Amenity)

            for instance in allAmenities.values():
                if instance.id in self.amenity_ids:
                    amenityList.append(instance)

            return amenityList

        @amenities.setter
        def amenities(self, obj=None):
            """Adds the id of an amenity instance to amenity_ids"""
            if type(obj).__name__ == 'Amenity':
                self.amenity_ids.append(obj.id)
                print(self.amenity_ids)
