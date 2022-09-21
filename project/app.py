import flask
from flask_session import Session
from Crypto.Hash import SHA256

from typing import Tuple, Union

from database.dao import Dao
from uploadsManager.uploadsManager import UploadsManager
from model.art import Art
from model.artIntro import ArtIntro
from model.artName import ArtName


APP = flask.Flask(__name__, static_folder=None)

DAO = Dao()


@APP.get('/')
@APP.get('/home')
def home_page() -> str:
    return flask.render_template('client/home.html')


@APP.get('/gallery')
def gallery_page() -> Union[str, flask.Response]:
    arts_details = DAO.get_arts_intro()

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


def build_art_intro_object_from_dao(details : Tuple[int, str, str]) -> ArtIntro:
    art_id, name, description = details
    art_intro = ArtIntro(art_id, name, description)

    return art_intro


def build_art_object_from_dao(details : Tuple[int, str, str, str, int]) -> Art:
    art_id, artists, name, description, creation_date, is_video_included = details
    art = Art(art_id, artists, name, description, creation_date, is_video_included)

    return art


@APP.get('/', subdomain='admin')
def admin_login_page(message : str = '') -> str:
    if message:
        return flask.render_template('admin/adminlogin.html', message=message)

    return flask.render_template('admin/adminlogin.html')


@APP.post('/login', subdomain='admin')
def admin_login() -> Union[str, flask.Response]:
    username = flask.request.form['username']
    password = flask.request.form['password']

    username_sha = SHA256.new()
    password_sha = SHA256.new()

    username_sha.update(username.encode())
    password_sha.update(password.encode())

    if DAO.is_admin(username_sha.hexdigest(), password_sha.hexdigest()):
        flask.session['admin'] = True
        return flask.redirect('/adminpanel')

    return admin_login_page('Username and/or password incorrect.')


@APP.get('/adminpanel', subdomain='admin')
def admin_panel_page(message : str = '', art : Art = None) -> str:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    arts_details = DAO.get_arts_names()
    arts_names = [build_art_name_object_from_dao(art_details) for art_details in arts_details]

    if message:
        return flask.render_template('admin/adminpanel.html', message=message, arts_names=arts_names, art=art)

    return flask.render_template('admin/adminpanel.html', arts_names=arts_names, art=art)


@APP.post('/add_art', subdomain='admin')
def admin_add_art() -> str:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    artists = flask.request.form['add_artists']
    name = flask.request.form['add_name']
    description = flask.request.form['add_description']
    creation_date = flask.request.form['add_creation_date']

    image = flask.request.files['add_image']
    video = flask.request.files['add_video']

    new_art_id = str(DAO.add_art(artists, name, description, creation_date, video.filename != '')[0][0])

    UploadsManager.upload_image(new_art_id, image.read())
    if video.filename:
        UploadsManager.upload_video(new_art_id, video.read())

    return admin_panel_page(f'Art added successfully under ID: {new_art_id}.')


@APP.post('/delete_art', subdomain='admin')
def admin_delete_art() -> str:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    art_id = int(flask.request.form['art-delete-picker'])
    is_video_included = bool(DAO.get_video_status(art_id)[0][0])

    DAO.delete_art(art_id)
    UploadsManager.delete_image(art_id)
    if is_video_included:
        UploadsManager.delete_video(art_id)

    return admin_panel_page(f'Deleted art under ID: {art_id}.')


@APP.post('/edit_art', subdomain='admin')
def admin_edit_art() -> str:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    art_id = int(flask.request.form['edit_id'])

    artists = flask.request.form['edit_artists']
    name = flask.request.form['edit_name']
    description = flask.request.form['edit_description']
    creation_date = flask.request.form['edit_creation_date']

    image = flask.request.files['edit_image']
    video = flask.request.files['edit_video']

    is_video_included = bool(DAO.get_video_status(art_id)[0][0])
    DAO.edit_art(art_id, artists, name, description, creation_date, video.filename != '')

    art_id = str(art_id)
    if image.filename:
        UploadsManager.edit_image(art_id, image.read())
    if not video.filename:
        if is_video_included:
            UploadsManager.delete_video(art_id)
    else:
        UploadsManager.edit_video(art_id, video.read())

    return admin_panel_page(f'Art id({art_id}) edited successfully.')


@APP.post('/edit_picker_change', subdomain='admin')
def admin_edit_picker_change() -> str:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    art_id = int(flask.request.form['art-edit-picker'])

    art_details = DAO.get_art(art_id)
    art = build_art_object_from_dao(art_details[0])

    return admin_panel_page(art=art)


@APP.post('/add_admin', subdomain='admin')
def add_admin() -> str:
    if not 'admin' in flask.session or not flask.session['admin']:
        return flask.redirect('/')

    username = flask.request.form['add_admin_username']
    password = flask.request.form['add_admin_password']

    username_sha = SHA256.new()
    password_sha = SHA256.new()

    try:
        username_sha.update(username.encode())
        password_sha.update(password.encode())
        DAO.add_admin(username_sha.hexdigest(), password_sha.hexdigest())
    except:
        return admin_panel_page(f'Failed to add {username} to admins.')

    return admin_panel_page(f'Admin {username} added successfully.')

def build_art_name_object_from_dao(details : Tuple[int, str]) -> ArtName:
    art_id, name = details
    art_name = ArtName(art_id, name)

    return art_name


if __name__ == '__main__':
    APP.secret_key = 'secret'
    APP.static_folder = 'static'

    APP.config['SERVER_NAME'] = 'thesnirgallery.com:80'
    APP.config['SESSION_TYPE'] = 'filesystem'

    APP.add_url_rule('/<path:filename>',
                    endpoint='static',
                    subdomain='',
                    view_func=APP.send_static_file)
    APP.add_url_rule('/<path:filename>',
                    endpoint='static',
                    subdomain='admin',
                    view_func=APP.send_static_file)
    Session(APP)
    APP.run()