import redis
from ..config import config

host , port , db , password = str(config.redis.host) , int(config.redis.port) , int(config.redis.db) ,  str(config.redis.password) if str(config.redis.password)!='0' else None

redser = redis.StrictRedis(host=host,port=port, db=db,password=password,decode_responses=True)
