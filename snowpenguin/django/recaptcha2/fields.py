import logging
import os

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import requests

logger = logging.getLogger(__name__)

class ReCaptchaField(forms.CharField):
    def __init__(self, attrs={}, *args, **kwargs):
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):

        # Disable the check if we run a test unit
        if os.environ.get('RECAPTCHA_DISABLE', None) is not None:
            return values[0]

        super(ReCaptchaField, self).clean(values[0])
        response_token = values[0]

        try:
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': response_token
                },
                timeout=5
            )
            r.raise_for_status()
        except requests.RequestException as e:
            logger.exception(e)
            raise ValidationError(
                _('Connection to reCaptcha server failed')
            )

        json_response = r.json()

        if bool(json_response['success']):
            return values[0]
        else:
            if 'error-codes' in json_response:
                if 'missing-input-secret' in json_response['error-codes'] or \
                        'invalid-input-secret' in json_response['error-codes']:

                    logger.exception('Invalid reCaptcha secret key detected')
                    raise ValidationError(
                        _('Connection to reCaptcha server failed')
                    )
                else:
                    raise ValidationError(
                        _('reCaptcha invalid or expired, try again')
                    )
            else:
                logger.exception('No error-codes received from Google reCaptcha server')
                raise ValidationError(
                    _('reCaptcha response from Google not valid, try again')
                )
