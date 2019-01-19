# Django reCaptcha v2 [![Build Status](https://travis-ci.org/kbytesys/django-recaptcha2.svg?branch=master)](https://travis-ci.org/kbytesys/django-recaptcha2)
----

This integration app implements a recaptcha field for <a href="https://developers.google.com/recaptcha/intro">Google reCaptcha v2</a>
with explicit rendering and multiple recaptcha support. The invisible version of the reCAPTCHA with the automatic render mode
is now supported, please read the related documentation below.

Are you looking for the Google reCaptcha v3? Take a look to the dedicated repository https://github.com/kbytesys/django-recaptcha3

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
# If you require reCaptcha to be loaded from somewhere other than https://google.com
# (e.g. to bypass firewall restrictions), you can specify what proxy to use.
# RECAPTCHA_PROXY_HOST = 'https://recaptcha.net'
```

If you have to create the apikey for the domains managed by your django project, you can visit this <a href="https://www.google.com/recaptcha/admin">website</a>.

## "I'm not a robot" Usage 
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

You can set the private key on the "private_key" argument of the field contructor and you can pass some
parameters into the widget contructor:

```python
class ReCaptchaWidget(Widget):
    def __init__(self, explicit=False, container_id=None, theme=None, type=None, size=None, tabindex=None,
                 callback=None, expired_callback=None, attrs={}, *args, **kwargs):
```

If you set the explicit boolean to true, you will render this field with explicit render support. This is useful if you
want to use multiple forms with reCaptcha in one page. Take a look to template and samples sections for more info.

You can personalize reCaptcha theme, type, size, tabindex, callback and expired_callback parameters. Look the reCaptcha
<a href="https://developers.google.com/recaptcha/docs/display#config">documentation</a> if you want to change those values.
Warning: the app doesn't validate the incoming parameter values.

### Recaptcha "container id"
Now the default container id for the recaptcha is:

* recaptcha-{$fieldname} for the automatic rendering
* recaptcha-{$fieldname}-{%fiverandomdigits} for the explicit rendering

This avoids name collisions when you use multiple instances of the recaptcha in different forms, but in the same page
and with the same field name.

**Note:** you can always override the container id with the "container_id" argument in the widget constructor, but take
care: nobody will check if the id you provide is already used.

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

### Samples
#### Simple render example

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

#### Explicit render example

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

#### Multiple render example

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

#### Mix manual render with app support

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

## "Invisible" Usage
The implementation and the usage of this kind of binding is simpler and you don't need to use the explicit
rendering to add multiple instances of the reCAPTCHA.

### Form and Widget
You can simply create a reCaptcha enabled form with the field provided by this app:

```python
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaHiddenInput

class ExampleForm(forms.Form):
    [...]
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())
    [...]
```

You can set the private key on the "private_key" argument of the field contructor.

### Templating
You just need to add the "recaptcha_init" tag on the head of your page and to place the invisible reCAPTCHA
submit button inside your form:

```django
<form id='myform1' action="?" method="POST">
      {% csrf_token %}
      {{ form }}
      {% recaptcha_invisible_button submit_label='Submit' %}
</form>
```

You can customize the button with the parameters included in its definition:

```python
def recaptcha_invisible_button(public_key=None, submit_label=None, extra_css_classes=None,
                               form_id=None, custom_callback=None):
``` 

You can override the reCAPTCHA public key, change the label of the button, apply extra css classes, force
the button to submit a form identified by id or provide the name of a custom callback. Please check the samples
to understand how it works.

### Samples
#### Simple usage

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
      {% recaptcha_invisible_button submit_label='Submit' %}
    </form>
  </body>
</html>
```

**Note:** The button will looking for the first "form" element using che "Element.closest" function. IE
doesn't support it, so please use a polyfill (for example https://polyfill.io). If you don't want to
add extra javascript libraries, please use the form id or a custom callback.

#### Form id

```django
{% load recaptcha2 %}
<html>
  <head>
      {% recaptcha_init %}
  </head>
  <body>
    <form id='myform' action="?" method="POST">
      {% csrf_token %}
      {{ form }}
      {% recaptcha_invisible_button submit_label='Submit' form_id='myform' %}
    </form>
  </body>
</html>
```

#### Custom callback

```django
{% load recaptcha2 %}
<html>
  <head>
      {% recaptcha_init %}
  </head>
  <body>
    <form id='myform' action="?" method="POST">
      {% csrf_token %}
      {{ form }}
      {% recaptcha_invisible_button submit_label='Submit' custom_callback='mycallback' %}
      <script>
          function mycallback(token) {
              someFunction();
              document.getElementById("myform").submit();
          }
      </script>
    </form>
  </body>
</html>
```

### TODO/ISSUES

- Only the automatic binding is supported, but you can add the dummy widget inside your form and the required
javascript code in your template in order to use the programmatically bind and invoke.

- You can only configure one reCAPTCHA key in the configuration. This isn't a real problem because if you want 
to use the invisible reCAPTCHA you don't need to use the "old one" anymore. If you need to use both implementations you
can still set the public and private keys in the fields, tags and widgets constructors.

- ReCaptchaHiddenInput could be the starting point for the creation of some "I'm not a robot" reCAPTCHA template
tags to use in place of the ReCaptchaWidget (maybe in a future release)

## Testing
### Test unit support
You can't simulate api calls in your test, but you can disable the recaptcha field and let your test works.

Just set the RECAPTCHA_DISABLE env variable in your test:

```python
os.environ['RECAPTCHA_DISABLE'] = 'True'
```

Warning: you can use any word in place of "True", the clean function will check only if the variable exists.

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
