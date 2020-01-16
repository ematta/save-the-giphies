from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from save_the_giphies.database.engine import Base, db_session
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(120))
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __init__(self, email: str, password: str, name: str = None):
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

    def to_dict(self):
        return dict(id=self.id, email=self.email, name=self.name)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        self.name: str = name


class Giphy(Base):
    __tablename__ = "giphies"
    __table_args__ = (UniqueConstraint('user_id', 'giphy', name='_user_giphy_uc_'),)
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
        db_session.commit()

    def to_dict(self):
        return dict(id=self.id, user_id=self.user_id, giphy=self.giphy)
