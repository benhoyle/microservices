"""Command line function to manage users."""
# services/users/manage.py
import unittest
import coverage

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

# Coverage
cov_entity = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
cov_entity.start()


@cli.command()
def recreate_db():
    """Command line function to recreate database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    """Seed the database."""
    db.session.add(User(
        username='ben',
        email='ben@benmail.com',
        password='12345678'
    ))
    db.session.add(User(
        username='jimbob',
        email='jimbob@email.com',
        password='herearesomerandomwords'
    ))
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Run the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov_entity.stop()
        cov_entity.save()
        print('Coverage Summary:')
        cov_entity.report()
        cov_entity.html_report()
        cov_entity.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
