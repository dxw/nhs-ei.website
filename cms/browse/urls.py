from django.urls import path

from cms.browse import views

urlpatterns = [
    path("", views.browse, name="browse", kwargs={"section": None, "branch": None}),
    path("<section>/", views.browse, name="browse", kwargs={"branch": None}),
    path("<section>/<branch>/", views.browse, name="browse"),
]
