# WebSite
A website for a completely classic school class coded in django-nginx-mysql

# Table of contents
1. [Introduction](#introduction)
2. [Mysql Set Up](#Mysql)
3. [Django Set Up](#Django)
4. [Nginx Set Up](#Nginx)
5. [Usefull Additions](#Additions)
6. [Complements : le Siphoneur](#Siphoneur)

## Introduction <a name="introduction"></a>
The purpose of this repository is to help anyone create a website. In my case, I created a website for my class during my first year of preparatory class for the "grandes écoles", this class is called HX2. Hope this tutorial and my code helps you out, and if you have any questions or issues please feel free to contact me.

This whole tutorial was done with hx2 as the site name, so if you want to change it adapt the set of files provided accordingly. The server used was an ubuntu 20.04.

The structure of the site is simple: a home page (which in my case brings together school subjects), a presentation page of these sections with sub-sections, and finally a sub-sections page presenting the documents grouped by topic.

The administration pages reflect the same structure, and I added a custom filter for easier access to each subsection and documents (all this is discribe after)

There is a compartmentalization of users and files. Each file therefore belongs to a section which is attached to a compartment called here "Année". For a user to have access to this file, he must belong to a group with the same name as this "Année". A user can belong to several groups, so he can have access to several years. Finally, in my case, I had created 3 types of users, the Administrator with all the rights (in dango you can run the command ```python3 manage.py createsuperuser```), a user having only the right to consult the documents (you simply have to remove the access rights to the administrator interface, and give no permission) and a moderating user who had the right to access the administrator interface with the corresponding permissions and who could add files or sub-sections in the "Years" to which he belongs. 

Moreover, the management of the media is pretty simple, in the directory ```media``` there are two others subdirectories ```fichiersdeposes``` and ```static```.
* In ```static```, there are all the files necessary for the proper functioning of the site: style files and javascript files. (You can add your staticfiles with the command ```python3 manage.py collectstatic``` ). You can also put files used by your website that do not require the user to be logged in, for example your website logo. 
* In ```fichiersdeposes``` there are all the uploaded files (as the French name suggests). These files are accessible by following the partitioning explained previously. There is also a subdirectory ```permanent```. In this subdirectory you put all the files used by your website but which requires the user to be at least logged in. 

We will first see how to configure the site backend with django and then we will see how to configure nginx for the site frontend. 

## Mysql Set Up <a name="Mysql"></a>
If you don't want to set up mysql skip this section and adapt the settings file as explain after.

__1. Installation of Mysql__
```bash
sudo apt install mysql-server
```


## Django Set Up <a name="Django"></a>
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

Place the folder hx2 in the right directory

For the ubuntu 20 users, create a user "www-data" and a group "www-data" with the appropriate permissions

__The in the settings file__
   * change your secret key and put yours
```python
SECRET_KEY = 'YOUR_SECRET_KEY'
```
   * change allowed hosts
```python
ALLOWED_HOSTS = ['127.0.0.1', 'website.com']
```
   * Change the database and put the right information (create a database and a user dedicated to django )
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


__2. Set up gunicorn__
Edit the file ```gunicorn_start.sh```
* Put your own name
```python
NAME="hx2Site"                              #Name of the application (*)
```

* Adapt the two following line with your right absolut path
```python
DJANGODIR=/var/www/hx2/hx2Site/            # Django project directory (*)
SOCKFILE=/var/www/hx2/run/gunicorn.sock        # we will communicate using this unix socket (*)

```

* Adapt the usernam and the group name if you didn't create the same user as me (www-data)
```python
USER=www-data                                        # the user to run as (*)
GROUP=www-data                                     # the group to run as (*)
```
Save and exit the file

Copy the file ```gunicorn_hx2Site.service``` in ```/etc/systemd/system/```

Run the command ```service gunicorn_hx2Site start```

And normally you have finished installing your django server, it is operational. You can join it on the port 8000 in localhost or on your local network if you opened this port.

## Nginx Set Up <a name="Nginx"></a>

__1. Setup let's encrypt with OVH for https__
Install dependecies
```python
pip3 install certbot 
pip3 install certbot-dns-ovh
```

Create the config file at ```/etc/logrotate.d/cerbot``` with:
```
/var/log/letsencrypt/*.log {
        monthly
        rotate 6
        compress
        delaycompress
        notifempty
        missingok
        create 640 root adm
}
```

Create the API
```
GET /domain/zone/
GET: /domain/zone/{domain.name}/
GET /domain/zone/{domain.ext}/status
GET /domain/zone/{domain.ext}/record
GET /domain/zone/{domain.ext}/record/*
POST /domain/zone/{domain.ext}/record
POST /domain/zone/{domain.ext}/refresh
DELETE /domain/zone/{domain.ext}/record/*
```

Connect to https://api.ovh.com/createToken/ to get the rigth information access for your API

Create ```/root/.ovhapi``` and add:
```
dns_ovh_endpoint = ovh-eu
dns_ovh_application_key = YOUR_APPLICATION_KEY
dns_ovh_application_secret = YOUR_SECRET
dns_ovh_consumer_key = YOUR_PERSONAL_KEY
```

```
chmod 600 /etc/certs/.ovhapi
```

Generate the certificate for your ```website.com``` and ```*.website.com```, they are two separate certificates but they will be put in the same file.
```
sudo certbot certonly --dns-ovh --dns-ovh-credentials /etc/certs/.ovhapi -d website.com -d *.website.com
```

You can do in several steps to get the two certifiactes in two different files with 
```
certbot certonly --dns-ovh --dns-ovh-credentials ~/.ovhapi -d *.website.com
```
Or make it automatically with no interaction with
```
certbot certonly --dns-ovh --dns-ovh-credentials ~/.ovhapi --non-interactive --agree-tos --email mon@email.fr -d website.com -d *.website.com
```

Then
```
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

When the certificates will expire run ```certbot renew``` to genrate new ones.

__2. Nginx installation__

```
sudo apt-get update
sudo apt-get -y install nginx

sudo service nginx restart
```
Put my nginx file in ```/etc/nginx/sites-available/website.com``` and make 
```sudo ln -s /etc/nginx/sites-available/website.com /etc/nginx/sites-enabled/```

Finally
```/sudo systemctl restart nginx```

NB : 
* ```/etc/nginx/nginx.conf``` is the main configuration file, you can modify its properties to suit your requirements 
* ```/var/log/nginx/access.log``` Nginx save all the access demand
* ```/var/log/nginx/error.log``` is the file where Nginx save all the errors

To check if a certificate is correct you can use "Online Certificate Status Protoocl (OCSP)"
Run ```openssl s_client -connect website.com:443 -tls1_2 -tlsextdebug -status | grep "OCSP Response Status: successful" ```
And ```openssl s_client -showcerts -connect website.com:443 -tls1_2 -tlsextdebug -status | grep "OCS" ```

## Useful additions  <a name="Additions"></a>

Explains tamplatags, templates base, dictioary, the document access system  ...

__ Useful commands __ 
* ```python python3 manage.py runserver``` with ```python 0.0.0.0``` to listen on all interface, ```python --insecure``` (but dangerous)
* ```python python3 manage.py makemigrations``` and ```python python3 manage.py migrate```
* ```python python3 manage.py shell```
* ```python python3 manage.py runscript``` (but requires configurations so prefer the method that I use in "le siphoneur")


## Complements : le Siphoneur <a name="Siphoneur"></a>
The "Siphoneur" aims to siphon a main directory with the same structure as the site and to put all the documents directly on the website automatically. 
Change the absolute path or remove the ```#``` to take the path as argument
```python
#walk_dir = sys.argv[1]
walk_dir = "/path/to/the/folder/to/siphon/"
```

Run the command

```python
python3 siphoneur.py
```
