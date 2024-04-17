class UserOnlineRespone(object):
    def __init__(self) -> None:
        self.users = []
        
        
class UsersRespone(object):
    def __init__(self) -> None:
        self.users = []
        self.total_page = None
        self.localtion_page = None
        
class RecordRespone(object):
    def __init__(self) -> None:
        self.records = []
        self.total_page = None
        self.localtion_page = None
        

class FilesRespone(object):
    def __init__(self) -> None:
        self.files = []
        self.total_page = None
        self.localtion_page = None
        
class WordsRespone(object):
    def __init__(self):
        self.words = []
        

class SMSRespone(object):
    def __init__(self):
        self.SMSs = []
        self.total_page = None
        self.localtion_page = None