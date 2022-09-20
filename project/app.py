import flask
from flask_session import Session

from typing import List, Tuple, Union

from database.dao import Dao
from uploadsManager.uploadsManager import UploadsManager
from model.art import Art
from model.artIntro import ArtIntro


APP = flask.Flask(__name__, static_url_path='/')

DAO = Dao()


@APP.get('/')
@APP.get('/home')
def home_page() -> str:
    return flask.render_template('client/home.html')


@APP.get('/gallery')
def gallery_page() -> Union[str, flask.Response]:
    arts_details = DAO.get_arts()

    if arts_details:
        arts = (build_art_intro_object_from_dao(art_details) for art_details in arts_details)

        return flask.render_template('client/gallery.html', arts=arts)

    return flask.redirect('/')


@APP.get('/artdetails')
def art_details_page() -> Union[str, flask.Response]:
    name = flask.request.args.get('name', default='', type=str)
    art_details = DAO.get_art(name)

    if art_details:
        art = build_art_object_from_dao(art_details[0])

        return flask.render_template('client/artdetails.html', art=art)

    return flask.redirect('/')


def build_art_intro_object_from_dao(details : List[Tuple[int, str, str]]) -> ArtIntro:
    art_id, name, description = details
    art_intro = ArtIntro(art_id, name, description)

    return art_intro


def build_art_object_from_dao(details : List[Tuple[int, str, str, str, int]]) -> Art:
    art_id, artists, name, description, creation_date, is_video_included = details
    art = Art(art_id, artists, name, description, creation_date, is_video_included)

    return art


@APP.get('/', subdomain='admin')
def admin_login_page() -> str:
    if flask.request.args:
        return flask.render_template('admin/adminlogin.html', message=flask.request.args['message'])

    return flask.render_template('admin/adminlogin.html')


@APP.post('/login', subdomain='admin')
def admin_login() -> Union[str, flask.Response]:
    username = flask.request.form['username']
    password = flask.request.form['password']

    if username == 'admin' and password == 'pass':
        flask.session['admin'] = True
        return flask.redirect('/adminpanel')

    return flask.redirect(flask.url_for('.admin_login_page', message='Username and/or password incorrect.'))


@APP.get('/adminpanel', subdomain='admin')
def admin_panel_page() -> Union[str, flask.Response]:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    if flask.request.args:
        return flask.render_template('admin/adminpanel.html', message=flask.request.args['message'])

    return flask.render_template('admin/adminpanel.html')


@APP.post('/adminpanel/add_art', subdomain='admin')
def admin_add_art() -> flask.Response:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    artists = flask.request.form['artists']
    name = flask.request.form['name']
    description = flask.request.form['description']
    creation_date = flask.request.form['creation_date']

    image = flask.request.files['image']
    video = flask.request.files['video']

    try:
        new_art_id = str(DAO.add_art(artists, name, description, creation_date, video.filename != '')[0][0])

        UploadsManager.upload_image(new_art_id, image.read())
        if video.filename:
            UploadsManager.upload_video(new_art_id, video.read())
    except Exception as e:
        return flask.redirect(flask.url_for('.admin_panel_page', message=f'Failed to add art: {e}.'))

    return flask.redirect(flask.url_for('.admin_panel_page', message=f'Art added successfully under ID: {new_art_id}.'))


if __name__ == '__main__':
    APP.secret_key = 'secret'
    APP.config['SERVER_NAME'] = 'thesnirgallery.com:80'
    APP.config['SESSION_TYPE'] = 'filesystem'
    Session(APP)
    APP.run()