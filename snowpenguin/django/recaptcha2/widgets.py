from random import randint

from django.conf import settings
from django.forms.widgets import Widget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


class ReCaptchaWidget(Widget):
    def __init__(self, explicit=False, container_id=None, theme=None, type=None, size=None, tabindex=None,
                 callback=None, expired_callback=None, public_key=None, attrs={}, *args, **kwargs):
        super(ReCaptchaWidget, self).__init__(*args, **kwargs)
        self.container_id = container_id
        self.explicit = explicit
        self.theme = theme
        self.type = type
        self.size = size
        self.tabindex = tabindex
        self.callback = callback
        self.expired_callback = expired_callback
        self.attrs = attrs
        self._public_key = public_key

    def render(self, name, value, attrs=None, *args, **kwargs):
        template = 'snowpenguin/recaptcha/'
        template += 'recaptcha_explicit.html' if self.explicit else 'recaptcha_automatic.html'

        if self.container_id:
            container_id = self.container_id
        else:
            # this avoids name collisions when you use multiple recaptcha in the same page with the same field name
            container_id = 'recaptcha-%s-%s' % (name, randint(10000, 99999)) if self.explicit else 'recaptcha-%s' % name

        return mark_safe(
            render_to_string(template, {
                'container_id': container_id,
                'public_key': self._public_key or settings.RECAPTCHA_PUBLIC_KEY,
                'theme': self.theme,
                'type': self.type,
                'size': self.size,
                'tabindex': self.tabindex,
                'callback': self.callback,
                'expired_callback': self.expired_callback
            })
        )

    def value_from_datadict(self, data, files, name):
        return [data.get('g-recaptcha-response', None)]


class ReCaptchaInvisibleWidget(Widget):
    def __init__(self, public_key=None, submit_label=_('Submit'), extra_css_classes=None, form_id=None, attrs={},
                 *args, **kwargs):
        super(ReCaptchaInvisibleWidget, self).__init__(*args, **kwargs)
        self.attrs = attrs
        self._public_key = public_key
        self.submit_label = submit_label
        self.extra_css_classes = extra_css_classes
        self.form_id = form_id

    def render(self, name, value, attrs=None, *args, **kwargs):
        template = 'snowpenguin/recaptcha/recaptcha_invisible_automatic.html'

        generated_id = '%s' % randint(10000, 99999)

        return mark_safe(
            render_to_string(template, {
                'generated_id': generated_id,
                'public_key': self._public_key or settings.RECAPTCHA_PUBLIC_KEY,
                'form_id': self.form_id,
                'submit_label': self.submit_label,
                'extra_css_classes': self.extra_css_classes
            })
        )

    def value_from_datadict(self, data, files, name):
        return [data.get('g-recaptcha-response', None)]
