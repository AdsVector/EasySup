from easysup.manager.JsonFileManager import JSON_Manager

class LinksManager(JSON_Manager):
    def __init__(self, file_path):
        super().__init__(file_path=file_path)
    
    def search_link(self, key, social_name:str):
        for element in self.data[key]:
            if str(element.get('socialName')).lower() == social_name.lower():
                return element['socialName'], element['socialUrl']
        return None
    
    def add_element(self, key, element):
        return super().add_element([key], element, JSON_Manager.Modes.APPEND)
    
    def delete_elements(self, key, elements, field=None):
        return super().delete_elements([key], elements, field, JSON_Manager.Modes.APPEND)
    
