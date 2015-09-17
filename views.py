from flask import Flask, render_template, request, flash
from flask.ext.session import Session
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from forms import AddBookMark, EditBookMark


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
CsrfProtect(app)
bookmark_flask_session = Session

from models import BookMark

# Helper functions


def all_bookmarks():
    return db.session.query(BookMark).all()


def one_bookmark(id):
    return db.session.query(BookMark).filter_by(bookmark_id=id).one()


# all bookmarks
@app.route('/api/v1/bookmarks', methods=['GET'])
def bookmarks():
    return render_template('bookmarks.html',
                           form=AddBookMark(request.form),
                           all_bookmarks=all_bookmarks())


# add a bookmark
@app.route('/api/v1/bookmarks/add', methods=['GET', 'POST'])
def add_bookmark():
    form = AddBookMark(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_bookmark = BookMark(form.bookmark_url.data)
            db.session.add(new_bookmark)
            db.session.commit()
            flash('New bookmark saved.')
            return render_template('bookmarks.html',
                                   form=form, all_bookmarks=all_bookmarks())
    return render_template('entry_bookmarks.html', form=form)


# get or edit a single bookmark
@app.route('/api/v1/bookmark/edit/<int:id>', methods=['GET', 'POST'])
def edit_bookmark(id):
    form = EditBookMark(request.form)
    editable_bookmark = one_bookmark(id)

    if request.method == 'POST':
        if form.validate_on_submit():
            updated_bookmark = str(form.bookmark_url.data)
            bmark_id = id
            db.session.query(BookMark).filter_by(bookmark_id=bmark_id).update(
                {"bookmark_url": updated_bookmark})
            db.session.commit()
            flash('BookMark Update is successful')
            return render_template('bookmarks.html',
                                   all_bookmarks=all_bookmarks())
    return render_template('edit_bookmarks.html', form=form,
                           editable_bookmark=editable_bookmark)


# delete a single bookmark
@app.route('/api/v1/bookmark/delete/<int:id>', methods=['GET'])
def delete_bookmark(id):
    bmark_id = id
    db.session.query(BookMark).filter_by(bookmark_id=bmark_id).delete()
    db.session.commit()
    flash('The BookMark was successfully deleted.')
    return render_template('bookmarks.html', all_bookmarks=all_bookmarks())
