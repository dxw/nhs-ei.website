from django.urls import path

from cms.browse import views

urlpatterns = [
    path("", views.browse, name="browse"),
    path("<section>/", views.browse_branch, name="browse_branch"),
    path("<section>/<branch>", views.browse_leaf, name="browse_leaf"),
]
