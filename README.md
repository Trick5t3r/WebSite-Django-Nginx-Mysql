# WebSite
A website for a completely classic school class coded in django-nginx 

# Table of contents
1. [Introduction](#introduction)
2. [Django installation](#Django)
3. [Nginx installation](#Nginx)
4. [Complements : le Siphoneur](#Siphoneur)

## Introduction <a name="introduction"></a>
The purpose of this repository is to help anyone create a website. In my case, I created a website for my class during my first year of preparatory class for the "grandes écoles", this class is called HX2. Hope this tutorial and my code helps you out, and if you have any questions or issues please feel free to contact me.

We will first see how to configure the site backend with django and then we will see how to configure nginx for the site frontend. 

## Django Installation <a name="Django"></a>
__1. Depedencies__

Installation of necessary packages 
```
pip3 install django 
pip3 install bootstrap4
pip3 install mysqlclient 
pip3 install django-widget-tweaks 
pip3 install django-cleanup
```

__2. Set up django__

__Dans le fichier settings__
   * change your secret key and put yours
```python
SECRET_KEY = 'YOUR_SECRET_KEY'
```
   * change allowed hosts
```python
ALLOWED_HOSTS = ['127.0.0.1', 'website.com']
```
   * Change the database and put the right information
```python
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hx2DB',
        'USER': 'hx2User',
        'PASSWORD' : 'VivelaHX2!',
        'HOST' : 'localhost',
        'PORT' : '3306',
    }
}
```

   * Change your language
```python
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
```

## Nginx <a name="Nginx"></a>

## Complements : le Siphoneur <a name="Siphoneur"></a>
