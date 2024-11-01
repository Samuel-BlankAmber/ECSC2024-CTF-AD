import random
import string
import requests

def random_string(min_length=5, max_length=10, allowed_chars=None):

    if allowed_chars is None:
        allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\'()*+,-.:;<=>?@[]^_`{|}~ '

        if random.random() > 0.8:
            allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    length = random.randint(min_length, max_length)

    while True:
        res = ''.join(random.choice(allowed_chars) for i in range(length))
        if res[0] != '.':
            return res

class CheckException(Exception):
    def __init__(self, comment, debug):
        self._comment = comment
        self._debug = debug
    
    def __str__(self):
        return f'{self.comment}: {self.debug}'
    
    @property
    def comment(self):
        return self._comment
    
    @property
    def debug(self):
        return self._debug
    

    
class UserChallenge:
    def __init__(self, host, username=None, password=None):
        self.host = host
        self.port = '4960'
        self.sess = requests.Session()
        self.sess.headers.update({"User-Agent": "checker"})

        self.username = random_string(5, 50)
        self.password = random_string(5, 20)
        
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        
    def register(self):
        try:
            r = self.sess.post(f'http://{self.host}:{self.port}/api/register', json={'name': self.username, 'password': self.password})

            if r.status_code != 200:
                raise CheckException('Cannot register user', r.text)

        except Exception as e:
            raise CheckException('Cannot register user', str(e))
        
    def login(self):
        try:
            r = self.sess.post(f'http://{self.host}:{self.port}/api/login' , json={'name': self.username, 'password': self.password})

            if r.status_code != 200:
                raise CheckException('Cannot login', r.text)
        
        except Exception as e:
            raise CheckException('Cannot register user', str(e))
            
    def logout(self):
        self.sess = requests.Session()
        return True

    def get_challenge(self, user):
        try:
            r = self.sess.get(f'http://{self.host}:{self.port}/api/question/{user}')

            if r.status_code != 200:
                raise CheckException('Cannot get challenge', r.text)

            return r.json()
        except Exception as e:
            raise CheckException('Cannot get challenge', str(e))
    
    def create_challenge(self, challenge):
        try:
            r = self.sess.post(f'http://{self.host}:{self.port}/api/createchallenge', json=challenge)

            if r.status_code != 200:
                raise CheckException('Cannot create challenge', r.text)
            return r.json()['id']
        
        except Exception as e:
            raise CheckException('Cannot create challenge', str(e))
        
    def upload_file(self, url, filename):
        try:
            r = self.sess.post(f'http://{self.host}:{self.port}/api/upload', json={'url': url, 'filename': filename})

            if r.status_code != 200:
                raise CheckException('Cannot upload file', r.text)
            
        except Exception as e:
            raise CheckException('Cannot upload file', str(e))
        
    def get_qimage(self, qid):
        try:
            r = self.sess.get(f'http://{self.host}:{self.port}/api/qimages/{qid}')

            if r.status_code != 200:
                raise CheckException('Cannot get qimage', r.text)

            return r.content

        except Exception as e:
            raise CheckException('Cannot get qimage', str(e))
        
    def get_challenges(self, user):

        try:
            r = self.sess.get(f'http://{self.host}:{self.port}/api/challenges/' + user)

            if r.status_code != 200:
                raise CheckException('Cannot get challenges', r.text)

            return r.json()
        
        except Exception as e:
            raise CheckException('Cannot get challenges', str(e))