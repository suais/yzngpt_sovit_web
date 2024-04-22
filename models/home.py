from models.files import query_all
from models.base import Home
from models.base import File
from models.base import VoiceModel
from models.voice_models import query_all as models_query_all

def main():
    home = Home()
    files_rows = query_all()
    for row in files_rows:
        file = File()
        file.filename = row[0]
        file.size = row[1]
        file.lenght = row[2]
        file.text = row[3]
        file.create_at = row[4]
        file.id = row[5]
        file.status = row[6]
        file.path = row[7]
        home.files.append(file)
    
    voice_models = models_query_all()
    
    for row in voice_models:
        voice_model = VoiceModel()
        voice_model.id = row[0]
        voice_model.name = row[1]
        voice_model.api = row[2]
        home.models.append(voice_model)
    
    return home
    
    
    