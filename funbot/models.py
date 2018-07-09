from django.db import models

class UserChat(models.Model):
    chat_id = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    button = models.CharField(max_length=7)
    numberofcalls = models.IntegerField(default=0)

    def __str__(self):
        return "{} {} {} - {}".format(self.first_name,self.last_name,self.button,self.numberofcalls)