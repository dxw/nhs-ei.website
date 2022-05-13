# Generated by Django 3.1.13 on 2021-08-25 11:03

import cms.categories.blocks
from django.db import migrations
import wagtail.blocks
import wagtail.blocks.field_block
import wagtail.fields
import wagtail.images.blocks
import wagtailnhsukfrontend.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210812_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Base')), ('care_card', wagtail.blocks.StructBlock([('type', wagtail.blocks.ChoiceBlock(choices=[('primary', 'Non-urgent'), ('urgent', 'Urgent'), ('immediate', 'Immediate')])), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=4.', max_value=6, min_value=2, required=True)), ('title', wagtail.blocks.CharBlock(required=True)), ('body', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.RichTextBlock()), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('body', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.RichTextBlock()), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))])), ('image', wagtail.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.blocks.CharBlock(required=False))])), ('feature_card', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))]))], required=True))])), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))])), ('image', wagtail.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.blocks.CharBlock(required=False))])), ('feature_card', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))]))], required=True))], group='Base')), ('details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('body', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.RichTextBlock()), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))])), ('image', wagtail.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.blocks.CharBlock(required=False))])), ('feature_card', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))]))], required=True))], group='Base')), ('do_list', wagtail.blocks.StructBlock([('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('label', wagtail.blocks.CharBlock(help_text='Adding a label here will overwrite the default of Do', label='Heading', required=False)), ('do', wagtail.blocks.ListBlock(wagtail.blocks.field_block.RichTextBlock))], group='Base')), ('dont_list', wagtail.blocks.StructBlock([('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('label', wagtail.blocks.CharBlock(help_text="Adding a label here will overwrite the default of Don't", label='Heading', required=False)), ('dont', wagtail.blocks.ListBlock(wagtail.blocks.field_block.RichTextBlock, label="Don't"))], group='Base')), ('expander', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('body', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.RichTextBlock()), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))])), ('image', wagtail.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.blocks.CharBlock(required=False))])), ('feature_card', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))]))], required=True))], group='Base')), ('expander_group', wagtail.blocks.StructBlock([('expanders', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.ExpanderBlock))], group='Base')), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Base')), ('image', wagtail.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.blocks.CharBlock(required=False))], group='Base')), ('panel', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))], group='Base')), ('panel_list', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.blocks.StreamBlock([('card_basic', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))]))], required=True))], group='Base')), ('warning_callout', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.blocks.RichTextBlock(required=True))], group='Base')), ('summary_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))], group='Base')), ('promo', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))], group='Base')), ('promo_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.blocks.StreamBlock([('card_basic', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))]))], required=True))], group='Base')), ('recent_posts', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('type', wagtail.blocks.MultipleChoiceBlock(choices=[('post', 'Post'), ('blog', 'Blog'), ('publication', 'Publications'), ('all', 'All')], help_text='All will get all pages that can have categories, regardless of other choices')), ('category', cms.categories.blocks.CategoryBlock(help_text='You may limit results to a single category', required=False)), ('num_posts', wagtail.blocks.IntegerBlock(default=10, help_text='How many pages to show')), ('see_all_link', wagtail.blocks.BooleanBlock(blank=True, default=True, help_text='Link to full category page?', required=False))], group='Custom')), ('text', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'], group='Custom', help_text='\n            Use this block to add formatted text into a page e.g.\n            paragraph with heading and/or links and images\n        ', template='blocks/text_block.html')), ('html', wagtail.blocks.RawHTMLBlock(group='custom', help_text='\n            Use this block to add raw html\n        ', template='blocks/html_block.html'))], blank=True),
        ),
    ]
