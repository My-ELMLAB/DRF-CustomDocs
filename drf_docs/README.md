# Introduction
Since Django Rest Framework 3.9, CoreAPI is being deprecated and OpenAPI is going to replace the documentation generation together with Swagger-UI or ReDoc renderer implementations.

This package includes the bare basic templates extracted from the DRF documentation (https://www.django-rest-framework.org/topics/documenting-your-api/) as of July 2019. The AutoSchema class is overridden to include per-API description with multiline support.

# Installation
Install and upgrade the following packages with Pip:

```
djangorestframework >=3.9
pyyaml >= 5
django-filter >= 2.1
```

Copy the 'drf_docs' folder into your project root folder. Add 'drf_docs' to INSTALLED_APPS in settings.py.

```
INSTALLED_APPS = [
    ...
    'drf_docs',
]

```

Add the following to REST_FRAMEWORK under settings.py:

```
REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_docs.openapi.AutoDescribeSchema',
}
```

Add the following imports and paths to urls.py in the project folder:


```
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

if settings.DEBUG is True:
    urlpatterns.append(path('openapi/', get_schema_view(
        title='API documentation',
        permission_classes=[permissions.AllowAny],
        public=True,
    ), name='openapi-schema')),
    urlpatterns.append(path('docs/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
     )))
```