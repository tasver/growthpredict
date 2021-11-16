
import click
from flask.cli import with_appcontext

from growthpredict import db,bcrypt
from growthpredict.models import *

@click.command(name = 'create_tables')
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name = 'init_db')
@with_appcontext
def init_db():
    init_db()

@click.group()
def cli():
    pass

@click.command(name='create_admin')
@with_appcontext
def create_admin():
    click.echo('Hello! Run command ok before')
    username = "admin"
    admin = True
    email = "admin@gmail.com"
    password = bcrypt.generate_password_hash("admin").decode('utf-8')
    u = User(username=username, admin=admin, email=email, password=password)
    #print("superadmin created", u)
    db.session.add(u)
    db.session.commit()
    click.echo("superadmin created!!!")

cli.add_command(init_db)
#cli.add_command(create_tables)
cli.add_command(create_admin)


if __name__ == '__main__':
    cli()