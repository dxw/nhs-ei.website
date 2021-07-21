from django.urls import path

from cms.categories import views

urlpatterns = [
    path("", views.CategoryListView.as_view()),
    path("<slug:slug>", views.CategoryDetailView.as_view(), name="category-detail"),
]
