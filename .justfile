# ----------------------------------------------------------------------------
# wagtail.resdigita.com — `just` recipes
#
# A `just`-native equivalent of the Makefile (which is intentionally kept).
# Run `just --list` to see all recipes. To make a recipe the default when you
# type bare `just`, add `default` to the alias/recipe list at the bottom.
# ----------------------------------------------------------------------------

# --- Environment -------------------------------------------------------------
# .env is not auto-loaded by `just`; read the variables we need with defaults
# that match example.env and the Makefile.
use_docker := env_var_or_default("USE_DOCKER", "0")
docker_container := env_var_or_default("DOCKER_CONTAINER", "web")

# Project root and per-mode paths (mirrors the Makefile's PROJECT_PATH logic).
repo_root := `git rev-parse --show-toplevel`
project_path := if use_docker == "1" { "/home/wagtail/resdigita/" } else { repo_root + "/" }
venv_py := project_path + ".venv/bin/python"
venv_pip := project_path + ".venv/bin/pip"
exec_cmd := if use_docker == "1" { "docker-compose exec -ti " + docker_container } else { "" }

host_name := env_var_or_default("HOST_NAME", "0.0.0.0")
host_port := env_var_or_default("HOST_PORT", "8000")

# --- Bootstrap ---------------------------------------------------------------

# Create .env from the template (refuses if .env already exists).
initenv:
    @test ! -e .env || (echo ".env exists at .env please remove." && exit 1)
    mkdir -p static media
    cp example.env .env
    @echo "MERCI DE CONFIGURER .env AVEC VOS VARIABLES D'ENVIRONNEMENT"

# Create the virtualenv (refuses if .venv already exists).
initvenv:
    @test ! -e .venv || (echo "venv exists at .venv. please remove if you wish to recreate." && exit 1)
    @echo "You MUST copy and paste as follows if you want an environment"
    @echo "source ./venv/bin/activate"
    {{ exec_cmd }} python -m venv {{ project_path }}.venv

# Install/upgrade Python dependencies (root + resdigita requirement files).
requirements:
    {{ exec_cmd }} {{ venv_pip }} install --upgrade pip
    {{ exec_cmd }} {{ venv_pip }} install -r {{ project_path }}requirements.txt
    cd resdigita && {{ exec_cmd }} {{ venv_pip }} install -r requirements.txt

# --- Django management -------------------------------------------------------

makemigrations:
    {{ exec_cmd }} {{ venv_py }} ./manage.py makemigrations

migrate:
    {{ exec_cmd }} {{ venv_py }} ./manage.py migrate

superuser:
    {{ exec_cmd }} {{ venv_py }} manage.py createsuperuser --username admin --email admin@resdigita.com

# Extract translatable strings (French + English).
messages:
    {{ exec_cmd }} {{ venv_py }} manage.py makemessages -l fr -l en

compilemessages:
    ./.venv/bin/python manage.py compilemessages

makemessages:
    ./.venv/bin/python manage.py makemessages -l en -l fr

collectstatic:
    {{ exec_cmd }} {{ venv_py }} ./manage.py collectstatic --noinput

secretkey:
    {{ exec_cmd }} {{ venv_py }} -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

runserver:
    {{ exec_cmd }} {{ venv_py }} ./manage.py runserver {{ host_name }}:{{ host_port }}

start: runserver

# --- Tailwind ----------------------------------------------------------------

# Download the standalone tailwind binary into the venv (Linux x86-64).
tailwind-install-bin-linux:
    wget https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
    mv tailwindcss-linux-x64 venv/bin/tailwindcss
    chmod +x venv/bin/tailwindcss

# npm-install the tailwind CLI in resdigita.
tailwind-install:
    #!/usr/bin/env bash
    set -euo pipefail
    cd resdigita/tailwind
    npm install tailwindcss @tailwindcss/cli

# Compile tailwind CSS for both resdigita and blog.
tailwind-compile:
    #!/usr/bin/env bash
    set -euo pipefail
    (cd resdigita/tailwind && npx @tailwindcss/cli -i ./tailwind/input.css -o ./static/css/resdigita/tailwind.css --cwd .. -m)
    (cd blog/tailwind && npx @tailwindcss/cli -i ./tailwind/input.css -o ./static/blog/css/tailwind.css --cwd .. -m)

# Alias kept for backward compatibility with the Makefile.
tailwind-compilemax: tailwind-compile

# Watch mode for tailwind (both apps).
tailwind-watch:
    #!/usr/bin/env bash
    set -euo pipefail
    (cd resdigita/tailwind && npx @tailwindcss/cli -i ./tailwind/input.css -o ./static/css/resdigita/tailwind.css --cwd .. --watch)
    (cd blog/tailwind && npx @tailwindcss/cli -i ./tailwind/input.css -o ./static/blog/css/tailwind.css --cwd .. --watch)

# --- Assets ------------------------------------------------------------------

# Install tailwind and compile CSS, then compile Django SASS.
sass:
    #!/usr/bin/env bash
    set -euo pipefail
    (cd resdigita/tailwind && npm install tailwindcss @tailwindcss/cli)
    (cd resdigita/tailwind && npx @tailwindcss/cli -i ./tailwind/input.css -o ./static/css/resdigita/tailwind.css --cwd .. -m)
    {{ exec_cmd }} {{ venv_py }} manage.py compilescss

# --- Fixtures ----------------------------------------------------------------

fixtures-dump-test-initial:
    #!/usr/bin/env bash
    set -euo pipefail
    cd fixtures
    rm *.json
    {{ exec_cmd }} {{ venv_py }} {{ project_path }}manage.py dumpdata --natural-foreign wagtailcore.Locale wagtailcore.Revision wagtailcore.Page wagtailcore.Site wagtailimages.Image wagtaildocs.Document base taggit blog project home resdigita wagtailmenus > {{ project_path }}fixtures/test-initial.json
    mkdir -p {{ project_path }}fixtures/media/images
    mkdir -p {{ project_path }}fixtures/media/original_images
    cp -a {{ project_path }}media/images/* {{ project_path }}fixtures/media/images
    cp -a {{ project_path }}media/original_images/* {{ project_path }}fixtures/media/original_images

fixtures-load-test-initial:
    #!/usr/bin/env bash
    set -euo pipefail
    cd fixtures
    {{ exec_cmd }} {{ venv_py }} {{ project_path }}manage.py loaddata {{ project_path }}fixtures/test-initial.json
    cp -a {{ project_path }}fixtures/media/* {{ project_path }}media

# --- Orchestrated targets ----------------------------------------------------

# Full first-time setup (env + venv + deps + migrate + superuser + tailwind).
init:
    @test -e .env || (just initenv && exit 1)
    @test -d .venv || just initvenv
    just requirements
    just migrate
    just superuser
    just tailwind-install

produpdate:
    just collectstatic
    just migrate

update:
    just sass
    just makemigrations
    just messages
    just produpdate
