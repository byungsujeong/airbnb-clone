from django.utils import timezone
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models
from cal import Calendar


class AbstractItem(core_models.TimeStampModel):

    """ Item Model Definition """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


# Create your models here.
class Room(core_models.TimeStampModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *arg, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings = all_ratings + review.rating_average()

        if len(all_reviews) == 0:
            return 0
        else:
            return round(all_ratings / len(all_reviews), 2)

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        if this_month == 12:
            next_year = this_year + 1
            next_month = 1
        else:
            next_year = this_year
            next_month = this_month + 1

        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(next_year, next_month)

        return [this_month_cal, next_month_cal]

    # def get_guests(self):
    #     if self.guests == 1:
    #         return "1 guest"
    #     else:
    #         return f"{self.guests} guests"

    # def get_beds(self):
    #     if self.beds == 1:
    #         return "1 bed"
    #     else:
    #         return f"{self.beds} beds"

    # def get_bedrooms(self):
    #     if self.bedrooms == 1:
    #         return "1 bedroom"
    #     else:
    #         return f"{self.bedrooms} bedrooms"

    # def get_baths(self):
    #     if self.baths == 1:
    #         return "1 bath"
    #     else:
    #         return f"{self.baths} baths"

    # def review_num(self):
    #     all_reviews = self.reviews.all()
    #     return len(all_reviews)
