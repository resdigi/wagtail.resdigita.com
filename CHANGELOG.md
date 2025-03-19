# Changelog

Wagtail Website for ResDigita.com

<https://github.com/resdigi/wagtail.resdigita.com>

## [0.1.1] - 205-03-19

- Documentation updates
- IMPORTANT: HOST_URL in .env file becomes HOST_NAME
- Debug Toolbar in InternalIPs work
  - Added DEBUG_TOOLBAR in .env
  - Added INTERNAL_IPS in settings/base.py
- Added service blog posts for publii blog feed
- Added PUBLII_FEED_URL to .env
- Renamed Blog Posts to Services on resdigita.models.PageHome 
- Added serice in resdigita.services for Publii post consumption
- Added Posts from Publii to resdigita.models.PageHome 

## [0.1.0] - 2025-03-17

When installing this version, one should consider doing a new install from scratch.

- ./home/: Removed "home" application (folder at top level and reference in settings/base.py)
- ./fixtures/: Changed ID in fixtures/*.json to reflect non-creation of default HomePage
- ./fixtures/: Still nees "admin" user to work
- Installation: Must manually create "Dashboard" user for OICD to work (/accounts/oidc/key-resdigita-com/login/?process=admin/login/)
- Installation: Added multiple requirements
- Development installation: make sass only works on development server (nixos prodction server will not pre-compile sass) require libsass
- Makefile: Included "if" statements to detect venv (python venv in ./.venv/) end env (file ./.env) required for most installations
- Makefile: Added makefile to ./resdigita/Makefile and ./resdigita/tailwind/Makefile
- ./wagtailresdigitacom: renamed to ./resdigita and app renamed to resdigita
- Makefile: commands are init (calling initenv, initvenv), messages, sass (only locally), requirements, superuser, makemigrations, migrate, produpdate (without sass call notably), update, runserver, start (legacy synonyme for runserver), secretkey, collectstatic, tailwind-install-bin-linux, tailwind-install, tailwind-compile, tailwind-compilemax, tailwind-watch, fixtures-dump-test-initial, fixtures-load-test-initial, 
- Open Connect: installed in ./settings/signals.py and ./resdigita/apps.py with .env variables as well
- API consumption from ghost.wagtail.com in ./resdigita/services.py. Should pull info, but not yet used on site.
- ./project/: Added tags and adjusted fixtures and ./resdigita/ accordingly
- ./docs/: renamed to [./doc/](./doc/)
- ./example.env: Added example .env file as multiple new variables are now required
- started creating tags
- Database: now configuring database from url in .env
- Tailwind: Using tailwind in ./resdigita with subfolder tailwind and corresponding makefile
- OICD: Redirects required in config (web front-end) for /fr/accounts/profile/ and /en/accounts/profile/ to home pages
- Changelog: See [common-changelog](https://github.com/vweevers/common-changelog) for formatting conventions.
- Added README.md files to most folders to explain what they are about
- Previously: Change of settings location (and urls.py and wsgi.py): `settings` does not need to be in `resdigita` and is therefor at the root. `wsgi.py` nor `urls.py` neither, and are in the root settings folder. Other referencing parts of the application (`manage.py`, Gunicorn and `Dockerfile` mainly) have been adjusted accordingly.
- Previously: Retired "Qualification News"

## [0.0.2] - 2025-01-20

## [0.0.1] - 2025-01-20

## [0.0.1-notemplate] - 2025-01-20
