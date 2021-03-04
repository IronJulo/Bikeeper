
# Templates

Templates allow us to generate HTML dynamically (serverside). 
A `base.html` template define the global structure off our website. 
All the other templates extends base.html. In this way we don't need to import css or scripts files on each pages. 

?> **Tip** Define here the main structure
```html
<!doctype html>
<html>

<head>
    {% block title %}{{ title }}{% endblock %}
    <link rel="stylesheet" href="{{ url_for('static', filename='pc/css/base.css')}}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='pc/assets/favicon.ico')}}" />
    {% block style %}{% endblock %}
</head>

<body>

{% block header %}
    {% include "components/header.html" %}
{% endblock %}

{% block sidebar %}
    {% include "components/sidebar.html" %}
{% endblock %}

<main>
    <div>
        {% block main %} {% endblock %}
    </div>
</main>


<script src="https://code.jquery.com/jquery-3.5.1.js"></script>
<script src="{{ url_for('static', filename='pc/js/sidebar.js') }}"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>
{% block script %}{% endblock %}

</body>

</html>
```

```html
{% extends "base.html" %}

{% block style %}
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='pc/css/device.css') }}">
{% endblock style %}

{% block main %}
<div class="flex">
    <section>
        <div class="flash">
```
?> **Tip** `{% extends "base.html" %}` to refer to base.html 

!> **Important** All code placed into a block will be automatically written in base.html block.

## Jinja2 templating

We use Jinja templating when it is possible. 

In this exemple we get the value `selected_device` sended by python to this template, and write it in html
```html
<div class="flash">
    {% include "messages.html" %}
</div>
<h1>Your Device ({{selected_device}})</h1>
```

?> **Tip** `{% include "messages.html" %}` is to call an other html page inside this one. 