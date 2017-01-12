# Django reCaptcha v2 [![Build Status](https://travis-ci.org/kbytesys/django-recaptcha2.svg?branch=master)](https://travis-ci.org/kbytesys/django-recaptcha2)
----

This integration app implements a recaptcha field for <a href="https://developers.google.com/recaptcha/intro">Google reCaptcha v2</a>
with explicit rendering and multiple recaptcha support.

----

## How to install

Install the required package from pip (or take the source and install it by yourself):

```bash
pip install django-recaptcha2
```

Then add django-recaptcha2 to your installed apps:

```python
INSTALLED_APPS = (
    ...
    'snowpenguin.django.recaptcha2',
    ...
)
```

And add your reCaptcha private and public key to your django settings.py:

```python
RECAPTCHA_PRIVATE_KEY = 'your private key'
RECAPTCHA_PUBLIC_KEY = 'your public key'
```

If you have to create the apikey for the domains managed by your django project, you can visit this <a href="https://www.google.com/recaptcha/admin">website</a>.

## Usage
### Form and Widget
You can simply create a reCaptcha enabled form with the field provided by this app:

```python
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class ExampleForm(forms.Form):
    [...]
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    [...]
```

You can pass some parameters into the widget contructor:

```python
class ReCaptchaWidget(Widget):
    def __init__(self, explicit=False, theme=None, type=None, size=None, tabindex=None, callback=None,
                 expired_callback=None, attrs={}, *args, **kwargs):
```

If you set the explicit boolean to true, you will render this field with explicit render support. This is usefull if you
want to use multiple forms with reCaptcha in one page. Take a look to template and samples sections for more info.

You can personalize reCaptcha theme, type, size, tabindex, callback and expired_callback parameters. Look the reCaptcha
<a href="https://developers.google.com/recaptcha/docs/display#config">documentation</a> if you want to change those values.
Warning: the app doesn't validate the incoming parameter values.

### Templating
You can use some template tags to simplify the reCaptcha adoption:
 
* recaptcha_init: add the script tag for reCaptcha api. You have to put this tag somewhere in your "head" element
* recaptcha_explicit_init: add the script tag for the reCaptcha api with explicit render support. You have to put this
  tag somewhere above the end of your "body" element. If you use this tag, you don't have to use "recaptcha_init".
* recaptcha_explicit_support: this tag add the callback function used by reCaptcha for explicit rendering. This tag also
  add some funcitions and javascript vars used by the ReCaptchaWidget when it is initialized with explicit=True. You have
  to put this tag somewhere in your "head" element.
* recaptcha_key: if you want to use reCaptcha manually in your template, you will need the sitekey (a.k.a. public api key).
  This tag returns a string with the configured public key.
  
You can use the form as usual.

### Force widget language
You can disable the language auto-detection in the recaptha2 init tag:

```django
{% load recaptcha2 %}
<html>
  <head>
      {% recaptcha_init 'es' %}
  </head>
```

or

```django
    </form>
    {% recaptcha_explicit_init 'es'%}
  </body>
</html>
```

For language codes take a look to <a href="https://developers.google.com/recaptcha/docs/language">this page</a>.

### Test unit support
You can't simulate api calls in your test, but you can disable the recaptcha field and let your test works.

Just set the RECAPTCHA_DISABLE env variable in your test:

```python
os.environ['RECAPTCHA_DISABLE'] = 'True'
```

Warning: you can use any word in place of "True", the clean function will check only if the variable exists.

## Samples
### Simple render example

Just create a form with the reCaptcha field and follow this template example:

```django
{% load recaptcha2 %}
<html>
  <head>
      {% recaptcha_init %}
  </head>
  <body>
    <form action="?" method="POST">
      {% csrf_token %}
      {{ form }}
      <input type="submit" value="Submit">
    </form>
  </body>
</html>
```

### Explicit render example

Create a form with explicit=True and write your template like this:

```django
{% load recaptcha2 %}
<html>
  <head>
    {% recaptcha_explicit_support %}
  </head>
  <body>
    <form action="?" method="POST">
      {% csrf_token %}
      {{ form }}
      <input type="submit" value="Submit">
    </form>
    {% recaptcha_explicit_init %}
  </body>
</html>
```

### Multiple render example

You can render multiple reCaptcha using only forms with explicit=True:

```django
{% load recaptcha2 %}
<html>
  <head>
      {% recaptcha_explicit_support %}
  </head>
  <body>
    <form action="{% url 'form1_post' %}" method="POST">
      {% csrf_token %}
      {{ form1 }}
      <input type="submit" value="Submit">
    </form>
    <form action="{% url 'form2_post' %}" method="POST">
      {% csrf_token %}
      {{ form2 }}
      <input type="submit" value="Submit">
    </form>
    {% recaptcha_explicit_init %}
  </body>
</html>
```

### Mix manual render with app support

You can use the app explicit render support also is you implement reCaptcha in one of your form in the template:

```django
{% load recaptcha2 %}
<html>
    <head>
        {% recaptcha_explicit_support %}
    </head>
    <body>
        [...]
        <div id='recaptcha'></div>
        <script>
            django_recaptcha_callbacks.push(function() {
                grecaptcha.render('recaptcha', {
                    'theme': 'dark',
                    'sitekey': '{% recaptcha_key %}'
                })
            });
        </script>
        [...]
        {% recaptcha_explicit_init %}
    </body>
</html>
```

### Test unit with recaptcha2 disabled
```python
import os
import unittest

from yourpackage.forms import MyForm

class TestCase(unittest.TestCase):
    def setUp(self):
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    def test_myform(self):
        form = MyForm({
            'field1': 'field1_value'
        })
        self.assertTrue(form.is_valid())

    def tearDown(self):
        del os.environ['RECAPTCHA_DISABLE']
```
