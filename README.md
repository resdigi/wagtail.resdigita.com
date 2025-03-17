# Resdigita website recreation in Wagtail

Wagtail Website for ResDigita.com

<https://github.com/resdigi/wagtail.resdigita.com>

The main app name is `resdigita` and uses other apps `search`, `blog`, `project`, `base` and the python module `settings`. It makes use of gnumake with a Makefile. `resdigita` has a tailwind component to it accessible via the Makefiles, and a service to consume an external Ghost blog engine. 

Here are additional resources on this project:

- <https://task.lesgrandsvoisins.com/projects/62>
- <https://mark.lesgrandsvoisins.com/resdigita>


## Documentation

Here is our documentation

  - [Installation](./doc/installation.md)
  - [Fixtures (mainly initial data for now)](./doc/fixtures.md)
  - [Git (tips on our usage)](./doc/git.md)
  - [CHANGELOG](./CHANGELOG.md)
  - [Connected](./doc/connected.md)
  - [Architecture and thoughts about workflow](./doc/architecture.md)
  - [Nixos in production](./doc/nixos.md)
  - [Starter template standard documentation](./doc/starter.md)

## Web access to the application

| Site | URL |
| ---  | --- |
| Qualification | <https://wagtail.resdigita.com> |
| Qualification Admin | <https://wagtail.resdigita.com/admin> |
| Qualification OICD Admin | <https://wagtail.resdigita.com/accounts/oidc/key-resdigita-com/login/> |
| Localhost | <http://localhost:8000> |
| Localhost Admin | <http://localhost:8000/admin> |

| Username | Password |
| ---  | --- |
| admin | password |
