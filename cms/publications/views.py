from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from django_weasyprint import WeasyTemplateView


class PublicationPdfView(WeasyTemplateView):

    template_name = "publications/publication_pdf.html"

    pdf_stylesheets = [
        settings.BASE_DIR / "cms/static_compiled/css/publication_pdf.css",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_pdf_filename(self):
        return "{slug}_{date}.pdf".format(
            slug=slugify(self.kwargs["publication"].title),
            date=self.kwargs["publication"].latest_revision_created_at.strftime(
                "%Y-%m-%d"
            ),
        )

    pdf_attachment = True
