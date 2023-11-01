from .JsonFileManager import JSON_Manager

class TW_Manager(JSON_Manager):
    def __init__(self, path_file : str):
        super().__init__(path_file)

    def getAllGuilds(self):
        return self.data.keys()

    def getSettingsGuild(self, guild_id : str):
        return self.data[guild_id]["settings"].values()
    
    def getStreamersByGuildID(self, guild_id):
        return list(self.data[guild_id]["streamers"].keys())
    

    def getStreamerByID(self, streamer : str):
        return self.data["streamers"][streamer].values()
    
