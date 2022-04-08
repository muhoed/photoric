import datetime
import pytest

from photoric import db
from photoric.modules.auth.models import User, Group, Role


@pytest.fixture
def user(app):

    image = User(
        name = "Test user",
        email = 'test@test.com',
        password = 'test_password'
        )
    db.session.add(user)
    db.session.commit()
    
    yield user

    db.session.delete(user)
    db.session.commit()

@pytest.fixture
def album(authenticated_request):

    album = Album(
        name = "Test album"
        )
    db.session.add(album)
    db.session.commit()
    
    yield album

    db.session.delete(album)
    db.session.commit()

def test_new_image(image):
    """
    GIVEN an Image model
    WHEN a new Image is created
    THEN check 'uploaded_on' is set, 'is_published' is set to False, '__str__' method returns image filename
    """
    assert image.uploaded_on is not None
    assert image.is_published is False
    assert str(image) == "<Image 'testimage.jpg'>"

def test_publish_image(image):
    """
    GIVEN an Image model
    WHEN an Image is published
    THEN check 'is_published' is set to True, 'published_on' is not None
    """
    image.publish()

    assert image.is_published is True
    assert image.published_on is not None

def test_new_album(album):
    """
    GIVEN an Album model
    WHEN a new Album is created
    THEN check 'is_published' is set to False, '__str__' method returns Album name
    """
    assert album.is_published is False
    assert str(album) == "<Album 'Test album'>"

def test_publish_album(album):
    """
    GIVEN an Album model
    WHEN an Album is published
    THEN check 'is_published' is set to True, 'published_on' is not None
    """
    album.publish()

    assert album.is_published is True
    assert album.published_on is not None
    
def test_add_image_to_album(image, album):
    """
    GIVEN Album and Image model
    WHEN an Image is added to Album
    THEN check Image is in Album's 'children_images', Albun is in Image's 'parent_albums'
    """
    album.children_images.append(image)

    assert image in album.children_images
    assert album in image.parent_albums

