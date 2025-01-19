venv:
	python -m venv venv
	echo "You MUST copy and paste as follows if you want an environment"
	echo "source ./venv/bin/activate"
	./venv/bin/pip install --upgrade pip

pip:
	./venv/bin/pip install -r requirements.txt

firstbareinstall:
	echo "This is only for documentation. The code is already generated"
	./venv/bin/
	for filename in .gitignore Makefile Dockerfile README.md .dockerignore .nvmrc requirements.txt ; do \
		echo $filename ; \
		mv $filename $filename.orig ; \
	done;
	./venv/bin/wagtail start --template=https://github.com/torchbox/wagtail-news-template/archive/refs/heads/main.zip wagtailresdigitacom .
	for filename in Makefile README.md ; do \
		echo $filename ; \
		cat $filename > $filename.new ; \
		echo "" >> $filename.new ; \
		cat $filename >> $filename.new ; \
		mv $filename.new $filename ; \
		rm $filename.orig ; \
	done 
	for filename in .gitignore Dockerfile  .dockerignore .nvmrc requirements.txt; do \
		echo $filename.orig ; \
		rm $filename.orig ; \
	done;

init: load-data start

start:
	./venv/bin/python ./manage.py runserver

load-data:
	./venv/bin/python ./manage.py createcachetable
	./venv/bin/python ./manage.py migrate
	./venv/bin/python ./manage.py load_initial_data
	./venv/bin/python ./manage.py collectstatic --noinput

dump-data:
	./venv/bin/python ./manage.py dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.rendition -e images.rendition -e sessions -e wagtailsearch.indexentry -e wagtailsearch.sqliteftsindexentry -e wagtailcore.referenceindex -e wagtailcore.pagesubscription > fixtures/demo.json

reset-db:
	rm -f db.sqlite3
	./venv/bin/python ./manage.py migrate
	./venv/bin/python ./manage.py load_initial_data

