from app import models
from app.daos import poems_dao

from tests.helpers import db


def test_create_poem(db):
    author_id = 1
    poem_data = models.PoemCreate(title="Test Poem", content="This is a test poem.")
    created_poem = poems_dao.create_poem(db, poem=poem_data, author_id=author_id)

    assert created_poem is not None
    assert created_poem.title == "Test Poem"
    assert created_poem.content == "This is a test poem."
    assert created_poem.author_id == author_id


def test_get_poems(db):
    for i in range(15):
        poem_data = models.PoemCreate(title=f"Poem {i}", content=f"Content {i}")
        poems_dao.create_poem(db, poem=poem_data, author_id=1)

    poems = poems_dao.get_poems(db, skip=0, limit=10)
    assert len(poems) == 10
    assert poems[0].title == "Poem 0"
    assert poems[-1].title == "Poem 9"


def test_get_poem_by_id(db):
    poem_data = models.PoemCreate(title="Test Poem", content="This is a test poem.")
    created_poem = poems_dao.create_poem(db, poem=poem_data, author_id=1)

    poem = poems_dao.get_poem_by_id(db, poem_id=created_poem.id)
    assert poem is not None
    assert poem.title == "Test Poem"

    assert poems_dao.get_poem_by_id(db, poem_id=999) is None


def test_update_poem(db):
    poem_data = models.PoemCreate(title="Original Title", content="Original Content")
    created_poem = poems_dao.create_poem(db, poem=poem_data, author_id=1)

    updated_poem = poems_dao.update_poem(db, poem_id=created_poem.id, title="Updated Title", content="Updated Content")

    assert updated_poem is not None
    assert updated_poem.title == "Updated Title"
    assert updated_poem.content == "Updated Content"

    assert poems_dao.update_poem(db, poem_id=999, title="Non-existent", content="Non-existent") is None
