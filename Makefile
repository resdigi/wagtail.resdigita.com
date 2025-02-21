venv:
	python -m venv venv
	echo "You MUST copy and paste as follows if you want an environment"
	echo "source ./venv/bin/activate"
	./venv/bin/pip install --upgrade pip

pip:
	make venv
	./venv/bin/pip install -r requirements.txt

update: 
	./venv/bin/python ./manage.py makemigrations
	./venv/bin/python ./manage.py migrate
	./venv/bin/python ./manage.py collectstatic --noinput

init:
	make update
	./venv/bin/python ./manage.py createsuperuser

runserver:
	./venv/bin/python ./manage.py runserver

start:
	make runserver

secretkey:
	./venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

collectstatic:
	./venv/bin/python ./manage.py collectstatic --noinput

# From https://tailwindcss.com/docs/installation/tailwind-cli
tailwindexe:
	wget https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 
	mv tailwindcss-linux-x64 venv/bin/tailwindcss
	chmod +x venv/bin/tailwindcss

# From https://tailwindcss.com/docs/installation/tailwind-cli
tailwindnpm:
	npm install tailwindcss @tailwindcss/cli

# From https://tailwindcss.com/docs/installation/tailwind-cli
tailwindcompile:
	npx @tailwindcss/cli -i ./tailwind/src/input.css -o ./wagtailresdigitacom/static/css/tailwind.css -m

tailwindcompilemax:
	npx @tailwindcss/cli -i ./tailwind/src/input.css -o ./wagtailresdigitacom/static/css/tailwind.css 

tailwindwatch:
	npx @tailwindcss/cli -i ./tailwind/src/input.css -o ./wagtailresdigitacom/static/css/tailwind.css --watch

fixtures-dump-test-initial:
	rm fixtures/*.json
	./venv/bin/python manage.py dumpdata  --natural-foreign wagtailcore.Locale	wagtailcore.Revision	wagtailcore.Page	wagtailcore.Site wagtailimages.Image 	wagtaildocs.Document 	base 	taggit 	blog 	project 	home 	wagtailresdigitacom  wagtailmenus > fixtures/test-initial.json
	mkdir -p fixtures/media/images
	mkdir -p fixtures/media/original_images
	cp -a fixtures/media/images/* media/images
	cp -a fixtures/media/original_images/* media/original_images

fixtures-load-test-initial:
	./venv/bin/python manage.py loaddata fixtures/test-initial.json
	cp -a fixtures/media/* media

