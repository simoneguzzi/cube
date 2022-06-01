from django.db import models


class Color(models.Model):
    class Foo(models.TextChoices):
        WHITE = "W"
        BLUE = "U"
        BLACK = "B"
        RED = "R"
        GREEN = "G"

    color = models.CharField(
        max_length=1,
        choices=Foo.choices,
    )

    def __str__(self):
        return self.color


class Archetype(models.Model):
    name = models.TextField()
    enablers = models.ManyToManyField("Card", related_name="+", blank=True)
    payoffs = models.ManyToManyField("Card", related_name="+", blank=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    playable = models.BooleanField(default=True)
    image_uri = models.URLField()
    cmc = models.IntegerField()
    colors = models.ManyToManyField(Color, blank=True)
    name = models.TextField()
    oracle_id = models.UUIDField()
    type_line = models.TextField()
    enabled_archetypes = models.ManyToManyField(
        Archetype, through=Archetype.enablers.through, related_name="+", blank=True
    )
    payed_off_archetypes = models.ManyToManyField(
        Archetype, through=Archetype.payoffs.through, related_name="+", blank=True
    )

    def __str__(self):
        return self.name


class Deck(models.Model):
    archetype = models.ForeignKey(Archetype, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, blank=True)
    colors = models.ManyToManyField(Color)

    def __str__(self):
        return (
            "".join(str(color) for color in self.colors.all())
            + " "
            + str(self.archetype)
        )
