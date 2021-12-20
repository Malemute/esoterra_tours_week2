from random import sample

from django.http import Http404
from django.http import HttpResponseBadRequest, HttpResponseNotFound, \
    HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render
from django.views import View

from tours.data import tours, departures


class MainView(View):
    def get(self, request, *args, **kwargs):
        random_tours_id = sample(tours.keys(), 6)
        tour = {tour_id: tours[tour_id] for tour_id in random_tours_id}
        return render(
            request, 'tours/index.html',
            context={'tours': tour, 'departures': departures})


class DepartureView(View):
    def get_data(self, city):
        city_name = departures[city]
        available_tours = {i: tours[i] for i in tours
                           if tours[i]['departure'] == city}
        min_price = min([available_tours[i]['price'] for i in available_tours])
        max_price = max([available_tours[i]['price'] for i in available_tours])
        min_nights = min([available_tours[i]['nights']
                          for i in available_tours])
        max_nights = max([available_tours[i]['nights']
                          for i in available_tours])
        context = {'city_name': city_name, 'available_tours': available_tours,
                   'min_price': min_price,
                   'max_price': max_price,
                   'min_nights': min_nights,
                   'max_nights': max_nights}
        return context

    def get(self, request, city, *args, **kwargs):
        available_cities = set([tours[i]['departure'] for i in tours])

        if city not in available_cities:
            raise Http404

        context = self.get_data(city)

        return render(
            request, 'tours/departure.html',
            context={'data': context, 'departures': departures})


class TourView(View):
    def get(self, request, id_tour, *args, **kwargs):
        if id_tour not in tours:
            raise Http404

        tour_title = tours[id_tour]['title']
        description = tours[id_tour]['description']
        departure_city = departures[tours[id_tour]['departure']]
        picture = tours[id_tour]['picture']
        price = tours[id_tour]['price']
        tour_stars = tours[id_tour]['stars']
        country = tours[id_tour]['country']
        nights = tours[id_tour]['nights']

        return render(
            request, 'tours/tour.html',
            context={'title': f'{tour_title} {tour_stars}',
                     'departure': departure_city, 'picture': picture,
                     'description': description, 'price': price,
                     'country': country, 'nights': nights,
                     'departures': departures})


def custom_handler400(request, exception):
    # Call when SuspiciousOperation raised
    return HttpResponseBadRequest('Неверный запрос!')


def custom_handler403(request, exception):
    # Call when PermissionDenied raised
    return HttpResponseForbidden('Доступ запрещен!')


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
