from typing import Dict, List

from . import models
from . import db
from datetime import datetime
from . import fake


def reset_db():
    db.drop_all()
    db.create_all()
    models.Role.insert_roles()
    admin_role = models.Role.query.filter_by(name='Administrator').first()
    u_admin = models.User(email='admin@localhost',
                          username='admin',
                          password='admin',
                          confirmed=True,
                          name='admin',
                          location='',
                          about_me='bbs admin',
                          member_since=datetime.utcnow(),
                          role=admin_role
                          )
    db.session.add(u_admin)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    fake.users(10)
    fake.threads(10)
    fake.posts(20)


def force_verify_user(username: str):
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        print('user not found')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()


def set_moderater(username: str):
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        print('user not found')
    else:
        Moderator_role = models.Role.query.filter_by(name='Moderator').first()
        user.change_role(Moderator_role)
        db.session.add(user)
        db.session.commit()
