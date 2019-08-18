"""
run program
flask_migrate use to upgrate models.py SQL tabel
flask_script use to commandline :
python manage.py runserver
"""
from app import create_app, db
from app.models import Uxser, Video, Camera
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app('production')
# manager = Manager(app)
migrate = Migrate(app, db)


# @manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# @manager.command
def deploy():
    """ run deployment tasks."""
    from flask_migrate import upgrade
    upgrade()


# for shell command auto to import app ,db
# python manage.py shell
def make_shell_context():
    return dict(app=app, db=db, Uxser=Uxser, Picture=Video, Camera=Camera)


# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
