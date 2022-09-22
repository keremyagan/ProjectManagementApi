from datetime import datetime

async def check_project(dict:dict) ->bool :
    '''
    Check project values.If all values are acceptable , returns True . Otherwise returns False.
    '''
    if list(dict.keys()) != ["project_name","status","created","owners","viewers"]:
        return False 
    if dict['status'] not in ['active','archived']:
        return False 
    if type(dict['owners']) != list :
        return False 
    if type(dict['viewers']) != list :
        return False  
    for i in dict['viewers'] :
        if '@' not in i :
            return False    
    for i in dict['owners'] :
        if '@' not in i :
            return False  
    return True


async def check_task(dict:dict) ->bool:
    '''
    Check task values.If all values are acceptable , returns True . Otherwise returns False.
    '''
    if list(dict.keys()) != ["project_name","title","content","status","startdate","enddate","created","owners","viewers"]:
        return False 
    if dict['status'] !='Created':
        return False 
    if type(dict['startdate']) in [datetime,None] :
        return False 
    if type(dict['enddate']) in [datetime,None] :
        return False  
    for i in dict['viewers'] :
        if '@' not in i :
            return False    
    for i in dict['owners'] :
        if '@' not in i :
            return False  
    return True
    