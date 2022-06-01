from time import sleep
import requests
from django.core.management.base import BaseCommand

from cube.models import Card, Color

SCRYFALL_API = "https://api.scryfall.com/"
SCRYFALL_SEARCH_ENDPOINT = SCRYFALL_API + "cards/search?"


class Command(BaseCommand):
    help = "Ingests from Scryfall cards that match given query"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument("query", type=str)

    def handle(self, *args, **options):
        url = SCRYFALL_SEARCH_ENDPOINT + options["query"]

        while True:
            self.stdout.write(self.style.WARNING(f"Ingesting from {url}"))
            resp = requests.get(url=url)
            if resp.status_code == 200:
                body = resp.json()
                data = body["data"]
                for card in data:
                    try:
                        Card.objects.get(oracle_id=card["oracle_id"])
                    except Card.DoesNotExist:
                        try:
                            image_uris = card["image_uris"]
                        except KeyError:
                            image_uris = card["card_faces"][0]["image_uris"]
                        new_card = Card(
                            image_uri=image_uris["normal"],
                            cmc=card["cmc"],
                            name=card["name"],
                            oracle_id=card["oracle_id"],
                            type_line=card["type_line"],
                        )
                        new_card.save()
                        new_card.colors.add(
                            *(
                                Color.objects.get(color=color)
                                for color in card["color_identity"]
                            )
                        )
                if body["has_more"]:
                    url = body["next_page"]
                    # Comply with Scryfall good citizenship rate limits
                    sleep(1)
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully ingested {body['total_cards']} cards"
                        )
                    )
                    break
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Request failed with status code {resp.status_code}"
                    )
                )
                break
