from fastapi_login import LoginManager 
from .redis_connect import *
from ..config import config
from typing import Union

session_expired_time = config.api.session_expired_time
message_object = config.messages
login_error , login_success , already_logen , invalid_credentials , account_created_success , account_created_error , project_created , project_exists , task_doesnt_access , task_taken , task_created , project_doesnt_exists , task_doesnt_exists , project_doesnt_access , comment_created_success , user_not_found , forgot_password_success , forgot_password_error = message_object.login_error , message_object.login_success , message_object.already_logen , message_object.invalid_credentials , message_object.account_created_success , message_object.account_created_error , message_object.project_created , message_object.project_exists , message_object.task_doesnt_access , message_object.task_taken , message_object.task_created , message_object.project_doesnt_exists , message_object.task_doesnt_exists , message_object.project_doesnt_access , message_object.comment_created_success , message_object.user_not_found , message_object.forgot_password_success , message_object.forgot_password_error

manager = LoginManager(
    'secret', '/login',
    use_cookie=True,
    cookie_name='secret'
)

async def check_login(secret:str) ->bool:
    '''
    if user is online , returns True , otherwise returns False 
    '''
    try:
        if redser.hgetall(secret)=={}:
            return False
        return True
    except :
        return False


async def get_email(secret:str) -> Union[bool,dict]:
    '''
    if secret(token) belong to an email , returns email , otherwise returns False
    '''
    try:
        query = redser.hgetall(secret)
        if query=={}:
            return False
        return query['email']
    except :
        return False


async def check_online(email:str) -> Union[bool,str]:
    '''
    if user is online , returns True , otherwise returns False 
    it checks with email so its not same with  check_login function
    '''
    try:
        token = redser.get(email)
        if token==None:
            return False #offline
        return token #online
    except:
        return False


async def create_token(email:str) -> str :
    token = manager.create_access_token(
        data=dict(sub=email)
    )   
    return token


async def set_token_expired_time(token:str,email:str,expired_time:int) ->None :
    redser.hmset(token,{'email':email}) 
    #The email of the token is recorded so that it can be understood who the person is with that token.
    redser.set(email,token) 
    #The token is kept online so that it cannot log in again while online, and cannot get new tokens.
    redser.expire(token,expired_time) #setting expiration time
    redser.expire(email,expired_time) #setting expiration time
    
