# -*- coding: utf-8 -*-
#
# Copyright 2019 Dynatrace LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

''' App Creation
'''

import os
import logging
import atexit

from flask import Flask
from flaskr import dynatrace
from flaskr.dynatrace_middleware import DynatraceWSGIMiddleware

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    # initialize the OneAgent Python SDK
    if dynatrace.sdk_init():
        atexit.register(dynatrace.sdk_shutdown)

    # create the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Do this after configuration is applied
    app.wsgi_app = DynatraceWSGIMiddleware(
        app.wsgi_app, app.name,
        virtual_host=app.config.get('SERVER_NAME'),
        context_root=app.config.get('APPLICATION_ROOT'))
    app.before_request(dynatrace.start_web_request)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the database commands
    from flaskr import db
    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')

    return app
