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

## My Nixos Service Config

```nix
      systemd.services.wagtail-resdigita-com-main = {
        description = "wagtail.resdigita.com Website from main branch based on no template";
        after = [ "network.target" ];
        wantedBy = [ "multi-user.target" ];
        serviceConfig = {
          WorkingDirectory = "/home/wagtail/wagtail.resdigita.com.main/";
          ExecStart = ''/home/wagtail/wagtail.resdigita.com.main/.venv/bin/gunicorn --env WAGTAIL_ENV='production' --access-logfile /var/log/wagtail/wagtail-resdigita-com-main-access.log --error-logfile /var/log/wagtail/wagtail-resdigita-com-main-error.log --chdir /home/wagtail/wagtail.resdigita.com.main --workers 12 --bind 0.0.0.0:8903 settings.wsgi:application'';
          Restart = "always";
          RestartSec = "10s";
          EnvironmentFile = "/home/wagtail/wagtail.resdigita.com.main/.env";
          User = "wagtail";
          Group = "users";
        };
        unitConfig = {
          StartLimitInterval = "1min";
        };
      };
```