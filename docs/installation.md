# Installation


## Makefile

Using `make` (gnumake) from the command-line (see [Makefile](../Makefile)), here is how to get started :

```
make venv
make pip
make init
make fixtures-load-test-initial
make runserver
```

and after initial data loaded :

`make runserver`



## Configure .env in production

.env is used by our systemd service. 

```
ALLOWED_HOSTS="wagtail.resdigita.com"
CSRF_TRUSTED_ORIGINS="https://wagtail.resdigita.com,wagtail.resdigita.com"
SECRET_KEY=THE_VALUE_HERE_WITHOUT_QUOTES
```

SECRET_KEY can be obtained by `make secretkey` and is only required in production.

