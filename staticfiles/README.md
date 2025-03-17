# Folder 'staticfiles'

This folder has static assets that are not in ./resdigita/static/ or in ./*/static/ where ./*/ are the referenced applications. It is an extra folder for static distribution-time files added to the `collectstatic` process. You may overload stuff here used by other apps, I think.



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
