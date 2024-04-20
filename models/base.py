class UserOnline(object):
    def __init__(self):
        self.uid = None
        self.username = None
        self.login_time = None
        self.login_length = None

    

class Users(object):
    def __init__(self):
        self.uid = None
        self.username = None
        self.password = None
        self.email = None
        self.last_login = None
        self.status = None
        self.is_admin = None


class Record(object):
    def __init__(self):
        self.id = None
        self.filename = None
        self.length = None
        self.size = None
        self.text = None
        self.uid = None
        self.create_at = None
        self.path = None
        
        
class File(object):
    def __init__(self):
        self.id = None
        self.filename = None
        self.size = None
        self.lenght = None
        self.text = None
        self.create_at = None
        self.status = None
        self.path = None
        

class Words(object):
    def __init__(self):
        self.id = None
        self.text = None
        self.edit_at = None
        
class SMS(object):
    def __init__(self):
        self.id = None
        self.uid = None
        self.username = None
        self.create_at = None
        self.msg = None
        self.phone = None

class Home(object):
    def __init__(self):
        self.files = [] # 语音
        self.models = [] # 模型
        self.user = None

class VoiceModel(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.api = None