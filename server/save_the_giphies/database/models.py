from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from save_the_giphies.database.engine import Base, db_session
from werkzeug.security import generate_password_hash, check_password_hash


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True,)
    name = Column(String(120))
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __init__(self, email: str, password: str, name: str):
        self.name: str = name
        self.email: str = email
        self.password: str = generate_password_hash(password, method="sha256")

    def to_dict(self):
        return dict(id=self.id, email=self.email, name=self.name)

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
        user = Users(email=email, password=password, name=name)
        db_session.add(user)
        return db_session.commit()


class Giphies(Base):
    __tablename__ = "giphies"
    __table_args__ = (UniqueConstraint("users_id", "giphy", name="_user_giphy_uc_"),)
    id = Column(Integer, primary_key=True, autoincrement=True,)
    users_id = Column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    giphy = Column(String, nullable=False)

    def __init__(self, users_id: int, giphy: str):
        self.users_id: int = users_id
        self.giphy: str = giphy

    def to_dict(self):
        return dict(id=self.id, users_id=self.users_id, giphy=self.giphy)

    @classmethod
    def all_giphies(cls, users_id: int):
        return cls.query.filter_by(users_id=users_id).all()

    @classmethod
    def delete_giphy(cls, users_id: int, giphy: str):
        giphy = cls.query.filter_by(users_id=users_id, giphy=giphy).first()
        db_session.delete(giphy)
        return db_session.commit()

    @classmethod
    def first_giphy(cls, users_id: int, giphy: str):
        return cls.query.filter_by(users_id=users_id, giphy=giphy).first()

    @classmethod
    def save_giphy(cls, users_id: int, giphy: str):
        giphy = Giphies(users_id=users_id, giphy=giphy)
        db_session.add(giphy)
        return db_session.commit()


class Tags(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("giphies_id", "tag", name="_tag_giphy_uc_"),)
    id = Column(Integer, primary_key=True)
    giphies_id = Column(
        Integer,
        ForeignKey("giphies.id", onupdate="CASCADE", ondelete="CASCADE"),
        autoincrement=True,
    )
    tag = Column(String(50), nullable=False)

    def __init__(self, tag: str, giphies_id: int):
        self.tag: str = tag
        self.giphies_id: id = giphies_id

    def to_dict(self):
        return dict(id=self.id, giphies_id=self.giphies_id, tag=self.tag)

    @classmethod
    def all_tags(cls, giphies_id: int):
        return cls.query.filter_by(giphies_id=giphies_id).all()

    @classmethod
    def delete_tag(cls, giphies_id: int, tag_id: int):
        found_tag = cls.query.filter_by(giphies_id=giphies_id, id=tag_id).first()
        db_session.delete(found_tag)
        return db_session.commit()

    @classmethod
    def save_tag(cls, giphies_id: int, tag: str):
        new_tag = Tags(**{"giphies_id": giphies_id, "tag": tag})
        db_session.add(new_tag)
        return db_session.commit()
