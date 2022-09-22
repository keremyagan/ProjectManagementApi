from .connect import *
from .helpers import *
from datetime import datetime
db = config.mongo.db
table = config.mongo.table

async def is_user(email , password) ->bool :
    '''
    It checks any data is exists which has the email and password.
    If exists returns True , otherwise returns False
    '''
    try:
        client = await connect_to_db()
        if client[db][table].find_one({'email': email,'password':password}) != None :
            await close_db_connection(client)
            return True #user found in db
        return False #user doesnt have any account
    except  :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def create_user(name,surname,email , password) ->bool :
    try:
        client =await connect_to_db()
        details = {
            'name':name ,
            'surname' : surname,
            'email' : email,
            'password' : password
        }
        client[db][table].insert_one(details)
        await close_db_connection(client)
        return True
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def check_user_exists(email) ->bool :
    '''
    It checks any data is exists which has the email .
    If exists returns True , otherwise returns False
    '''
    try:
        client = await connect_to_db()
        if client[db][table].find_one({'email': email}) != None :
            await close_db_connection(client)
            return True #user found in db
        return False #user doesnt have any account
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def check_project_exists(project_name) ->bool :
    '''
    If project is exists returns True , otherwise returns False
    '''
    try:
        client = await connect_to_db()
        if client[db][table].find_one({'project_name': project_name}) != None :
            await close_db_connection(client)
            return True #project found in db
        return False #project doesnt exists
    except :
        try:await close_db_connection(client) 
        except:pass
        return False   


async def project_authorized_people(project_name:str)  ->Union[bool,dict]:
    '''
    It returns project owners list . Users in list have authorized in project.
    If an error occurs or something goes wrong , returns False.
    '''
    try:
        client = await connect_to_db()
        query = client[db][table].find_one({'project_name': project_name})
        if query != None :
            await close_db_connection(client)
            return query['owners']
        return False #project doesnt exists
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def task_authorized_people(project_name:str,title:str)  ->Union[bool,dict]:
    '''
    It returns task owners and viewers list . Users in list have authorized in task under the project.
    If an error occurs or something goes wrong , returns False.
    '''
    try:
        client = await connect_to_db()
        query = client[db][table].find_one({'project_name': project_name,'title':title})
        if query != None :
            await close_db_connection(client)
            return query['owners']+query['viewers']
        return False #project or task doesnt exists
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def get_user_projects(email:str,project_type:str='owners',
                            project_or_task:str='project') ->Union[bool,dict] :
    '''
    Returns projects owned by the user.
    If an error occurs or something goes wrong , returns False.
    '''
    try:
        client = await connect_to_db()
        queries = client[db][table].find({project_type: email})
        data = {}
        for n,query in enumerate(queries) :
            try :
                if project_or_task == 'project':
                    query['title'] #if it includes 'title' , it is a task
                else:
                    #task
                    details = {
                    'project_name':query["project_name"] ,
                    'title' : query['title'],
                    'content':query['content'],
                    'status' : query["status"], 
                    'created' : query["created"], 
                    'startdate' : query['startdate'],
                    'enddate' : query['enddate'],
                    'owners' : query["owners"], 
                    'viewers' : query["viewers"] 
                        }
                    data[n] = details                   
            except:#project
                details = {
                'project_name':query["project_name"] ,
                'status' : query["status"], 
                'created' : query["created"], 
                'owners' : query["owners"], 
                'viewers' : query["viewers"] 
                    }
                data[n] = details
        await close_db_connection(client)
        return data
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def create_project(project_name:str,status:str , owners:list,viewers:list) -> bool :
    '''
    Creates project. If everything is fine , returns True , Otherwise returns false.
    '''
    try:
        client =await connect_to_db()
        details = {
            'project_name':project_name ,
            'status' : status, 
            'created' : datetime.utcnow(), 
            'owners' : owners,
            'viewers' : viewers 
        }
        if await check_project(details) :
            client[db][table].insert_one(details)
            return True
        await close_db_connection(client)
        return False
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 
    
    
async def check_task_exists(project_name:str,title:str) -> bool :
    '''
    If task exists, returns True . Otherwise returns False.
    '''
    try:
        client = await connect_to_db()
        if client[db][table].find_one({'project_name': project_name,'title':title}) != None :
            await close_db_connection(client)
            return True #task found in db
        return False #task doesnt exists
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def create_task(project_name:str,title:str,content:str,owners:list,
                      viewers:list , startdate:datetime=None,enddate:datetime=None) ->bool :
    '''
    Creates task. If everything is fine , returns True , Otherwise returns false.
    '''
    try:
        client =await connect_to_db()
        details = {
            'project_name' : project_name ,
            'title':title ,
            'content' : content ,
            'status' : 'Created', 
            'startdate' : startdate, 
            'enddate' : enddate,
            'created' : datetime.utcnow(), 
            'owners' : owners, 
            'viewers' : viewers 
        }
        if await check_task(details) :
            client[db][table].insert_one(details)
            return True
        await close_db_connection(client)
        return False
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 
      
       
async def make_comment(email:str,project_name:str,title:str , comment:str) ->bool :
    '''
    Makes comment. If everything is fine , returns True , Otherwise returns false.
    '''
    try:
        client =await connect_to_db()
        details = {
            'project_name':project_name ,
            'title' : title,
            'created' : datetime.utcnow(), 
            'from' : email, 
            'comment' : comment
        }
        client[db][table].insert_one(details)
        await close_db_connection(client)
        return True
    except :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def password_reset(email:str,name:str,new_password:str) ->bool :
    '''
    Resets password. If everything is fine , returns True , Otherwise returns false.
    '''
    try:
        client =await connect_to_db()
        filter = {'email':email,'name':name}
        newvalues = { "$set": {'password':new_password} }
        client[db][table].update_one(filter,newvalues)
        await close_db_connection(client)
        return True
    except  :
        try:await close_db_connection(client) 
        except:pass
        return False 


async def get_task_comments(project_name:str,title:str) ->Union[bool,dict] :
    '''
    Get task comments and return it in dictionary. If any error occurs returns False.
    '''
    try:
        client = await connect_to_db()
        queries = client[db][table].find({'project_name': project_name,'title':title})
        data = {}
        for n,query in enumerate(queries) :
            try :
                query['comment'] 
                details = {
                'project_name':query["project_name"] ,
                'title' : query['title'],
                'created' : query["created"], 
                'from' : query['from'],
                'comment' : query['comment']
                    }
                data[n] = details                   
            except:
                pass
        await close_db_connection(client)
        return data
    except  :
        try:await close_db_connection(client) 
        except:pass
        return False 