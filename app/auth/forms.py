from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


"""
注册表单使用wtforms提供的Regexp验证函数，以一个正则为参数，确保昵称字段只包含汉子，字母，数字，下划线和点号。
后两个参数是正则的旗标和验证失败的错误信息。
注册表单有两个自定义的验证函数，以方法的形式实现。
如果表单类中定义了以validate_开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用。
"""

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('rememberme', default=False)


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    nickname = StringField('Nickname', validators=[
        DataRequired(), Length(1, 64), Regexp('^[\u4e00-\u9fa5]|[a-z]|[A-Z][0-9_.]*', 0,
                                          '昵称必须以汉字或字母开头')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='密码必须确认一致。')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册。')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经存在。')

# 更改密码表单
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='密码必须确认一致。')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])