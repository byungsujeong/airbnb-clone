import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampModel):

    """ Review Model Definition """

    review = models.TextField()
    accurancy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room.name} - {self.user.username}"

    def rating_average(self):
        avg = (
            self.accurancy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."

    def pass_90_days(self):
        now = datetime.datetime.utcnow()
        diff = (now - self.created.replace(tzinfo=None)).days
        if diff > 90:
            return True
        else:
            return False

    class Meta:
        ordering = ("-created",)
