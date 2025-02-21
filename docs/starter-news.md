# Alternative branch News

There is a separate starter template `wagtail-news-template` on the branch `news` ([news branch on github.com](https://github.com/resdigi/wagtail.resdigita.com/tree/news)). This `main` is from the branch `notemplate`. 

I was surprised by looking into the Wagtail starter setups to find that there really isn't an empty template that pleased me. Consequentially, I decided to go with one that looked already pretty opinionated -- the Wagtail News Template -- but in reality, I think it is less opinionated than some of the stuff Torchbox (the company behind Wagtail) had produced otherwise. This works pretty well.

Wagtail News Template is available here:

<https://github.com/torchbox/wagtail-news-template>

**I am not happy with WAGTAIL-NEWS-TEMPLATE!** This is not a blog out-of-the-box. I tried writing an article and can't add images !

<https://wagtailnews.resdigita.com/blog/digital-human/>

Maybe continue with ghost integration only for article composition?

Here are additional things in the wagtail-news-template: 

I think a lot of the look-and-feel comes from `tailwind.config.js`.

Not sure about `webpack.config.js`, maybe something to do with using the website as a web app.

I don't use `fly.toml`.

I don't use `gunicorn.conf.py` and configure gunicorn differently. `/home/wagtail/wagtail.resdigita.com/venv/bin/gunicorn --env WAGTAIL_ENV='production' --access-logfile /var/log/wagtail/wagtail-resdigita-com-access.log --error-logfile /var/log/wagtail/wagtail-resdigita-com-error.log --chdir /home/wagtail/wagtail.resdigita.com --workers 12 --bind 0.0.0.0:8902 wagtailresdigitacom.wsgi:application`

`Dockerfile` looks nice, but I don't use it either.

TailwindCSS.

## Tailwind CSS

This came with wagtail-news-template. It seems to require `npm install` and  `npm run build:prod`. I added `tailwind-install` and `tailwind-compile` to the Makefile. 

Tailwind seems to take static files from `static_src` and put them into `static_compiled`. Django then takes `static_compiled` and puts it in to `static`.

For now, all static assets are at the root level. It would seem cleaner to me to have everything in the `wagtailresdigitacom` app.

