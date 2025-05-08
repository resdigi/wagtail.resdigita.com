# Loading environment variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

ifndef DOCKER_CONTAINER
	DOCKER_CONTAINER := web
endif

ifeq ($(USE_DOCKER),1)
	EXEC_CMD := docker-compose exec -ti $(DOCKER_CONTAINER)
	PROJECT_PATH := /home/wagtail/resdigita/
else
	EXEC_CMD := 
	PROJECT_PATH := ${dir ${abspath ${lastword ${MAKEFILE_LIST}}}}
endif

# Simplified env variables
ENV_EXISTS := $(wildcard ${PROJECT_PATH}.env)
VENV_EXISTS := $(wildcard ${PROJECT_PATH}.venv/)

initenv:
	mkdir -p static
	mkdir -p media 
ifneq (,$(ENV_EXISTS))
	$(error .env exists at $(ENV_EXISTS) please remove.)
endif
	cp example.env .env
	echo "MERCI DE CONFIGURER .env AVEC VOS VARIABLES D'ENVIRONNEMENT"

initvenv:
ifneq (,$(VENV_EXISTS))
	$(error venv exists at $(PROJECT_PATH).venv. please remove if you wish to recreate.)
endif
	echo "You MUST copy and paste as follows if you want an environment"
	echo "source ./venv/bin/activate"
	$(EXEC_CMD) python -m venv $(PROJECT_PATH).venv

messages:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python manage.py makemessages -l fr -l en 

# --ignore=manage.py --ignore=medias --ignore=setup.py --ignore=staticfiles --ignore=templates

sass:
	make -C $(PROJECT_PATH)/resdigita/tailwind install
	make -C $(PROJECT_PATH)/resdigita/tailwind compile
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python manage.py compilescss

init:
ifeq (,$(ENV_EXISTS))
	make initenv
	$(error .env required at $(ENV_PATH)  )
endif
ifeq (,$(VENV_EXISTS))
	make initvenv
endif
	make requirements
	make migrate
	make superuser
	make -C $(PROJECT_PATH)/resdigita init

requirements:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/pip install --upgrade pip
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/pip install -r $(PROJECT_PATH)/requirements.txt
	make -C ./resdigita requirements

superuser:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python manage.py createsuperuser --username admin --email admin@resdigita.com

makemigrations:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python ./manage.py makemigrations

migrate:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python ./manage.py migrate

produpdate:
	make collectstatic
	make migrate

update: 
	make sass
	make makemigrations
	make messages
	make produpdate

runserver:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python ./manage.py runserver $(HOST_NAME):$(HOST_PORT)

start:
	make runserver

secretkey:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

collectstatic:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python ./manage.py collectstatic --noinput

# From https://tailwindcss.com/docs/installation/tailwind-cli
tailwind-install-bin-linux:
	wget https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 
	mv tailwindcss-linux-x64 venv/bin/tailwindcss
	chmod +x venv/bin/tailwindcss

# From https://tailwindcss.com/docs/installation/tailwind-cli
tailwind-install:
	make -C resdigita/tailwind install

# From https://tailwindcss.com/docs/installation/tailwind-cli
tailwind-compile:
	make -C resdigita/tailwind compile
	make -C blog/tailwind compile

tailwind-compilemax:
	make -C resdigita/tailwind compile
	make -C blog/tailwind compile

tailwind-watch:
	make -C resdigita/tailwind watch
	make -C blog/tailwind watch

fixtures-dump-test-initial:
	make -C fixtures dump-initial

fixtures-load-test-initial:
	make -C fixtures load-initial

compilemessages:
	./.venv/bin/python manage.py compilemessages

makemessages:
	./.venv/bin/python manage.py  makemessages -l en -l fr
