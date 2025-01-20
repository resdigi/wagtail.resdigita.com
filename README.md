# wagtail.resdigita.com

Wagtail Website for ResDigita.com

https://github.com/resdigi/wagtail.resdigita.com

The app name is `wagtailresdigitacom`. 

## Web access

| Site | URL |
| ---  | --- |
| Qualification | <https://wagtail.resdigita.com> |
| Localhost | <http://localhost:8000> |
| Qualification Admin | <https://wagtail.resdigita.com/admin> |
| Localhost | <http://localhost:8000/admin> |


| Username | Password |
| ---  | --- |
| admin | password |

## Makefile

Using `gnumake` from the command-line, here is how to get started :

```
make venv
make pip
make load-data
make start
```

and after initial data loaded :

`make start`


## Below is the standard content from Django Starter Template

The stack might be a little top-heavy:

* wagtail-news-template
* wagtail
* django
* python

By default, I use the sqlite database engine until we integrate SSO with key.resdigita.com. 

## Thoughts about developing strategy

Wagtail, as a Django app, integrates well with vanilla Django. As such, maybe let's develop our custom parts as Django apps without necessarily depending on 
Wagtail nor Wagtail-News-Template as in `wagtailresdigitacom`?

Here is a documentation page from Wagtail showing how to integrate Wagtail into an existing Django app, although our strategy may be to integrate distinct Django apps into Wagtail:

<https://docs.wagtail.org/en/stable/advanced_topics/add_to_django_project.html>

We could then integrate the development into the wagtail site. Just an idea.

The wagtail templates are in `templates/*.html`.

I think a lot of the look-and-feel comes from `tailwind.config.js`.

Not sure about `webpack.config.js`, maybe something to do with using the website as a web app.

I don't use `fly.toml`.

I don't use `gunicorn.conf.py` and configure gunicorn differently. `/home/wagtail/wagtail.resdigita.com/venv/bin/gunicorn --env WAGTAIL_ENV='production' --access-logfile /var/log/wagtail/wagtail-resdigita-com-access.log --error-logfile /var/log/wagtail/wagtail-resdigita-com-error.log --chdir /home/wagtail/wagtail.resdigita.com --workers 12 --bind 0.0.0.0:8902 wagtailresdigitacom.wsgi:application`

`Dockerfile` looks nice, but I don't use it either.

I do use the default setup of `sqlite`.

## Tailwind CSS

This came with wagtail-news-template. It seems to require `npm install` and  `npm run build:prod`. I added `tailwind-install` and `tailwind-compile` to the Makefile. 

Tailwind seems to take static files from `static_src` and put them into `static_compiled`. Django then takes `static_compiled` and puts it in to `static`.

For now, all static assets are at the root level. It would seem cleaner to me to have everything in the `wagtailresdigitacom` app.

## Decision not made : WAGTAIL-NEWS-TEMPLATE

I was surprised by looking into the Wagtail starter setups to find that there really isn't an empty template that pleased me. Consequentially, I decided to go with one that looked already pretty opinionated -- the Wagtail News Template -- but in reality, I think it is less opinionated than some of the stuff Torchbox (the company behind Wagtail) had produced otherwise. This works prette well.

Wagtail News Template is available here:

<https://github.com/torchbox/wagtail-news-template>


## Wagtail Starter Kit - Django Project Template

This Django project template is designed for creating Wagtail builds quickly, intended for developers to bootstrap their Wagtail site development using `wagtail start --template=`. The template comes with pre-defined pages, blocks, functionalities, and fixtures to streamline the initial setup process.

### Getting Started

