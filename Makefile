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

start:
	./venv/bin/python ./manage.py runserver

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

fixturesdump:
	rm fixtures/*.json
	./venv/bin/python manage.py dumpdata  --natural-foreign wagtailcore.Locale wagtailcore.Revision > fixtures/00_locales.json
	./venv/bin/python manage.py dumpdata  --natural-foreign wagtailcore.Page > fixtures/01_pages.json
	./venv/bin/python manage.py dumpdata  --natural-foreign wagtailimages.Image > fixtures/02_images.json
	./venv/bin/python manage.py dumpdata  --natural-foreign wagtaildocs.Document > fixtures/03_documents.json
	./venv/bin/python manage.py dumpdata  --natural-foreign base > fixtures/04_base.json
	./venv/bin/python manage.py dumpdata  --natural-foreign taggit > fixtures/05_taggit.json
	./venv/bin/python manage.py dumpdata  --natural-foreign blog.Author blog.BlogPage blog.BlogPageGalleryImage blog.BlogIndexPage blog.BlogPageTag blog.BlogTagIndexPage  > fixtures/06_blog.json
	./venv/bin/python manage.py dumpdata  --natural-foreign project.ProjectIndexPage project.ProjectPage project.ProjectPageTag > fixtures/07_projects.json
	./venv/bin/python manage.py dumpdata  --natural-foreign home > fixtures/08_home.json
	./venv/bin/python manage.py dumpdata  --natural-foreign wagtailresdigitacom > fixtures/09_wagtailresdigitacom.json
	./venv/bin/python manage.py dumpdata  --natural-foreign wagtailmenus > fixtures/10_wagtailmenus.json

fixturesload:
	./venv/bin/python manage.py loaddata fixtures/*.json
	cp -a fixtures/media/* media

