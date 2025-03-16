# Resdigit@ website recreation in Wagtail

Wagtail Website for ResDigita.com

https://github.com/resdigi/wagtail.resdigita.com

The app name is `wagtailresdigitacom`. 

https://task.lesgrandsvoisins.com/projects/62

https://mark.lesgrandsvoisins.com/resdigita

https://wagtail.resdigita.com/

https://wagtail.resdigita.com/admin/

## Table of Contents

Here is our documentation

  - [Installation](./docs/installation.md)
  - [Fixtures (mainly initial data for now)](./docs/fixtures.md)
  - [Architecture and thoughts about workflow](./docs/architecture.md)
  - [Nixos in production](./docs/nixos.md)
  - [Starter template standard documentation](./docs/starter.md)
  - [Starter-news template we are not using](./docs/starter-news.md)

## Change of settings location (and urls.py and wsgi.py)

`settings` does not need to be in `wagtailresdigitacom` and is therefor at the root. `wsgi.py` nor `urls.py` neither, and are in the root settings folder. Other referencing parts of the application (`manage.py`, Gunicorn and `Dockerfile` mainly) have been adjusted accordingly.

## Version check

There may have been desynchornisation of git on different environments. Maybe we should have a version and installation check. 

## Web access

| Site | URL |
| ---  | --- |
| Qualification | <https://wagtail.resdigita.com> |
| Localhost | <http://localhost:8000> |
| Qualification Admin | <https://wagtail.resdigita.com/admin> |
| Localhost Admin | <http://localhost:8000/admin> |
| Qualification News | <https://wagtailnews.resdigita.com> |
| Qualification News Admin | <https://wagtailnews.resdigita.com/admin> |

| Username | Password |
| ---  | --- |
| admin | password |
