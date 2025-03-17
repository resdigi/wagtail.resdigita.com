# Changelog

See [common-changelog](https://github.com/vweevers/common-changelog) for formatting conventions.

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
- Makefile: commands are init (calling initenv, initvenv), messages, sass (only locally), requirements, superuser, makemigrations, migrate, produpdate (without sass call notably), update, runserver, start (legacy synonyme for runserver), secretkey, collectstatic, tailwind-install-bin-linux, tailwind-install, tailwind-compile, tailwind-compilemax, tailwind-watch, fixtures-dump-test-initial, fixtures-load-test-initial, - Open Connect: installed in ./settings/signals.py and ./resdigita/apps.py with .env variables as well
- API consumption from ghost.wagtail.com in ./resdigita/services.py. Should pull info, but not yet used on site.
- ./project/: Added tags and adjusted fixtures and ./resdigita/ accordingly
- ./docs/: renamed to ./doc/
- ./example.env: Added example .env file as multiple new variables are now required
- started creating tags
- Database: now configuring database from url in .env
- Tailwind: Using tailwind in ./resdigita with subfolder tailwind and corresponding makefile
- OICD: Redirects required in config (web front-end) for /fr/accounts/profile/ and /en/accounts/profile/ to home pages

## [0.0.2] - 2025-01-20

## [0.0.1] - 2025-01-20

## [0.0.1-notemplate] - 2025-01-20