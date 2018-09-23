import requests
from json import dumps

class User:

    def __init__(self,json_object):
        self.username = json_object["username"]
        self.locale = json_object["locale"]
        self.mfa_enabled = json_object["mfa_enabled"]
        self.avatar = json_object["avatar"]
        self.discriminator = json_object["discriminator"]
        self.id = json_object["id"]
        self.json = json_object
    
    '''
    gets the url of the user avatar
    size is between
    '''
    def get_avatar_url(self,size = 5) -> str:
        clamped_size = self.clamp(size,1,7)
        img_size = (2**(clamped_size+3))
        link = "https://cdn.discordapp.com/avatars/{}/{}.png?size={}".format(self.id,self.avatar,img_size)
        return link

    def clamp(self,value,min,max):
        if(value>max):
            return max
        if(value<min):
            return min
        else:
            return value

    def __str__(self):
        return dumps(self.json)
