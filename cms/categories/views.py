from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cms.categories.models import Category, CategoryPage


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["self"] = {"title": "All categories"}
        return context


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pages = CategoryPage.objects.live()
        category = context["object"]
        pages = pages.filter(categorypage_category_relationship__category=category)
        ordered_pages = pages.order_by("-latest_revision_created_at")
        page_data = [
            {
                "record": page,
                "tag": page.specific._meta.verbose_name.title(),
                "date": page.latest_revision_created_at,
            }
            for page in ordered_pages
        ]
        context["category_pages"] = page_data

        pages.filter(categorypage_category_relationship__category=context["object"])

        return context
