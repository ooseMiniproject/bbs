# coding:utf-8
import json
from app import db
from . import main
from app.models import Thread, User
from flask import jsonify, request, Response


@main.route('/thread/', methods=['POST'])
def add_thread():
    if request.method == 'POST':
        data = request.get_json
        description = data.get("description")
        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(username=username).first()
        if user.verify_password(password):
            thread = Thread(
                    description=description,
                    user_id=user.id,
                    )
            db.session.add(thread)
            db.session.commit()
            return jsonify({"msg":"创建新板块成功！"}), 200    
        else:
            return jsconify({"msg":"用户验证失败！"})
