# Project Management App

## General Info About Project
- **Project Purpose** : Creating a project management app with fastapi . 
- **Project Time** : 2 day 
- **Project Database** : MongoDb
- **Used technologies** : Redis , Fastapi , Pymongo , Pydantic

### Features

- Register/Login 
- Password Reset
- Create Projects 
- Create Task under specific project
- Make Comment
- Get Projects/Task/Comments

### Limitations 
- User can be online until  token expires
- If send login requests when already logging , expiration date is renewed
- The token is deleted when it expires. After it re-login is required
- An email can not have more than one account 
- Account name is also required while resetting password
- People can create projects , can add owner users and viewer users
- Only users in owners list can create a task under the project
- Owners or viewers people can make comment in task
- Project names are unique 
- Task names are unique in same project . Task name may be same on different projects
- When the project will be saved, utc time uses for 'created' value in database
- Users can get information about the projects/tasks, they are added to in the owners/viewers list
- Users can get all user comments on specific project and task, but user must be in the project owners/viewers list
- Uses token and the token changes from session to session, so requests. Session should be used or cookie  should be used on requests 



![](https://camo.githubusercontent.com/38f5db5524ba43e7262dfbca1f7d3631ba127fb1596785dfd707d5fc671821c9/687474703a2f2f466f7254686542616467652e636f6d2f696d616765732f6261646765732f6d6164652d776974682d707974686f6e2e737667)

![](https://cdn.iconscout.com/icon/free/png-256/redis-3-1175053.png) ![](https://cdn.iconscout.com/icon/free/png-256/mongodb-5-1175140.png) ![](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)


**Table of Contents**

[TOCM]

[TOC]

#Project Details
##API 
Fastapi was used on API side .
Redis was used to set expiration time for tokens.
Fastapi_login was used to create token .
Pydantic was used to create models.

##Database
MongoDB was used for Database operations.
Inserting , finding , updating methods were  used.

##Config
Config file includes some arrangements.
On config.ini file :
- Token expiration time,
- Redis server configurations,
- Mongo server configurations,
- API response messages are adjustable.

##Client
A class has been created for clients to use the API.
Client can use clients.py to use API easily. Otherwise client can create own class with Requests . The cookie should be used because the API uses login cookies for login required functions.

# Example Codes

##Register
```python
client = Client()
client.register(name='John',surname='Survey',email='john@example.com',password='ExamplePassword')
```
If email was not taken , account creates.

## Login
```python
client = Client(email='john@example.com',password='ExamplePassword')
client.login()
```
## Password Reset
```python
client = Client()
client.password_reset(name='John',email='john@example.com',new_password='ExampleNewPassword')
```

##Create Project
```python
client.create_project(project_name='Example Project Name',
                      owners=['john@example.com','david@example.com'],
                      viewers=['lusia@example.com','danny@example.com'],
                      status='active',
                      startdate=datetime(2022,9,22,12,20,30),
                      enddate=datetime(2022,10,22,12,20,30))
```
- Data in owners/viewers must include @ symbol . Otherwise the project will not be created.
- Status must be active or archived . 
- Startdate and Enddate is not required . Default is None.
- When the project will be saved, utc time uses for 'created' value in database
##Create Task
```python
client.create_task(project_name='Example Project Name',title='Example Task Title',
                   content='Example Task Content',status='active',
                    owners=['john@example.com','david@example.com'],
                    viewers=['lusia@example.com','danny@example.com'],
                    startdate=datetime(2022,9,22,12,20,30),
                    enddate=datetime(2022,10,22,12,20,30))
```
- Project name must be exists in database.
- Only owners can create task in the project.
- Data in owners/viewers must include @ symbol . Otherwise the project will not be created.
- Startdate and Enddate is not required . Default is None.
- When the task will be saved, utc time uses for 'created' value in database
## Make Comment
```python
client.make_comment(project_name='Example Project Name',title='Example Task Title',
                    comment='Example Comment For This Task')
```
- When the comment will be saved, utc time uses for 'created' value in database
- Owners or viewers people can make comment in task
- Project name and task title must be exists in database.

## Get Data
### Get Owners Projects
```python
client.get_owner_projects()
```
### Get Viewers Projects
```python
client.get_viewer_projects()
```
Example Response:
```json
{
    '0': {
        'project_name': 'Example Proje Name',
        'status': 'active',
        'created': '2022-09-21T16:57:51.694000',
        'owners': ['jessica@example.com', 'dany@example.com'],
        'viewers': ['viewers@gmail.com', 'lusy@example.com', 'captain@example.com']
    },
    '1': {
        'project_name': 'Example Proje Name',
        'title': 'Example Title',
        'content': 'Example Content',
        'status': 'Created',
        'created': '2022-09-21T17:02:14.544000',
        'startdate': None,
        'enddate': None,
        'owners': ['jessica@example.com', 'dany@example.com'],
        'viewers': ['viewers@gmail.com', 'lusy@example.com', 'captain@example.com']
    },
    '2': {
        'project_name': 'Example Proje Name',
        'title': 'Example Title 2',
        'content': 'Example Content',
        'status': 'Created',
        'created': '2022-09-21T20:31:52.887000',
        'startdate': None,
        'enddate': None,
        'owners': ['jessica@example.com', 'dany@example.com'],
        'viewers': ['viewers@gmail.com', 'lusy@example.com', 'captain@example.com']
    }
}

```
### Get Owners Cart
```python
client.get_owner_tasks()
```

### Get Viewers Cart
```python
client.get_viewer_tasks()
```
Example Response:
```json
{
    'message': {
        '0': {
            'project_name': 'Example Project Name',
            'status': 'active',
            'created': '2022-09-21T16:57:51.694000',
            'owners': ['example2@example.com', 'jessica@example.com'],
            'viewers': ['danny@example.com', 'michael@example.com', 'david@example.com']
        },
        '1': {
            'project_name': 'Example Project Name',
            'title': 'Example Title',
            'content': 'Example Content',
            'status': 'Created',
            'created': '2022-09-21T20:31:52.887000',
            'startdate': None,
            'enddate': None,
            'owners': ['example2@example.com', 'jessica@example.com'],
            'viewers': ['danny@example.com', 'michael@example.com', 'david@example.com']
        },
        '2': {
            'project_name': 'Example Project Name 4',
            'status': 'active',
            'created': '2022-09-21T22:01:34.210000',
            'owners': ['example2@example.com', 'jessica@example.com'],
            'viewers': ['danny@example.com', 'michael@example.com', 'david@example.com']
        },
        '3': {
            'project_name': 'Example Project Name 4',
            'title': 'Example Title',
            'content': 'Example Content',
            'status': 'Created',
            'created': '2022-09-21T22:01:56.227000',
            'startdate': None,
            'enddate': None,
            'owners': ['example2@example.com', 'jessica@example.com'],
            'viewers': ['danny@example.com', 'michael@example.com', 'david@example.com']
        }
    }
}

```

### Get Comments
```python
client.get_comments(project_name='Example Project',title='Example Title')
```
Example Response:
```json
{
    'message': {
        '1': {
            'project_name': 'Example Project',
            'title': 'Example Title',
            'created': '2022-09-21T17:13:35.427000',
            'from': 'john@example.com',
            'comment': 'example comment 1'
        },
        '2': {
            'project_name': 'Example Project',
            'title': 'Example Title',
            'created': '2022-09-21T19:22:09.259000',
            'from': 'john@example.com',
            'comment': 'example comment 2'
        }
    }
}
```

