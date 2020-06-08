from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('请输入用户名', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('修改')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名必须是字母，数字，标点，下划线')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('身份', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('修改')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    body = PageDownField("正文", validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    body = StringField('发表评论', validators=[DataRequired()])
    submit = SubmitField('发表:')
