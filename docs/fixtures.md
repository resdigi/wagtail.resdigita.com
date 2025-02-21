# Fixtures in Wagtail.ResDigita.com

Fixtures are used here as initial data. They are a Django feature as described here.

<https://docs.djangoproject.com/en/5.1/topics/db/fixtures/>

Fixtures can be used to provide initial data for models, as described here 

<https://docs.djangoproject.com/en/5.1/howto/initial-data/>

## Note on use of venv in this document

The assumption here is that the venv virtual environment is at a `./venv` folder from the root. The venv python we use in this document is `./venv/bin/python` and also can be created with `make venv` (see [Makefile](../Makefile) and [installation](./installation.md)).

## Installation initial state

See [installation](./installation.md) documentation for setting up environment.

The conformity of the installation should be perfect for this to work. It probably is a good test of the installation itself.

## Loading initial fixtures on test initial data

This is assuming that you just created an empty Wagtail site. You can also use `make fixtures-load-test-initial` from the root (see [Makefile](../Makefile)).

`./venv/bin/python manage.py loaddata fixtures/test-initial.json`

and don't forget the media files

`cp fixtures/media/* media`

## Setting test initial data from current website to test initial data

This is assuming the website data is coherent with initial test data and is not running. You can also use `make fixtures-dump-test-initial` from the root (see [Makefile](../Makefile)).

`./venv/bin/python manage.py dumpdata  --natural-foreign wagtailcore.Locale wagtailcore.Revision wagtailcore.Page wagtailcore.Site wagtailimages.Image  wagtaildocs.Document  base  taggit  blog  project  home  wagtailresdigitacom  wagtailmenus > fixtures/test-initial.json`

and don't forget the media files.

## One way to test

You can create the initial environment as described in the [installation](./installation.md) documentation.

Assuming that the settings/dev.py is as follows.

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
```

Then you can then set the database state by copying the database files themselves. 

For the initial state before fixtures :

`cp fixtures/initialstate.db.sqlite3 db.sqlite3`

For the state with test data (after fixtures) :

`cp fixtures/targetstate.db.sqlite3 db.sqlite3`