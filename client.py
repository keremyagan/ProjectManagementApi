from datetime import datetime
from typing import Optional
import requests


class Client() :
    
    def __init__(self , email:str=None , password:str=None ) :
        self.API_URL = 'http://127.0.0.1:8000/'
        self.session = requests.Session()
        self.email , self.password = email , password


    def _post(self,path:str,**kwargs) ->requests.Response :
        return self.session.post(self.API_URL+path,json=kwargs)


    def _get(self,path:str) ->requests.Response :
        return self.session.get(self.API_URL+path)
       
        
    def login(self) -> dict  :
        if (self.email == None) or (self.password == None) :
            return {'message':'Please Enter Valid Email/Password.'}
        return self._post('login/',email = self.email , password = self.password).json()


    def register(self , name:str , surname:str , email:str ,password:str) -> dict :
        return self._post('register/',name=name,surname=surname,email=email,password=password).json()
        
        
    def password_reset(self,name:str , email:str , new_password:str) -> dict :
        return self._post('password-reset/',name=name,email=email,new_password=new_password).json()
    
    
    def create_project(self,project_name:str ,owners:list ,
                viewers:list, status:str='active' , startdate : Optional[datetime]  = None , 
                enddate : Optional[datetime]  = None) -> dict :
    
        return self._post('create-project/',project_name=project_name,status=status,
                          owners=owners,viewers=viewers,startdate=startdate,enddate=enddate).json()


    def create_task(self,project_name:str, title:str , content:str ,owners:list ,
                viewers:list, status:str='active' , startdate : Optional[datetime]  = None , 
                enddate : Optional[datetime]  = None) -> dict :
    
        return self._post('create-task/',project_name=project_name,title=title,
                          content=content,status=status,
                          owners=owners,viewers=viewers,startdate=startdate,enddate=enddate).json()
        
        
    def get_owner_projects(self) ->dict :
        return self._get('get-owners-projects/').json()    


    def get_viewer_projects(self) ->dict :
        return self._get('get-viewers-projects/').json()       


    def get_owner_tasks(self) ->dict :
        return self._get('get-owners-tasks/').json()    


    def get_viewer_tasks(self) ->dict :
        return self._get('get-viewers-tasks/').json()     


    def make_comment(self,project_name:str , title:str , comment:str) ->dict :
        return self._post('make-comment/',project_name=project_name,title=title,comment=comment).json()


    def get_comments(self,project_name:str , title:str) -> dict :
        return self._get(f'get-comments/{project_name}/{title}').json() 
        

