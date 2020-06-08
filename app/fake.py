from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Thread


def users(count=100):
    fake = Faker('zh_CN')
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='123456',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date(),
                 )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker('zh_CN')
    user_count = User.query.count()
    thread_count = Thread.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        t = Thread.query.offset(randint(0, thread_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u,
                 thread_id=t,
                 )
        db.session.add(p)
        db.session.commit()


def threads(count=20):
    fake = Faker('zh_CN')
    user_count = User.query.count()

    t0 = Thread(description="测试板块",
                user_id=1,
                name="测试板块"
                )
    db.session.add(t0)
    db.session.commit()

    for i in range(2, count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        t = Thread(description=fake.text(),
                   user_id=u.id,
                   name=f"第{i}板块"
                   )
        db.session.add(t)
    db.session.commit()
