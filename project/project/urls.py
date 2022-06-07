"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from itertools import chain, groupby
from random import choice, sample

from django.contrib import admin
from django.db.models import QuerySet
from django.urls import path

from cube.models import Archetype, Card

THRESHOLD = 2


def random_deck_suggestion():
    while True:
        archetype: Archetype = choice(list(Archetype.objects.all()))
        pool: QuerySet[Card] = archetype.enablers.all().union(archetype.payoffs.all())
        colors = chain(*(card.colors.all() for card in pool))
        frequencies = (
            (color, len(list(cards)))
            for (color, cards) in groupby(
                sorted(colors),
            )
        )
        frequent_colors = [color for color, count in frequencies if count >= THRESHOLD]
        if len(frequent_colors):
            break

    random_colors = sorted(
        frequent_colors if len(frequent_colors) <= 1 else sample(frequent_colors, 2)
    )
    return f"{''.join(color.__str__() for color in random_colors)} {archetype}"


admin.site.index_title = f"Hi! Have you considered {random_deck_suggestion()}?"

urlpatterns = [
    path("", admin.site.urls),
]
