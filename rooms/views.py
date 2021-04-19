from django.utils import timezone
from django_countries import countries
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from . import models

# Create your views here.
class HomeVIew(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = request.GET.get("price", 0)
    guests = request.GET.get("guests", 0)
    beds = request.GET.get("beds", 0)
    bedrooms = request.GET.get("bedrooms", 0)
    baths = request.GET.get("baths", 0)
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    c_amenities = request.GET.getlist("amenities")
    c_facilities = request.GET.getlist("facilities")
    c_house_rules = request.GET.getlist("house_rules")
    print(instant)
    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "instant": instant,
        "super_host": super_host,
        "c_amenities": c_amenities,
        "c_facilities": c_facilities,
        "c_house_rules": c_house_rules,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    house_rules = models.HouseRule.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    return render(
        request,
        "rooms/search.html",
        {**form, **choices},
    )
