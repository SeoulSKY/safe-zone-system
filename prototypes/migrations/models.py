from sqlalchemy.orm import declarative_base
import sqlalchemy as db

Base = declarative_base()
class Course(Base):
    __tablename__ = "courses"
    name = db.Column(db.String, primary_key=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String, nullable=False)
    # will add a Column for location using alembic
    # location = Column(String, nullable=False)

class School(Base):
    __tablename__ = "schools"
    name = db.Column(db.String, primary_key=True, nullable=False)
    students = db.Column(db.Integer, nullable=False)
