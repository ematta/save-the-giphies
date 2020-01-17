from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from save_the_giphies.database.engine import Base, db_session
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(120))
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __init__(self, email: str, password: str, name: str):
        self.name: str = name
        self.email: str = email
        self.password: str = generate_password_hash(password, method="sha256")

    @classmethod
    def authenticate(cls, email: str, password: str):
        if not email or not password:
            return None
        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    @classmethod
    def register(cls, email: str, name: str, password):
        user = User(email=email, password=password, name=name)
        db_session.add(user)
        return db_session.commit()

    def to_dict(self):
        return dict(id=self.id, email=self.email, name=self.name)

class Giphy(Base):
    __tablename__ = "giphies"
    __table_args__ = (UniqueConstraint("user_id", "giphy", name="_user_giphy_uc_"),)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    giphy = Column(String, nullable=False)

    def __init__(self, user_id: int, giphy: str):
        self.user_id: int = user_id
        self.giphy: str = giphy

    @classmethod
    def all_giphies(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def delete_giphy(cls, user_id: int, giphy: str):
        giphy = cls.query.filter_by(user_id=user_id, giphy=giphy).first()
        db_session.delete(giphy)
        return db_session.commit()

    @classmethod
    def first_giphy(cls, user_id: int, giphy: str):
        return cls.query.filter_by(user_id=user_id, giphy=giphy).first()

    @classmethod
    def save_giphy(cls, user_id: int, giphy: str):
        giphy = Giphy(user_id=user_id, giphy=giphy)
        db_session.add(giphy)
        return db_session.commit()

    def to_dict(self):
        return dict(id=self.id, user_id=self.user_id, giphy=self.giphy)




class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("giphy_id", "tag", name="_tag_giphy_uc_"),)
    id = Column(Integer, primary_key=True)
    giphy_id = Column(Integer, ForeignKey("giphies.id"), nullable=False)
    tag = Column(String(50), unique=True, nullable=False)

    @classmethod
    def all_tags(cls, giphy_id: int):
        return cls.query.filter_by(giphy_id=giphy_id).all()

    @classmethod
    def delete_tag(cls, giphy_id: int, tag: str):
        found_tag = cls.query.filter_by(giphy_id=giphy_id, tag=tag).first()
        db_session.delete(found_tag)
        return db_session.commit()

    @classmethod
    def save_tag(cls, giphy_id: int, tag: str):
        new_tag = Tag(**{"giphy_id": giphy_id, "tag": tag})
        db_session.add(new_tag)
        return db_session.commit()

    def __init__(self, tag: str, giphy_id: int):
        self.tag: str = tag
        self.giphy_id: id = giphy_id
