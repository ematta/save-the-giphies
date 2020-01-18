import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from save_the_giphies.database.models import Users, Giphies, Base, Tags


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
        user = Users(**{"name": name, "password": password, "email": email})
        self.db_session.add(user)
        self.db_session.commit()
        found = self.db_session.query(Users).filter_by(id=user.id).first()
        self.assertEqual(email, found.email)
        self.assertEqual(name, found.name)
        self.assertNotEqual(password, found.password)

    def test_giphy(self):
        user = Users(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        giphy1 = {"users_id": user.id, "giphy": "test_giphy1"}
        test_giphy1 = Giphies(**giphy1)
        giphy2 = {"users_id": user.id, "giphy": "test_giphy2"}
        test_giphy2 = Giphies(**giphy2)
        self.db_session.add(test_giphy1)
        self.db_session.add(test_giphy2)
        self.db_session.commit()
        found_first = (
            self.db_session.query(Giphies).filter_by(id=test_giphy1.id).first()
        )
        found_second = (
            self.db_session.query(Giphies).filter_by(id=test_giphy2.id).first()
        )
        self.assertEqual(giphy1["users_id"], found_first.users_id)
        self.assertEqual(giphy1["giphy"], found_first.giphy)
        self.assertEqual(giphy2["users_id"], found_second.users_id)
        self.assertEqual(giphy2["giphy"], found_second.giphy)
        with self.assertRaises(Exception) as ex:  # noqa: ignore=F841
            self.db_session.add(Giphies(**giphy2))
            self.db_session.commit()

    def test_giphy_delete(self):
        user = Users(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        test_giphy = Giphies(**{"users_id": user.id, "giphy": "test_giphy1"})
        self.db_session.add(test_giphy)
        self.db_session.commit()
        self.db_session.delete(test_giphy)
        self.db_session.commit()

    def test_users_giphies_delete(self):
        user = Users(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        test_giphy = Giphies(**{"users_id": user.id, "giphy": "test_giphy1"})
        self.db_session.add(test_giphy)
        self.db_session.commit()
        self.db_session.delete(user)
        self.db_session.commit()

    def test_tag(self):
        user = Users(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        giphy = Giphies(**{"users_id": user.id, "giphy": "test_giphy1"})
        self.db_session.add(giphy)
        self.db_session.commit()
        tag = {"giphies_id": giphy.id, "tag": "animal"}
        test_tag = Tags(**tag)
        self.db_session.add(test_tag)
        self.db_session.commit()
        found = self.db_session.query(Tags).filter_by(id=test_tag.id).first()
        self.assertEqual(tag["giphies_id"], found.giphies_id)
        self.assertEqual(tag["tag"], found.tag)
        with self.assertRaises(Exception) as ex:  # noqa: ignore=F841
            self.db_session.add(Tags(**tag))
            self.db_session.commit()

    def test_delete_tag(self):
        user = Users(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        giphy = Giphies(**{"users_id": user.id, "giphy": "test_giphy1"})
        self.db_session.add(giphy)
        self.db_session.commit()
        tag = Tags(**{"giphies_id": giphy.id, "tag": "animal"})
        self.db_session.add(tag)
        self.db_session.commit()
        self.db_session.delete(tag)
        self.db_session.commit()

    def test_delete_giphies_with_tags(self):
        user = Users(**{"name": "foo", "password": "foobar", "email": "foo@bar.net"})
        self.db_session.add(user)
        self.db_session.commit()
        giphy = Giphies(**{"users_id": user.id, "giphy": "test_giphy1"})
        self.db_session.add(giphy)
        self.db_session.commit()
        tag = Tags(**{"giphies_id": giphy.id, "tag": "animal"})
        self.db_session.add(tag)
        self.db_session.commit()
        self.db_session.delete(giphy)
        self.db_session.commit()
