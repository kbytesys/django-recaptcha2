from random import randint

from django import template
from django.conf import settings
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def recaptcha_key():
    return settings.RECAPTCHA_PUBLIC_KEY

def recaptcha_common_init(language, additional_variables):
    common_variables = {
        'language': language,
        'recaptcha_host': getattr(settings, 'RECAPTCHA_PROXY_HOST', 'https://google.com')    
    }
    common_variables.update(additional_variables)
    return common_variables


@register.inclusion_tag('snowpenguin/recaptcha/recaptcha_init.html')
def recaptcha_init(language=None):
    return recaptcha_common_init(language, {'explicit': False})


@register.inclusion_tag('snowpenguin/recaptcha/recaptcha_init.html')
def recaptcha_explicit_init(language=None):
    return recaptcha_common_init(language, {'explicit': True})


@register.inclusion_tag('snowpenguin/recaptcha/recaptcha_explicit_support.html')
def recaptcha_explicit_support():
    return {}


@register.inclusion_tag('snowpenguin/recaptcha/recaptcha_invisible_button.html')
def recaptcha_invisible_button(public_key=None, submit_label=None, extra_css_classes=None, form_id=None,
                               custom_callback=None):
    generated_id = '%s' % randint(10000, 99999)

    return {
        'generated_id': generated_id,
        'public_key': public_key or settings.RECAPTCHA_PUBLIC_KEY,
        'form_id': form_id,
        'submit_label': submit_label or _('Submit'),
        'extra_css_classes': extra_css_classes,
        'custom_callback': custom_callback
    }
