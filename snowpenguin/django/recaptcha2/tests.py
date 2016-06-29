import os

from django.forms import Form
from django.test import TestCase

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class RecaptchaTestForm(Form):
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget())


class TestRecaptchaForm(TestCase):
    def setUp(self):
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    def test_dummy_validation(self):
        form = RecaptchaTestForm({})
        self.assertTrue(form.is_valid())

    def test_dummy_error(self):
        del os.environ['RECAPTCHA_DISABLE']
        form = RecaptchaTestForm({})
        self.assertFalse(form.is_valid())

    def tearDown(self):
        if 'RECAPTCHA_DISABLE' in os.environ.keys():
            del os.environ['RECAPTCHA_DISABLE']
