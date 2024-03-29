from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from . import forms


# Create your views here.
def create_review(request, room):
    print(request.method)
    if request.method == "POST":
        print("post?")
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
