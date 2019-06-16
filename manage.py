from app import app, db

from flask_script import Manager

manager = Manager(app)

@manager.command
def initdb():
    """ Initialize database.
    """

    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    manager.run()