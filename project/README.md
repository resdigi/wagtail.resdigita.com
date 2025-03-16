# Application folder 'project'

Has details about different projects we manage.

```mermaid
---
title: wagtail.resdigita.com
---
classDiagram
  class settings
  
  

  namespace apps {

    class project {
        +ProjectPage()
        +ProjectIndexPage()
        +ProjectTagIndexPage()
    }

  }
  
```