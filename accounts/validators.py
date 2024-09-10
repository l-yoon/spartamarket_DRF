from django.core.validators import validate_email
from .models import User
def validate_signup(signup_data):
    usename = signup_data.get("username")
    password = signup_data.get("password")
    nickname = signup_data.get("nickname")
    birth = signup_data.get("birth")
    first_name = signup_data.get("first_name")
    last_name = signup_data.get("last_name")
    email = signup_data.get("email")
    
    err_msg = []
    #username validation
    if User.objects.filter(username=usename).exists():
        err_msg.append("존재하는 유저네임입니다")
        
    #nickname validation
    if len(nickname) > 20:
        err_msg.append("닉네임은 20자 이하여야합니다")
    
    #email validation
    try:
        validate_email(email)
    except:
        err_msg.append("이메일 형식이 옮바르지 않습니다")

    if err_msg:
        return False, err_msg
    else:
        return True, None