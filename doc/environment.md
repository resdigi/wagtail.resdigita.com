# Development environment

This page documents the **local developer environment** for `wagtail.resdigita.com`. It covers the three ways of provisioning the Python environment and the tooling available:

| Tool | File(s) | Purpose |
| --- | --- | --- |
| Makefile | `Makefile` (+ sub-`Makefile`s) | Original task runner (kept for compatibility) |
| Nix flake | `flake.nix`, `flake.lock` | Reproducible Python + toolchain shell |
| `just` | `.justfile` | Modern task runner, equivalent to the Makefile |

They are **not** mutually exclusive — pick whichever fits your workflow. The Nix flake provisions the Python environment; `just` (or `make`) drives the project tasks on top of it.

---

## Options for the Python environment

### 1. Native venv (classic, Makefile)

The original workflow uses a plain Python virtualenv and pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
(cd resdigita && pip install -r requirements.txt)
```

or via the Makefile fabric `make init` / `make requirements` (see [installation.md](./installation.md)).

### 2. Nix flake (recommended for Nix users)

`flake.nix` provides a `devShells.default` shell that:

- Uses **Python 3.11** (matching the production NixOS config in [nixos.md](./nixos.md)).
- **Automatically provisions `.venv`** on first `nix develop` and pip-installs both `requirements.txt` files, preserving the pinned versions.
- Ships the **native build toolchain** needed for the compiled Python extensions in this project:

  | Group | Packages |
  | --- | --- |
  | Compilers / build | `gcc`, `pkg-config`, `autoconf`, `automake`, `libtool` |
  | Rust (maturin wheels) | `rustc`, `cargo`, `maturin` |
  | CSS/CMake | `cmake`, `ninja` |
  | Image / native libs | `zlib`, `libjpeg`, `libwebp`, `libtiff`, `freetype`, `libheif`, `libffi`, `openssl` |
  | Tooling | `nodejs_22` (Tailwind), `gettext` (translations), `gnumake`, `sqlite` |

- Prefers prebuilt wheels (`PIP_PREFER_BINARY`), only falling back to source builds when no compatible wheel exists.

**Usage:**

```bash
nix develop            # first run provisions .venv and installs requirements
make runserver         # or: just runserver
```

> **Note:** the first `nix develop` downloads packages from PyPI (like the classic venv). The `flake.lock` pins `nixpkgs` to `nixos-24.11` (rev `50ab793786d9de88ee30ec4e4c24fb4236fc2674`). To move to a newer channel: `nix flake update`.

---

## Task runner: `just` vs `make`

A `.justfile` was added as a modern, self-contained equivalent of the Makefile. It reproduces every target and **inlines** the sub-`Makefile` commands (tailwind, fixtures), so `just` does not depend on `make` at all.

| `make` | `just` |
| --- | --- |
| `make initenv` | `just initenv` |
| `make initvenv` | `just initvenv` |
| `make requirements` | `just requirements` |
| `make makemigrations` | `just makemigrations` |
| `make migrate` | `just migrate` |
| `make superuser` | `just superuser` |
| `make messages` | `just messages` |
| `make compilemessages` | `just compilemessages` |
| `make makemessages` | `just makemessages` |
| `make collectstatic` | `just collectstatic` |
| `make secretkey` | `just secretkey` |
| `make runserver` | `just runserver` |
| `make start` | `just start` |
| `make sass` | `just sass` |
| `make tailwind-install-bin-linux` | `just tailwind-install-bin-linux` |
| `make tailwind-install` | `just tailwind-install` |
| `make tailwind-compile` | `just tailwind-compile` |
| `make tailwind-compilemax` | `just tailwind-compilemax` |
| `make tailwind-watch` | `just tailwind-watch` |
| `make fixtures-dump-test-initial` | `just fixtures-dump-test-initial` |
| `make fixtures-load-test-initial` | `just fixtures-load-test-initial` |
| `make init` | `just init` |
| `make produpdate` | `just produpdate` |
| `make update` | `just update` |

**Usage:**

```bash
just --list    # list all recipes
just runserver # run one
```

The `.justfile` honors the same environment convention as the Makefile:

- `USE_DOCKER=1` switches commands to `docker-compose exec -ti <container>` (default `web`).
- `HOST_NAME` / `HOST_PORT` control the dev server bind address.

The `Makefile` is intentionally kept for backward compatibility and is unchanged.

---

## Django Debug Toolbar configuration

The toolbar is gated by the `DEBUG_TOOLBAR` environment variable (default `True` in `example.env`).

In `settings/base.py`, `debug_toolbar` is added to `INSTALLED_APPS` and `MIDDLEWARE` **only when `DEBUG_TOOLBAR` is true**. `settings/urls.py` registers the toolbar URLs under the **same** condition.

> **Troubleshooting — `RuntimeError: Model class debug_toolbar.models.HistoryEntry ...`**
>
> This error occurs when `debug_toolbar.toolbar` is imported (e.g. from `urls.py`) while `debug_toolbar` is **not** present in `INSTALLED_APPS`. This used to happen because `urls.py` gated the toolbar on `settings.DEBUG` while `base.py` gated it on `DEBUG_TOOLBAR` — two conditions that can diverge.
>
> **Fix:** `settings/urls.py` now gates the toolbar import/registration on the same `DEBUG_TOOLBAR` toggle used in `settings/base.py`. If you change the toggle, keep the three places in sync:
>
> - `INSTALLED_APPS += ["debug_toolbar"]` in `settings/base.py`
> - `MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]` in `settings/base.py`
> - `urlpatterns += debug_toolbar_urls()` in `settings/urls.py`

---

## Summary of recent changes

- `flake.nix`, `flake.lock` — new reproducible Nix dev shell (Python 3.11 + native toolchain + venv provisioning).
- `.justfile` — new modern task runner, equivalent to and independent of the Makefile.
- `settings/urls.py` — fixed the Django Debug Toolbar `HistoryEntry` `RuntimeError` by aligning the URL gate with `DEBUG_TOOLBAR`.
