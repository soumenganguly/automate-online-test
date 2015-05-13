#!/usr/bin/python

import subprocess

#Installing Virtualenv
wget_call = subprocess.call("wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-12.1.1.tar.gz", shell=True)
if(wget_call==0):
    tar_call = subprocess.call("tar xf virtualenv-12.1.1.tar.gz", shell=True)
    if(tar_call==0):
        setup_call = subprocess.call("cd virtualenv-12.1.1 && sudo python setup.py install --quiet", shell=True)
        if(setup_call==0): #create and activate the virtualenv
                print "Successfully installed virtualenv"
                create_venv = subprocess.call(["virtualenv","online_test"])
                if(create_venv==0): #Install the dependencies inside the virtualenv"
                    print "Virtualenv created"
                    install_dep = subprocess.call("online_test/bin/easy_install --quiet git+https://github.com/FOSSEE/online_test.git#egg=django_exam-0.1 ", shell=True)
                    if(install_dep==0): #Create a django project
                        print "Dependencies installed"
                        subprocess.call("wget https://github.com/soumenganguly/online_test_starter_kit/archive/v1.0.zip ", shell=True)
                        subprocess.call("unzip v1.0.zip", shell=True)
                        sync_db = subprocess.call("online_test/bin/python online_test_starter_kit-1.0/manage.py syncdb", shell=True)
                        run_app = subprocess.call("online_test/bin/python online_test_starter_kit-1.0/manage.py runserver --verbosity=0", shell=True)
                        if(sync_db and run_app==0):
                            print "The online test interface is running, please point your browser to http://localhost:8000/exam"
                        else:
                            print "online test app failed to load"
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


