from fastapi import  Response,Cookie
from .models import *
from .app import app
from .helpers import *
from ..db.database import *

@app.get("/")
async def root():
    '''
    Homepage of app.
    '''
    return {'message':'Welcome to the app.'}


@app.post('/login/',response_model=UserLoginResponse)
async def login(user: UserLogin,response: Response):
    '''
    Login is required to use all functions.
    
    After logging in, a token is generated and it has an expiration date.
     
    The token is deleted when it expires. After it re-login is required.
    
    If send login requests when already logging , expiration date is renewed.
    
    '''
    token = await check_online(user.email)
    if  token :
        await set_token_expired_time(token,user.email,int(session_expired_time))
        manager.set_cookie(response, token)
        #if user is logged in and submits login request again
        #token expired time is sets again
        return {'message':already_logen}

    if await is_user(user.email,user.password):
        #if the user is not logged in and has an account, the token is created
        token = await create_token(user.email)
        await set_token_expired_time(token,user.email,int(session_expired_time))
        manager.set_cookie(response, token)
        return {'message':login_success}
    return {'message':invalid_credentials}


@app.post('/password-reset/',response_model=PasswordResetResponse)
async def forgot_password_(user: PasswordReset):
    '''
    If there is a valid account , the password of that account is changed to a new one .
    
    In order to ensure security , the name information verification of the account is required.
    '''
    if  await check_online(user.email) : 
        #if user online , cant reset password
        return {'message':already_logen}
    if not await check_user_exists(user.email) :
        #if email doesnt exists , returns a message
        return {'message':user_not_found}
    if await password_reset(user.email,user.name,user.new_password):
        #if information is valid , password will change . Otherwise there is no changes
        return {'message':forgot_password_success}
    return {'message':forgot_password_error}


@app.post('/register/',response_model=UserRegisterResponse)
async def register(user: UserRegister):
    '''
    If email doesnt exists , an account is created according to coming parameters
    '''
    if not await check_user_exists(user.email) : #email checking
        result = await create_user(user.name,user.surname,user.email,user.password)
        if result :
            return {'message':account_created_success}
        else :
            return {'message':'error'}
    return {'message':account_created_error}
 
 
@app.post('/create-project/',response_model=ProjectResponse)
async def create_project_(project: Project,secret: Optional[str] = Cookie(None)):
    '''
    It creates project. Project must have some features such as :
    
    :project_name 
    
    :status : 'active' or 'archived'. Otherwise the project will not be created
    
    :owners : it contains emails as a string in a list . If email doesnt have @ symbol the project will not be created
    
    :viewers : it contains emails as a string in a list . If email doesnt have @ symbol the project will not be created
    
    When the project will be saved, utc time uses for 'created' value in database.
    '''
    is_login =await check_login(secret)
    if not is_login : #login check
        return {'message':login_error}    

    if not await check_project_exists(project.project_name) :
        #if project is exists , cant create project with same name
        result = await create_project(project.project_name,project.status,project.owners,project.viewers)
        if result :
            return {'message':project_created}
        else :
            return {'message':'error'}
    return {'message':project_exists}


@app.post('/create-task/',response_model=TaskResponse)
async def create_task_(task: Task,secret: Optional[str] = Cookie(None)):
    '''
    It creates task under the project .
    
    Cant find task with same name on same project.
    
    Only project owners can create task under the project. 
    '''
    is_login =await check_login(secret)
    if not is_login :
        return {'message':login_error}    
   
    if  await check_project_exists(task.project_name) :
        email = await get_email(secret)
        if not email in await project_authorized_people(task.project_name) :
            #if email not in owners list , user cant create any task on this project
            return {'message':task_doesnt_access}

        if await check_task_exists(task.project_name,task.title) :
            #if task is exists , cant create task with same name
            return {'message':task_taken}
        
        result = await create_task(task.project_name,task.title,task.content,
                                   task.owners,task.viewers,task.startdate,task.enddate)
        if result :
            return {'message':task_created}
        else :
            return {'message':'error'}
    return {'message':project_doesnt_exists}


@app.get("/get-{get_type}-{project_or_task}/",response_model=ProjectsDetails)
async def get_owner_projects(get_type:str,project_or_task:str,secret: Optional[str] = Cookie(None)):
    ''' It returns their owner/viewer projects/tasks .

    get_type = owners or viewers 
    
    project_or_task = projects or tasks
    '''
    is_login =await check_login(secret)
    if not is_login :
        return {'message':{'error':login_error}} 
    email = await get_email(secret)
    return {'message' :await get_user_projects(email,get_type,project_or_task)}


@app.post('/make-comment/',response_model=CommentResponse)
async def make_comment_(comment: Comment,secret: Optional[str] = Cookie(None)):
    '''
    User can comment on task under the project but user must be in owners or viewers list in task.
    '''
    is_login =await check_login(secret)
    if not is_login :
        return {'message':login_error}    
   
    if  not await check_project_exists(comment.project_name) :
        return {'message':project_doesnt_exists}
    
    if not await check_task_exists(comment.project_name,comment.title) :
        return {'message':task_doesnt_exists}
    
    email = await get_email(secret)
    if not email in await task_authorized_people(comment.project_name,comment.title) :
        return {'message':project_doesnt_access}

    result = await make_comment(email,comment.project_name,comment.title,comment.comment)
    if result :
        return {'message':comment_created_success}
    else :
        return {'message':'error'}
       
       
@app.get('/get-comments/{project_name}/{title}',response_model=GetComments)
async def get_comments_(project_name:str,title:str,secret: Optional[str] = Cookie(None)):
    '''
    Returns all user comments on specific project and task
    '''
    is_login =await check_login(secret)
    if not is_login :
        return {'message':{'error':login_error}}   
   
    if  not await check_project_exists(project_name) :
        return {'message':{'error':project_doesnt_exists}} 
    
    if not await check_task_exists(project_name,title) :
        return {'message':{'error':task_doesnt_exists}} 
    
    email = await get_email(secret)
    if not email in await project_authorized_people(project_name) :
        return {'message':{'error':project_doesnt_access}} 

    return {'message':await get_task_comments(project_name,title)}
