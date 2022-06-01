# Cube

## Local setup

1. Create a **virtual environment** with `python -m venv venv`, and activate it
   with `source venv/bin/activate`.
2. Install **dependencies** with `pip install -r requirements.txt`.
3. If necessary, install **dev dependencies** with `pip install -r requirements-dev.txt`.
4. Run **migrations** with `python project/manage.py migrate`.
5. Load key entities with `project/manage.py loaddata --format yaml - < project/cube/fixtures/init.yaml`.
6. Create an **admin** user with `python project/manage.py createsuperuser`.
7. Run the Django **server** with `python project/manage.py runserver`.

## Conventions

An **Archetype** is a group of cards which synergies together towards the same
strategy.

A **Deck** is the combination of an archetype and one or more colors.

An **Enabler**, with respect to a certain archetype, is a card that allows that
archetype's strategy to function.

A **Payoff**, with respect to a certain archetype, is a card that benefits from
the archetype's strategy. For some very aggressive decks, aggression can be
itself a payoff.