1. **Check that you have an appropriate version of Python 3**  You want to make sure that you have a [compatible version](https://docs.wagtail.org/en/stable/releases/upgrading.html#compatible-django-python-versions) installed:

    ```sh
    python --version
    # Or:
    python3 --version
    # **On Windows** (cmd.exe, with the Python Launcher for Windows):
    py --version
    ```

2. **Create a Virtual Environment**: Set up a virtual environment to isolate your project dependencies. These instructions are for GNU/Linux or MacOS, but there are [other operating systems in the Wagtail docs](https://docs.wagtail.org/en/stable/getting_started/tutorial.html#create-and-activate-a-virtual-environment).

    ```bash
    python -m venv myproject/env
    source myproject/env/bin/activate
    ```

4. **Navigate to Project Directory**: Move into the newly created project directory.

    ```bash
    cd myproject
    ```

5. **Install Wagtail**: Install the Wagtail CMS package using pip.

    ```bash
    pip install wagtail
    ```

6. **Initialize Project**: Use the `wagtail start` command to create a new project based on the Wagtail Starter Kit template.

    ```bash
    wagtail start --template=https://github.com/torchbox/wagtail-news-template/archive/refs/heads/main.zip myproject .
    ```

7. **Install Project Dependencies**: Install the project's dependencies into a virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

All commands from now on should be run from inside the virtual environment.

8. **Load Dummy Data**: Load in some dummy data to populate the site with some content.

    ```bash
    make load-data
    ```

9. **Start the Server**: Start the Django development server.

    ```bash
    make start
    ```

10. **Access the Site and Admin**: Once the server is running, you can view the site at `localhost:8000` and access the Wagtail admin interface at `localhost:8000/admin`. Log in with the default credentials provided by :

    - Username: admin
    - Password: password

#### Deploying

Once you have your own copy of the template, you can extend and configure it however you like.

To get it deployed, follow the instructions below for your hosting provider of choice.

Don't see your preference here? Contributions are always welcome!

##### fly.io

Before you can deploy to [fly.io](https://fly.io/), you will need an account and the `fly` CLI tool will need to be [installed on your machine](https://fly.io/docs/flyctl/install/).

1. In the root directory of your project (the one with a `fly.toml` file), run `fly launch`
   1. When prompted about copying the existing `fly.toml` file to a new app, choose "Yes".

> [!CAUTION]
> Choosing "No" (the default) here will result in a broken deployment, as the `fly.toml` file requires configuration needed for the project to run correctly.

   2. When prompted about continuing the setup in the web UI, or tweak the generated settings, choose "No".
      1. The "Region" will be selected automatically. If you wish to change this, choose "Yes" instead, and modify the region in the browser.
2. Once the launch is successful, you'll need to [generate a secret key](https://realorangeone.github.io/django-secret-key-generator/)
   1. This can be done using `fly secrets set SECRET_KEY=<key>`, or through the web UI.
3. Finally (optional), load in the dummy data, to help get you started
   1. `fly ssh console -u wagtail -C "./manage.py load_initial_data"`

> [!NOTE]
> If you receive "error connecting to SSH server" when running the above command, It likely means the `fly.toml` above wasn't picked up correctly. Unfortunately, you'll need to delete your application and start again, resetting the changes to the `fly.toml` file.
> If the error still persists, check the application logs.

You can now visit your wagtail site at the URL provided by `fly`. We strongly recommend setting strong password for your user.

The database and user-uploaded media are stored in the attached volume. To save costs and improve efficiency, the app will automatically stop when not in use, but will automatically restart when the browser loads.

### Contributing

To customize this template, you can either make changes directly or backport changes from a generated project (via the `wagtail start` command) by following these steps:

1. Create a new project using the provided instructions in the [Getting Started](#getting-started) section.
2. Make changes within the new project.
3. Once you've completed your changes, you'll need to copy them over to the original project template, making sure to:

    3.1. Replace occurrences of `myproject` with `{{ project_name }}`

    3.2. Rename the project directory from `myproject` to `project_name` (without double curly brackets this time).

    3.3. Wrap template code (`.html` files under the templates directory), with a [verbatim tag](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#std-templatetag-verbatim) or similar [templatetag](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#templatetag) to prevent template tags being rendered on `wagtail start` ([see django's rendering warning](https://docs.djangoproject.com/en/5.0/ref/django-admin/#render-warning)).
5. Update compiled static assets using `npm run build:prod`.
6. Update fixtures using `make dump-data`

Make sure to test any changes by reviewing them against a newly created project, by following the [Getting Started](#getting-started) instructions again.


Happy coding with Wagtail! If you encounter any issues or have suggestions for improvement, feel free to contribute or open an issue.

## Configure .env in production

.env is used by our systemd service. 

```
ALLOWED_HOSTS="wagtail.resdigita.com"
CSRF_TRUSTED_ORIGINS="https://wagtail.resdigita.com,wagtail.resdigita.com"
SECRET_KEY=THE_VALUE_HERE_WITHOUT_QUOTES
```

SECRET_KEY can be obtained by `make secretkey` and is only required in production.

## Nixos configuration in production environment

I use Nixos for production. Below are extracts of our configuration environment.

```nix
{ config, pkgs, lib, ... }:
let
in
{
  containers.wagtail = {
    users.users.wagtail.uid = 1003;
    users.groups.wwwrun.gid = 54;
    users.groups.wwwrun.members = ["wagtail"];
    environment.systemPackages = with pkgs; [
        ((vim_configurable.override {  }).customize{
          name = "vim";
          vimrcConfig.customRC = ''
            " your custom vimrc
            set mouse=a
            set nocompatible
            colo torte
            syntax on
            set tabstop     =2
            set softtabstop =2
            set shiftwidth  =2
            set expandtab
            set autoindent
            set smartindent
            " ...
          '';
          }
        )
        python311
        python311Packages.pillow
        python311Packages.gunicorn
        python311Packages.pip
        libjpeg
        zlib
        libtiff
        freetype
        python311Packages.venvShellHook
        curl
        wget
        lynx
        dig    
        python311Packages.pylibjpeg-libjpeg
        git
        tmux
        bat
        cowsay
        lzlib
        killall
        pwgen
        python311Packages.pypdf2
        python311Packages.python-ldap
        python311Packages.pq
        python311Packages.aiosasl
        python311Packages.psycopg2
        gettext
        sqlite
        postgresql_14
        pipx
        gnumake
        poetry
        nodejs_22
        yarn
        jq
        ];
      nix.settings.experimental-features = "nix-command flakes";
      time.timeZone = "Europe/Amsterdam";
      system.stateVersion = "24.11";
    bindMounts = { 
      "/home/wagtail/wagtail.resdigita.com/media" = { 
        hostPath = "/var/www/wagtail.resdigita.com/media";
        isReadOnly = false; 
      }; 
      "/home/wagtail/wagtail.resdigita.com/static" = { 
        hostPath = "/var/www/wagtail.resdigita.com/static";
        isReadOnly = false; 
      }; 
    };
    systemd.services.wagtail-resdigita-com = {
      description = "wagtail.resdigita.com Website based on wagtail-news-starter";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        WorkingDirectory = "/home/wagtail/wagtail.resdigita.com/";
        ExecStart = ''/home/wagtail/wagtail.resdigita.com/venv/bin/gunicorn --env WAGTAIL_ENV='production' --access-logfile /var/log/wagtail/wagtail-resdigita-com-access.log --error-logfile /var/log/wagtail/wagtail-resdigita-com-error.log --chdir /home/wagtail/wagtail.resdigita.com --workers 12 --bind 0.0.0.0:8902 wagtailresdigitacom.wsgi:application'';
        Restart = "always";
        RestartSec = "10s";
        EnvironmentFile = "/home/wagtail/wagtail.resdigita.com/.env";
        User = "wagtail";
        Group = "users";
      };
      unitConfig = {
        StartLimitInterval = "1min";
      };
    };
  };
  services.nginx.virtualHosts = {
    "wagtail.resdigita.com"= {
      root = "/var/www/wagtail.resdigita.com/";
      locations."/" = {
        proxyPass = "http://127.0.0.1:8902/";
        extraConfig = nginxLocationWagtailExtraConfig;
      };
      enableACME=true;
      forceSSL = true;
      locations."/favicon.ico" = { proxyPass = null; };
      locations."/static" = { proxyPass = null; };
      locations."/media" = { proxyPass = null; };
      locations."/.well-known" = { proxyPass = null; };
    };
  };
  users = {
    users = {
        wagtail = {
            isNormalUser = true;
        };
    };
    groups = {
        
    };
  };
}
```
