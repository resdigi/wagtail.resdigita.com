# Folder 'docs'

This has the documentation for wagtail.resdigita.com. See [../README.md](../README.md) for a more concise introduction.

```mermaid
---
title: wagtail.resdigita.com
---
flowchart LR

base
blog
docs
fixtures
home
locale
media
project
resdigita
search
settings -- apps --> base & blog & home & project & resdigita & search
base & blog & home & project & resdigita -- static --> static
staticfiles --> static
static
staticfiles

```