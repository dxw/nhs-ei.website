from django.utils.safestring import mark_safe

from wagtail.admin.ui.components import Component
from wagtail.core import hooks


class MySummaryItem:
    order = 50

    def __init__(self, request):
        pass

    def is_shown(self):
        return True

    def render_html(self, parent_context):
        return mark_safe("""
        <section class="panel summary nice-padding">
          <h3>No, but seriously -- welcome to the admin homepage.</h3>
        </section>
        """)


@hooks.register('construct_homepage_summary_items')
def add_another_welcome_panel(request, items):
    items.append(MySummaryItem())
