from aiohttp import ClientSession
from io import BytesIO
from bs4 import BeautifulSoup
from config import r
import lxml
import random
import string

# -- Fake Generator Functions
admins = [121, 56454, 78787, 416340608]

async def generate_pfp() -> BytesIO:
    '''
    Generate a random profile picture from ThisPersonDoesntExist Website.
    '''
    async with ClientSession() as session:
        async with session.get('https://thispersondoesnotexist.com/image') as data:
            _io = BytesIO(await data.read())
            _io.name = 'pfp.jpg'
            return _io


async def generate_info() -> str:
    '''
    Generate random information about a user using fake-it.ws
    '''
    country_list = ['de', 'it', 'ca', 'us', 'au', 'nl']
    async with ClientSession() as session:
        async with session.get(f'https://fake-it.ws/{random.choice(country_list)}') as data:
            raw_data = await data.read()
            name = BeautifulSoup(raw_data, features='lxml').select(
                'div:nth-of-type(1) .row tr:nth-of-type(1) td:nth-of-type(2)')[0].text
            return(name)


async def generate_bio() -> str:
    '''
    Generate random words for bio.
    '''
    async with ClientSession() as session:
        async with session.get(f'http://metaphorpsum.com/sentences/1') as data:
            bio = await data.read()
            return(str(bio.decode('utf-8'))[:70])


async def generate_string(lenght: int = None) -> str:
    '''
    Generate random string for passwords/etc...
    '''
    letters = string.ascii_letters + string.digits
    return(''.join(random.choice(letters) for _ in range(lenght)))


async def generate_username(lenght: int = None) -> str:
    '''
    Generate random string for username -starting with a letter-...
    '''
    x = random.choice(string.ascii_letters)
    letters = string.ascii_letters + string.digits
    for i in range(lenght):
        x += random.choice(letters)
    return(x)

# -- Bot Related Functions


def verify_sudo(user_id: int = None) -> bool:
    '''
    Check given `user_id` in `sudos` Database.
    '''
    #  return(str(user_id) in list(r.smembers('admins')))
    
    if user_id in admins:
         return True
    else:
       return False


def verify_admin(user_id: int = None) -> bool:
    '''
    Check given `user_id` in `admins` Database.
    '''
  #  return(str(user_id) in list(r.smembers('admins')))

    if user_id in admins:
         return True
    else:
       return False



def all_check(user_id: int = None) -> bool:
    '''
    Return `True` for all given queries // All check for regular users.
    '''
    return(True)


def add_to_user(user_id: int = None) -> int:
    if str(user_id) not in list(r.smembers('adders')):
        r.sadd('adders', user_id)
    last = r.get(user_id)

    if not last:
        r.set(user_id, 1)
        return(1)
    else:
        new = int(last) + 1
        r.set(user_id, new)
        return(new)


def calc_banner(banner_id: str = None, status: int = None):
    '''
    1 ==> Adds One Success to `banner_id`.\n
    2 ==> Adds One Fail to `banner_id`.\n
    3 ==> Adds One Fail & Reported Account to `banner_id`.\n
    '''

    info = r.get(banner_id).split('//')
    success = info[0]
    fail = info[1]
    rep = info[2]
    stime = info[3]

    if status == 1:
        new_succ = int(success) + 1
        r.set(banner_id, f'{new_succ}//{fail}//{rep}//{stime}')
    elif status == 2:
        new_fail = int(fail) + 1
        r.set(banner_id, f'{success}//{new_fail}//{rep}//{stime}')
    elif status == 3:
        new_fail = int(fail) + 1
        new_rep = int(rep) + 1
        r.set(banner_id, f'{success}//{new_fail}//{new_rep}//{stime}')
