from django.forms.widgets import Widget

class ReCaptcha(Widget):
    def __init__(self, explicit=False, attrs={}, *args, **kwargs):
        super(ReCaptcha, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return data.get('g-recaptcha-response', None)
