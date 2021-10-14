from flask import Flask
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Course

"""
call 'alembic revision -m "comment"' to make migration script
call using the --autogenerate tag to have alembic generate a script itself
using the model changes
"""

app = Flask(__name__)

# can specify a pool size that determines how many db connections we can have
engine = create_engine("postgresql://joshua:cmpt371@localhost:5432/proto")
Session = sessionmaker(bind=engine)  # object for use later
session = Session()


@app.route('/')
def index():
    data = session.query(Course)
    return f"<h1>{data}</h1>"


if __name__ == '__main__':
    app.run()
