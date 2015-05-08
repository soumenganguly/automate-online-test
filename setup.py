#! /usr/bin/python

import subprocess
import os
import sys
import re
pwd = os.getcwd()
sys.path.append(pwd+'/django_online_test/django_online_test')

def manipulate_settings():
    import settings
    new_file = open("django_online_test/django_online_test/new_settings.py","a")

    new_file.write("import os")
    new_file.write("\n\n")

    new_file.write("BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))")
    new_file.write("\n\n")

    new_file.write("SECRET_KEY = '%s'"%(settings.SECRET_KEY))
    new_file.write("\n\n")

    new_file.write("DEBUG = %s"%(settings.DEBUG))
    new_file.write("\n\n")

    new_file.write("ALLOWED_HOSTS = %s"%(settings.ALLOWED_HOSTS))
    new_file.write("\n\n")

    new_file.write("TEMPLATE_DEBUG = %s"%(settings.TEMPLATE_DEBUG))
    new_file.write("\n\n")

    new_file.write("AUTH_PROFILE_MODULE = 'exam.Profile'")
    new_file.write("\n\n")

    test_apps = ('testapp.exam','taggit','taggit_autocomplete_modified',)
    default_apps = settings.INSTALLED_APPS
    online_test_app = default_apps.__add__(test_apps)
    comma_append = re.sub('\)',',)',str(online_test_app))
    new_file.write("INSTALLED_APPS = %s"%(comma_append))
    new_file.write("\n\n")
    
    new_file.write("MIDDLEWARE_CLASSES = %s"%(str(settings.MIDDLEWARE_CLASSES)))
    new_file.write("\n\n")

    new_file.write("ROOT_URLCONF = '%s'"%(settings.ROOT_URLCONF))
    new_file.write("\n\n")

    new_file.write("WSGI_APPLICATION = '%s'"%(settings.WSGI_APPLICATION))
    new_file.write("\n\n")

    new_file.write("DATABASES = %s"%(settings.DATABASES))
    new_file.write("\n\n")

    new_file.write("LANGUAGE_CODE = '%s'"%(settings.LANGUAGE_CODE))
    new_file.write("\n\n")

    new_file.write("TIME_ZONE = '%s'"%(settings.TIME_ZONE))
    new_file.write("\n\n")

    new_file.write("USE_I18N = %s"%(settings.USE_I18N))
    new_file.write("\n\n")

    new_file.write("USE_L10N = %s"%(settings.USE_L10N))
    new_file.write("\n\n")


    new_file.write("STATIC_URL = '%s'"%(settings.STATIC_URL))
    new_file.write("\n\n")

    new_file.close()


def manipulate_urls():
    new_urls_file = open("django_online_test/django_online_test/new_urls.py","a")

    new_urls_file.write("from django.conf.urls import patterns, include, url")
    new_urls_file.write("\n\n")

    new_urls_file.write("from django.contrib import admin")
    new_urls_file.write("\n")

    new_urls_file.write("admin.autodiscover")
    new_urls_file.write("\n\n")

    new_urls_file.write("urlpatterns = patterns('', url(r'^admin/', include(admin.site.urls)), url(r'^exam/', include('testapp.exam.urls')), url(r'^taggit_autocomplete_modified/', include('taggit_autocomplete_modified.urls')))")

    new_urls_file.close()
    

#Installing Virtualenv
wget_call = subprocess.call("wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-12.1.1.tar.gz", shell=True)
if(wget_call==0):
    tar_call = subprocess.call("tar xf virtualenv-12.1.1.tar.gz", shell=True)
    if(tar_call==0):
        setup_call = subprocess.call("cd virtualenv-12.1.1 && sudo python setup.py install", shell=True)
        if(setup_call==0): #create and activate the virtualenv
                print "Successfully installed virtualenv"
                create_venv = subprocess.call(["virtualenv","online_test"])
                if(create_venv==0): #Install the dependencies inside the virtualenv"
                    print "Virtualenv created"
                    install_dep = subprocess.call("online_test/bin/easy_install git+https://github.com/FOSSEE/online_test.git#egg=django_exam-0.1", shell=True)
                    if(install_dep==0): #Create a django project
                        print "Dependencies installed"
                        create_project = subprocess.call("online_test/bin/django-admin.py startproject django_online_test", shell=True)
                        if(create_project==0):
                            print "Online test project created"
                            
                            #Manipulate the project settings
                            subprocess.call("touch django_online_test/django_online_test/new_settings.py", shell=True)
                            manipulate_settings()
                            subprocess.call("rm django_online_test/django_online_test/settings.py", shell=True)
                            new_settings = subprocess.call("mv django_online_test/django_online_test/new_settings.py django_online_test/django_online_test/settings.py", shell=True)
                            
                            #Manipulate URL's
                            subprocess.call("touch django_online_test/django_online_test/new_urls.py", shell=True)
                            manipulate_urls()
                            subprocess.call("rm django_online_test/django_online_test/urls.py", shell=True)
                            new_urls = subprocess.call("mv django_online_test/django_online_test/new_urls.py django_online_test/django_online_test/urls.py", shell=True)
                            if(new_settings==0 and new_urls==0): #Running the application on localhost
                                sync_db = subprocess.call("online_test/bin/python django_online_test/manage.py syncdb", shell=True)
                                run_app = subprocess.call("online_test/bin/python django_online_test/manage.py runserver", shell=True)
                                if(sync_db and run_app==0):
                                    print "The online test interface is running, please point your browser to http://localhost:8000/exam"
                                else:
                                    print "online test app failed to load"
                            else:
                                print "The project setting's could not be altered"
                        else:
                            print "online test project creation failed"
                    else:
                        print "Dependencies could not be installed"
                else:
                    print "Virtualenv creation failed"
        else:
            print "Could not install virtualenv"
    else:
        print "tar call failed"
else:
    print "wget call failed"

