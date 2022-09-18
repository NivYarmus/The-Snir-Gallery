import flask
from flask_session import Session

from database.dao import Dao
from model.art import Art
from model.artIntro import ArtIntro
from model.artName import ArtName


APP = flask.Flask(__name__, static_url_path='/')

DAO = Dao()


@APP.get('/')
@APP.get('/home')
def home_page():
    return flask.render_template('client/home.html')


@APP.get('/gallery')
def gallery_page():
    arts_details = DAO.get_arts()

    if arts_details:
        arts = (build_art_intro_object_from_dao(art_details) for art_details in arts_details)

        return flask.render_template('client/gallery.html', arts=arts)

    return flask.redirect('/')


@APP.get('/artdetails')
def art_details_page():
    name = flask.request.args.get('name', default='', type=str)
    art_details = DAO.get_art(name)

    if art_details:
        art = build_art_object_from_dao(art_details[0])

        return flask.render_template('client/artdetails.html', art=art)

    return flask.redirect('/')


@APP.get('/', subdomain='admin')
def admin_login():
    if 'display_error' in flask.request.args:
        return flask.render_template('admin/adminlogin.html', display_error=flask.request.args['display_error'])

    return flask.render_template('admin/adminlogin.html')


@APP.get('/adminpanel', subdomain='admin')
def admin_panel():
    if not 'ADMIN' in flask.session or not flask.session['ADMIN']:
        return flask.redirect('/')

    arts_names = DAO.get_arts_names()
    arts_names = (x[0] for x in arts_names)

    if 'new_name' in flask.request.args:
        return flask.render_template('admin/adminpanel.html', names=arts_names, new_name=flask.request.args['new_name'])

    return flask.render_template('admin/adminpanel.html', names=arts_names)

@APP.post('/login', subdomain='admin')
def admin_login_handle():
    username_input = flask.request.form['username']
    password_input = flask.request.form['password']

    if username_input == 'admin' and password_input == 'pass':
        flask.session['ADMIN'] = True
        return flask.redirect('/adminpanel')

    return flask.redirect(flask.url_for('.admin_login', display_error='True'))


@APP.post('/add_art', subdomain='admin')
def admin_add_art():
    if not 'ADMIN' in flask.session or not flask.session['ADMIN']:
        return flask.redirect('/')

    new_art_id = DAO.add_new_art()[0][0]
    
    return flask.redirect(flask.url_for('.admin_panel', new_name=str(new_art_id)))


def build_art_intro_object_from_dao(details):
    art_id, name, description = details
    art_intro = ArtIntro(art_id, name, description)

    return art_intro


def build_art_name_object_from_dao(details):
    art_id, name = details
    art_name = ArtName(art_id, name)
    
    return art_name

def build_art_object_from_dao(details):
    art_id, artists, name, description, creation_date, is_video_included = details
    art = Art(art_id, artists, name, description, creation_date, is_video_included)

    return art


if __name__ == '__main__':
    APP.config['SERVER_NAME'] = 'thesnirgallery.com:80'
    APP.config["SESSION_PERMANENT"] = False
    APP.config["SESSION_TYPE"] = "filesystem"
    Session(APP)
    APP.run() #ssl_context='adhoc'
