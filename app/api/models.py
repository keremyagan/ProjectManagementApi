from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from .helpers import *

class UserLogin(BaseModel):
    email: str = Field(example="example@example.com")
    password: str = Field(example="examplePassword")
    class Config:
        schema_extra = {
        "example": {
            "email": "example@example.com",
            "password": "examplepassword"
        }
        }

class UserLoginResponse(BaseModel):
    message: str = Field(example=already_logen)

class PasswordResetResponse(BaseModel):
    message: str = Field(example=forgot_password_success)

class UserRegisterResponse(BaseModel):
    message: str = Field(example=account_created_success)

class ProjectResponse(BaseModel):
    message: str = Field(example=project_created)

class TaskResponse(BaseModel):
    message: str = Field(example=task_doesnt_access)

class ProjectsDetails(BaseModel):
    message = {'0': {'project_name': 'Example Proje Name', 'status': 'active', 'created': '2022-09-21T16:57:51.694000', 'owners': ['jessica@example.com', 'dany@example.com'], 'viewers': ['viewers@gmail.com', 'lusy@example.com', 'captain@example.com']}, '1': {'project_name': 'Example Proje Name', 'title': 'Example Title', 'content': 'Example Content', 'status': 'Created', 'created': '2022-09-21T17:02:14.544000', 'startdate': None, 'enddate': None, 'owners': ['jessica@example.com', 'dany@example.com'], 'viewers': ['viewers@gmail.com', 'lusy@example.com', 'captain@example.com']}, '2': {'project_name': 'Example Proje Name', 'title': 'Example Title 2', 'content': 'Example Content', 'status': 'Created', 'created': '2022-09-21T20:31:52.887000', 'startdate': None, 'enddate': None, 'owners': ['jessica@example.com', 'dany@example.com'], 'viewers': ['viewers@gmail.com', 'lusy@example.com', 'captain@example.com']}}

class CommentResponse(BaseModel):
    message: str = Field(example=comment_created_success)

class GetComments(BaseModel):
    message: dict = {'message': {'1': {'project_name': 'Example Proje', 'title': 'Example Title', 'created': '2022-09-21T17:13:35.427000', 
'from': 'john@example.com', 'comment': 'example comment 1'}, '2': {'project_name': 'Example Proje', 'title': 'Example Title', 'created': '2022-09-21T19:22:09.259000', 'from': 'john@example.com', 'comment': 'example comment 2'}}}

class UserRegister(BaseModel):
    email: str = Field(example="example@example.com")
    password: str = Field(example="examplePassword")
    name : str  = Field(example="John")
    surname : str = Field(example="John")
    class Config:
        schema_extra = {
        "example": {
            "email": "example@example.com",
            "password": "examplepassword",
            "name" : "John",
            "surname" : "Joe"
        }
    }

class Project(BaseModel):
    project_name: str = Field(example="Example Project Name")
    status: str = Field(default='active', example="archived")
    owners : list  = Field(example=["john@example.com","marry@example.com"])
    viewers : list = Field(example=["jessica@example.com"])
    class Config:
        schema_extra = {
        "example": {
            "project_name": "Example Project Name",
            "status": "active",
            "owners" : ["john@example.com","marry@example.com"],
            "viewers" : ["jessica@example.com"]
        }
    }
    
class Task(BaseModel) :
    project_name: str = Field(example="Example Project Name")
    title: str = Field(example="Example Title")
    content: str = Field(example="Example Content")
    owners : list  = Field(example=["john@example.com","marry@example.com"])
    viewers : list = Field(example=["jessica@example.com"])
    startdate : Optional[datetime]  =  Field(default=None, example=datetime(2022,9,21,20,15,10))
    enddate : Optional[datetime]  =  Field(default=None, example=datetime(2022,10,21,20,15,10))
    class Config:
        schema_extra = {
        "A Normal Example": {
            "project_name": "Example Project Name",
            "title": "Example Title" ,
            "content": "Example Content",
            "status": "active",
            "owners" : ["john@example.com","marry@example.com"],
            "viewers" : ["jessica@example.com"] ,
            "startdate" : datetime(2022,9,21,20,15,10) ,
            "enddate" : datetime(2022,10,21,20,15,10)
        } 
    }

class Comment(BaseModel) :
    project_name: str  = Field(example="Example Project Name")
    title: str =  Field(example="Example Title")
    comment: str =  Field(example="Example Comment")
    class Config:
        schema_extra = {
        "example": {
            "project_name": "Example Project Name",
            "title": "Example Title",
            "comment" : "Example Comment"
        }
    }

class PasswordReset(BaseModel):
    email: str = Field(example="example@example.com")
    name : str = Field(example="John")
    new_password : str = Field(example="ExampleNewPassword10")
    class Config:
        schema_extra = {
        "example": {
            "email": "john@example.com",
            "name": "John",
            "new_password" : "ExampleNewPassword10"
        }
    }