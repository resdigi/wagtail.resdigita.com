# Python Module Folder 'settings'

This folder, referenced by manage.py, is the entry to the application.

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