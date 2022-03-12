import redis
from configparser import ConfigParser

r = redis.StrictRedis(decode_responses=True)

parser = ConfigParser()
parser.read('values.ini')
cfg = parser['1678077614']

ApiID = cfg['7024625'] #==//آیپی آیدی
ApiHash = cfg['d6061fffbe83b7b09ea6aa96e3736'] #==//آیپی هش
Token = cfg['2020512988:AAH3DduaI6fLwqVTofcoHLBnkQs33P_YAFA'] #==//توکن

