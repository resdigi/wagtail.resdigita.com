dump-initial:
	rm *.json
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python manage.py dumpdata  --natural-foreign wagtailcore.Locale wagtailcore.Revision wagtailcore.Page wagtailcore.Site wagtailimages.Image  wagtaildocs.Document base taggit blog project home resdigita wagtailmenus > test-initial.json 
	mkdir -p media/images
	mkdir -p media/original_images
	cp -a ../media/images/* media/images
	cp -a ../media/original_images/* media/original_images

load-initial:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python loaddata test-initial.json
	cp -a media/* ../media