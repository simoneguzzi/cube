import re
from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html


from .models import Archetype, BacklogCard, Card, Color, Deck


@admin.register(Archetype)
class ArchetypeAdmin(admin.ModelAdmin):
    filter_horizontal = ("enablers", "payoffs")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    filter_horizontal = ("colors", "enabled_archetypes", "payed_off_archetypes")
    list_display = ("hover", "cmc", "playable")
    list_filter = ("playable", "enabled_archetypes", "payed_off_archetypes")
    readonly_fields = ("image",)
    search_fields = ("name",)

    def get_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ("image", ("enabled_archetypes", "payed_off_archetypes"), "playable")
        else:  # This is an addition
            return super().get_fields(request)

    def ignore(modeladmin, request, queryset):
        queryset.update(playable=False)

    actions = [ignore]

    def image(self, obj):
        return format_html('<img src="{}" width="100%"/>', obj.image_uri)

    @admin.display(ordering="name")
    def hover(self, obj):
        return format_html(
            """
            <a href="{3}" style="position: relative" 
            onmouseover="document.getElementById('{1}').style.display='block';"
            onmouseout="document.getElementById('{1}').style.display='none';">{2}
            <img id="{1}" style="display:none; position: absolute; top: 2em; left: 2em; z-index: 1" src="{0}" />
            """,
            obj.image_uri,
            obj.pk,
            obj.name,
            f"/admin/cube/card/{obj.pk}/change",
        )


@admin.register(BacklogCard)
class BacklogAdmin(CardAdmin):
    list_display = ("name", "cmc", "playable")
    list_filter = ()
    list_per_page = 10
    ordering = ("oracle_id",)

    def get_queryset(self, *args, **kwargs):
        return Card.objects.filter(
            playable=True, enabled_archetypes=None, payed_off_archetypes=None
        )


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    filter_horizontal = ("colors", "cards")

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field=from_field)
        # Cache object for use in formfield_for_manytomany
        request.deck_obj = obj
        return obj

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "cards" and hasattr(request, "deck_obj"):
            deck_colors = set(request.deck_obj.colors.all())
            kwargs["queryset"] = (
                Card.objects.annotate(
                    color_not_match_count=Count(
                        "colors", filter=~Q(colors__in=deck_colors)
                    )
                )
                .exclude(color_not_match_count__gt=0)
                .filter(
                    Q(enabled_archetypes=request.deck_obj.archetype)
                    | Q(payed_off_archetypes=request.deck_obj.archetype)
                )
            )
        return super(DeckAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass
