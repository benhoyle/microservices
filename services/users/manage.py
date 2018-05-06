"""Command line function to manage users."""
# services/users/manage.py

from flask.cli import FlaskGroup

from project import app, db

cli = FlaskGroup(app)


@cli.command()
def recreate_db():
    """Command line function to recreate database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
