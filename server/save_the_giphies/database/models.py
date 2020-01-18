from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from save_the_giphies.database.engine import Base, db_session
from werkzeug.security import generate_password_hash, check_password_hash
from save_the_giphies.libraries.logger import logger

from typing import Dict, List, Tuple


class Users(Base):
    """ Users table Model """

    __tablename__: "str" = "users"
    id: "Column" = Column(
        Integer, primary_key=True, autoincrement=True,
    )
    name: "Column" = Column(String(120))
    email: "Column" = Column(String(120), unique=True, nullable=False)
    password: "Column" = Column(String(120), nullable=False)

    def __init__(self, email: "str", password: "str", name: "str"):
        self.name: "str" = name
        self.email: "str" = email
        self.password: "str" = generate_password_hash(password, method="sha256")

    def to_dict(self) -> "Dict":
        """ Converts model to dict """
        result = dict(id=self.id, email=self.email, name=self.name)
        logger.info(f"User Dict {result}")
        return result

    @classmethod
    def authenticate(cls, email: "str", password: "str") -> "Dict":
        """Authentication helper
        Params:
            email (str): Email address of account
            password (str): String to check

        Returns Dict
        """
        if not email or not password:
            logger.warn(f"No email or password set: email {email}, password {password}")
            return {"success": False, "msg": "No email or password set"}
        user: "Users" = cls.query.filter_by(email=email).first()
        if not user:
            logger.warn(f"User not found")
            return {"success": False, "msg": "User not found"}
        if not check_password_hash(user.password, password):
            logger.warn(f"Password incorrect")
            return {"success": False, "msg": "Password incorrect"}
        return {"success": True, "msg": "User authenticated", "user": user}

    @classmethod
    def register(cls, email: "str", name: "str", password: "str") -> "Dict":
        """ Registers a user
        Params:
            email (str): User's email
            name (str): User's name
            password (str): User's password

        Returns Dict
        """
        try:
            user: "Users" = Users(email=email, password=password, name=name)
            db_session.add(user)
            db_session.commit()
            logger.info(f"User registered")
            new_user: "Users" = cls.query.filter_by(email=email).first()
            return {"success": True, "msg": "User Registered", "user": new_user}
        except Exception as e:
            msg: "str" = f"Could not register {e}"
            logger.error(msg)
            return {"success": False, "msg": msg}


class Giphies(Base):
    """ Giphies table model """

    __tablename__: "str" = "giphies"
    __table_args__: "Tuple[UniqueConstraint]" = (
        UniqueConstraint("users_id", "giphy", name="_user_giphy_uc_"),
    )
    id: "Column" = Column(
        Integer, primary_key=True, autoincrement=True,
    )
    users_id: "Column" = Column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    giphy: "Column" = Column(String, nullable=False)

    def __init__(self, users_id: "int", giphy: "str"):
        self.users_id: "int" = users_id
        self.giphy: "str" = giphy

    def to_dict(self) -> "Dict":
        """ Converts model to dict """
        result = dict(id=self.id, users_id=self.users_id, giphy=self.giphy)
        logger.info(f"Giphy Dict {result}")
        return result

    @classmethod
    def all_giphies(cls, users_id: "int") -> "List[Giphies]":
        """ Returns user's giphies
        Params:
            user_id (int): User ID

        Returns List[Giphies]
        """
        giphies: "List[Dict]" = cls.query.filter_by(users_id=users_id).all()
        logger.info(f"Giphies list {giphies}")
        return giphies

    @classmethod
    def delete_giphy(cls, users_id: "int", giphy: "str") -> "bool":
        """ Deletes user's giphy
        Params:
            user_id (int): User's ID
            giphy (str): The giphy ID provided by GIPHY

        Returns boolean
        """
        try:
            giphy: "Giphies" = cls.query.filter_by(
                users_id=users_id, giphy=giphy
            ).first()
            db_session.delete(giphy)
            db_session.commit()
            logger.error(f"Deleted {giphy}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {giphy}: {e}")
            return False

    @classmethod
    def first_giphy(cls, users_id: "int", giphy: "str") -> "Giphies":
        """ Grabs the giphy for the user
        Params:
            user_id (int): User's ID
            giphy (str): The giphy ID provided by GIPHY

        Returns Giphies
        """
        giphy: "Giphies" = cls.query.filter_by(users_id=users_id, giphy=giphy).first()
        success = True if giphy is not None else False
        logger.info(f"User's Giphy: {giphy}")
        return {"success": success, "giphy": giphy}

    @classmethod
    def save_giphy(cls, users_id: int, giphy: str) -> "Dict":
        """ Save Giphy for user
        Params:
            user_id (int): User's ID
            giphy (str): The giphy ID provided by GIPHY

        Returns Dict
        """
        try:
            giphy = Giphies(users_id=users_id, giphy=giphy)
            db_session.add(giphy)
            db_session.commit()
            logger.info("Saved giphy")
            return {"success": True, "msg": "Saved Giphy", "giphy": giphy}
        except Exception as e:
            return {
                "success": False,
                "msg": f"Could not save {giphy} for {users_id}: {e}",
            }


class Tags(Base):
    """ Tags table model """

    __tablename__: "str" = "tags"
    __table_args__: "Tuple[UniqueConstraint]" = (
        UniqueConstraint("giphies_id", "tag", name="_tag_giphy_uc_"),
    )
    id = Column(Integer, primary_key=True)
    giphies_id: "Column" = Column(
        Integer,
        ForeignKey("giphies.id", onupdate="CASCADE", ondelete="CASCADE"),
        autoincrement=True,
    )
    tag: "Column" = Column(String(50), nullable=False)

    def __init__(self, tag: "str", giphies_id: "int"):
        self.tag: "str" = tag
        self.giphies_id: "int" = giphies_id

    def to_dict(self):
        """ Converts model to dict """
        result = dict(id=self.id, giphies_id=self.giphies_id, tag=self.tag)
        logger.info(f"Giphy Dict {result}")
        return result

    @classmethod
    def all_tags(cls, giphies_id: "int") -> "List[Tags]":
        """ All tags retrieved for Giphy
        Params:
            giphies_id (int): Giphy ID

        Returns List[Tags]
        """
        tags: "List[Tags]" = cls.query.filter_by(giphies_id=giphies_id).all()
        logger.info(f"Tags found: {tags}")
        return tags

    @classmethod
    def delete_tag(cls, giphies_id: "int", tag_id: "int") -> "bool":
        """ Delete tag for giphy
        Params:
            giphies_id (int): Giphy ID
            tag_id (int): Tag ID

        Returns boolean
        """
        try:
            found_tag = cls.query.filter_by(giphies_id=giphies_id, id=tag_id).first()
            db_session.delete(found_tag)
            db_session.commit()
            logger.error(f"Deleted Tag {tag_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {tag_id}: {e}")
            return False

    @classmethod
    def save_tag(cls, giphies_id: "int", tag: "str") -> "Dict":
        """ Save tag
        Params:
            giphies_id (int): Giphy ID
            tag (str): The tag

        Returns Dict
        """
        try:
            new_tag = Tags(**{"giphies_id": giphies_id, "tag": tag})
            db_session.add(new_tag)
            db_session.commit()
            logger.info("Saved giphy")
            return {
                "success": True,
                "msg": f"Saved tag {tag} for giphy id {giphies_id}",
            }
        except Exception as e:
            return {
                "success": False,
                "msg": f"Could not save {tag} for {giphies_id}: {e}",
            }
