import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from save_the_giphies.database.models import User, Giphy, Base, Tag


class TestModels(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        self.db_session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        Base.metadata.create_all(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_users(self):
        name = "foo"
        password = "foobar"
        email = "foo@bar.net"
        user = User(**{"name": name, "password": password, "email": email})
        self.db_session.add(user)
        self.db_session.commit()
        found = self.db_session.query(User).filter_by(id=user.id).first()
        self.assertEqual(email, found.email)
        self.assertEqual(name, found.name)
        self.assertNotEqual(password, found.password)

    def test_giphy(self):
        user = User(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        giphy1 = {"user_id": user.id, "giphy": "test_giphy1"}
        test_giphy1 = Giphy(**giphy1)
        giphy2 = {"user_id": user.id, "giphy": "test_giphy2"}
        test_giphy2 = Giphy(**giphy2)
        self.db_session.add(test_giphy1)
        self.db_session.add(test_giphy2)
        self.db_session.commit()
        found_first = self.db_session.query(Giphy).filter_by(id=test_giphy1.id).first()
        found_second = self.db_session.query(Giphy).filter_by(id=test_giphy2.id).first()
        self.assertEqual(giphy1["user_id"], found_first.user_id)
        self.assertEqual(giphy1["giphy"], found_first.giphy)
        self.assertEqual(giphy2["user_id"], found_second.user_id)
        self.assertEqual(giphy2["giphy"], found_second.giphy)
        with self.assertRaises(Exception) as ex:  # noqa: ignore=F841
            self.db_session.add(Giphy(**giphy2))
            self.db_session.commit()

    def test_tag(self):
        user = User(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        giphy = Giphy(**{"user_id": user.id, "giphy": "test_giphy1"})
        self.db_session.add(giphy)
        self.db_session.commit()
        tag = {"giphy_id": giphy.id, "tag": "animal"}
        test_tag = Tag(**tag)
        self.db_session.add(test_tag)
        self.db_session.commit()
        found = self.db_session.query(Tag).filter_by(id=test_tag.id).first()
        self.assertEqual(tag["giphy_id"], found.giphy_id)
        self.assertEqual(tag["tag"], found.tag)
        with self.assertRaises(Exception) as ex:  # noqa: ignore=F841
            self.db_session.add(Tag(**tag))
            self.db_session.commit()
