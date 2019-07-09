# -*- coding: utf-8 -*-

''' Blog Implementation
'''

import time
import requests

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.dynatrace import getdbinfo, getsdk, get_user_role

import oneagent.sdk

bp = Blueprint('blog', __name__)

@bp.route("/")
def index():
    ''' Create the Post Index '''
    query = "SELECT p.id, title, body, created, author_id, username" \
            " FROM post p JOIN user u ON p.author_id = u.id" \
            " ORDER BY created DESC"
    dbinfo = getdbinfo()
    with dbinfo:
        with getsdk().trace_sql_database_request(dbinfo, query):
            # Show all the posts, most recent first.
            db = get_db()
            posts = db.execute(query).fetchall()
    return render_template("blog/index.html", posts=posts)


def get_post(pid, check_author=True):
    '''Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param pid: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    '''

    query = 'SELECT p.id, title, body, created, author_id, username' \
            ' FROM post p JOIN user u ON p.author_id = u.id' \
            ' WHERE p.id = ?'
    dbinfo = getdbinfo()
    with dbinfo:
        with getsdk().trace_sql_database_request(dbinfo, query):
            post = get_db().execute(query, (pid,)).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(pid))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    '''Create a new post for the current user.'''
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            query = "INSERT INTO post (title, body, author_id)" \
                    " VALUES (?, ?, ?)"
            dbinfo = getdbinfo()
            db = get_db()
            with dbinfo:
                with getsdk().trace_sql_database_request(dbinfo, query):
                    db.execute(query, (title, body, g.user["id"]),)
                    db.commit()

            inform_editors()

            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route('/<int:pid>/update', methods=('GET', 'POST'))
@login_required
def update(pid):
    ''''Update a post if the current user is the author.'''
    post = get_post(pid)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            query = 'UPDATE post SET title = ?, body = ? WHERE id = ?'
            dbinfo = getdbinfo()
            db = get_db()
            with dbinfo:
                with getsdk().trace_sql_database_request(dbinfo, query):
                    db.execute(query, (title, body, pid))
                    db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route("/<int:pid>/delete", methods=("POST",))
@login_required
def delete(pid):
    ''' Delete a Post '''
    dbinfo = getdbinfo()
    query = "DELETE FROM post WHERE id = ?"
    get_post(pid)
    db = get_db()
    with dbinfo:
        with getsdk().trace_sql_database_request(dbinfo, query):
            db.execute(query, (pid,))
            db.commit()
    return redirect(url_for("blog.index"))

def inform_editors():
    ''' Inform Editors '''
    sdk = getsdk()
    role = get_user_role()
    if role == "author":
        with sdk.trace_custom_service('review', 'BlogReview'):
            time.sleep(5)
            send_notification()

def send_notification():
    ''' Send Notification '''
    url = 'http://localhost:8123/send'
    with getsdk().trace_outgoing_web_request(url, 'GET') as tracer:
        # Get the Dynatrace tag.
        tag = tracer.outgoing_dynatrace_string_tag

        # Sending the web request, attaching the tag with the name expected by
        # other Dynatrace OneAgents
        response = requests.get(url,
            headers={oneagent.sdk.DYNATRACE_HTTP_HEADER_NAME: tag})

        tracer.add_response_headers(response.headers)
        tracer.set_status_code(response.status_code)
