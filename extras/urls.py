
from django.urls import path,include
from .views import BannerListView,AnnouncementListView

urlpatterns = [
path('banners/', BannerListView.as_view()),
path('announcements/', AnnouncementListView.as_view()),
]2025-07-02 04:33:41 |   File "/usr/local/lib/python3.10/site-packages/django/urls/resolvers.py", line 666, in resolve
2025-07-02 04:33:41 |     for pattern in self.url_patterns:
2025-07-02 04:33:41 |   File "/usr/local/lib/python3.10/site-packages/django/utils/functional.py", line 47, in __get__
2025-07-02 04:33:41 |     res = instance.__dict__[self.name] = self.func(instance)
2025-07-02 04:33:41 |   File "/usr/local/lib/python3.10/site-packages/django/urls/resolvers.py", line 718, in url_patterns
2025-07-02 04:33:41 |     patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
2025-07-02 04:33:41 |   File "/usr/local/lib/python3.10/site-packages/django/utils/functional.py", line 47, in __get__
2025-07-02 04:33:41 |     res = instance.__dict__[self.name] = self.func(instance)
2025-07-02 04:33:41 |   File "/usr/local/lib/python3.10/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
2025-07-02 04:33:41 |     return import_module(self.urlconf_name)
2025-07-02 04:33:02 | [2025-07-02 04:33:02 +0330] [71] [INFO] Booting worker with pid: 71