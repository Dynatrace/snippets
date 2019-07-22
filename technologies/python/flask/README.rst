Monitoring Flask application with Dynatrace
======

The basic blog app built in the Flask `tutorial <http://flask.pocoo.org/docs/tutorial/>`_ instrumented with `OneAgent SDK for Python <https://github.com/Dynatrace/OneAgent-SDK-for-Python>`_ for full stack monitoring in Dynatrace. The blog post `From monitoring to software intelligence for Flask applications <https://www.dynatrace.com/news/blog/monitoring-flask-applications>`_ describes this sample.

Disclaimer
-------

The contained code is considered educational and NOT SUPPORTED by Dynatrace.
Please use at your own risk. You can contact the author via Github issues.

Deploy Dynatrace OneAgent
-------

see `Dynatrace OneAgent documentation <https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/>`_

Install Flaskr
-------

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install Flaskr::

    $ pip install -e .

Or if you are using the master branch, install Flask from source before
installing Flaskr::

    $ pip install -e ../..
    $ pip install -e .


Run Flaskr
-------

::

    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
    > flask init-db
    > flask run

Open http://127.0.0.1:5000 in a browser.


Optional: compile and run the notification server (sample)
-------

The notification server is a simple Java HTTP server to showcase tracing outgoing web request from Python to Java.

Compile and run the sample notification server::

    $ cd ./sampleNotificationService 
    $ javac NotificationServer.java
    $ java NotificationServer

Optional: simulate load with Selenium
-------

The python package selenium is required::

    $ pip install selenium

Compile and run the sample notification server::

    $ cd ./scripts
    $ python flaskr_load_selenium.py
    


