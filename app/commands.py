import click
from flask import Blueprint
from app.department.models import db, Department

bp = Blueprint('commands',__name__)


@bp.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    admin = Department.query.filter_by(role=1).first()
    if admin is not None:
        click.echo('Updating admin...')
        admin.username = username
        admin.set_password(password)  # 设置密码
    else:
        click.echo('Creating admin...')
        admin = Department(username=username, role=1)
        admin.set_password(password)  # 设置密码
        db.session.add(admin)

    db.session.commit()  # 提交数据库会话
    click.echo('Create Admin Done.')