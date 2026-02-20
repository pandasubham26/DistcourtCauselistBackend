import click
from app.extensions import db, bcrypt
from app.models.master.user import User


@click.command('create-superadmin')
def create_superadmin():
    username = input("Username: ")
    email = input("Email: ")
    estcode = input("Estcode: ")
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)

    super_admin = User(
        username=username,
        email=email,
        estcode=estcode,
        role='app_admin',
        isactive=True
    )

    password_hash = password
    super_admin.set_password(password_hash)

    db.session.add(super_admin)
    db.session.commit()

    click.echo("✅ Super admin created successfully!")
