from django.db import models
import uuid 



class Offenses(models.Model) : 
    offense_id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, null=True)
    offense = models.CharField(max_length=250, null=True,blank = True)
    name = models.CharField(max_length=250, null=True,blank = True)
    matric = models.CharField(max_length=250)
    department = models.CharField(max_length=250, null=True,blank = True)
    punishment = models.CharField(max_length=250)
    pardon = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    ongoing = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('offense',)


