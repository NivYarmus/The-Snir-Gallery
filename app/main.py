import flask

from database.dao import Dao
from model.art import Art, ArtIntro


APP = flask.Flask(__name__, static_url_path='/')
#APP.config['SERVER_NAME'] = 'thesnirgallery.com'

DAO = Dao()


@APP.get('/')
@APP.get('/home')
def home_page():
    return flask.render_template('home.html')


@APP.get('/gallery')
def gallery_page():
    arts_details = DAO.get_arts()

    if arts_details:
        arts = (build_art_intro_object_from_dao(art_details) for art_details in arts_details)

        return flask.render_template('gallery.html', arts=arts)
    
    return flask.redirect('/')


@APP.get('/artdetails')
def art_details_page():
    name = flask.request.args.get('name', default='', type=str)
    art_details = DAO.get_art(name)

    if art_details:
        art = build_art_object_from_dao(art_details[0])

        return flask.render_template('artdetails.html', art=art)

    return flask.redirect('/')


def build_art_intro_object_from_dao(details):
    id, name, description = details
    art_intro = ArtIntro(id, name, description)

    return art_intro

def build_art_object_from_dao(details):
    id, artist, name, description, creation_date = details
    art = Art(id, artist, name, description, creation_date)

    return art


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=80)
