from django.urls import path

from cms.browse import views

urlpatterns = [
    path("", views.browse, name="browse", kwargs={"programme": None, "branch": None}),
    path("<programme>/", views.browse, name="browse", kwargs={"branch": None}),
    path("<programme>/<branch>/", views.browse, name="browse"),
]
