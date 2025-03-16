dump-initial:
	rm *.json
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python $(PROJECT_PATH)manage.py dumpdata --natural-foreign wagtailcore.Locale wagtailcore.Revision wagtailcore.Page wagtailcore.Site wagtailimages.Image  wagtaildocs.Document base taggit blog project home resdigita wagtailmenus > $(PROJECT_PATH)fixtures/test-initial.json 
	mkdir -p $(PROJECT_PATH)fixtures/media/images
	mkdir -p $(PROJECT_PATH)fixtures/media/original_images
	cp -a $(PROJECT_PATH)media/images/* $(PROJECT_PATH)fixtures/media/images
	cp -a $(PROJECT_PATH)media/original_images/* $(PROJECT_PATH)fixtures/media/original_images

load-initial:
	$(EXEC_CMD) $(PROJECT_PATH).venv/bin/python $(PROJECT_PATH)manage.py loaddata $(PROJECT_PATH)fixtures/test-initial.json
	cp -a $(PROJECT_PATH)fixtures/media/* $(PROJECT_PATH)media