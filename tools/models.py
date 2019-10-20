from django.db import models

# Create your models here.

class Tool(models.Model):
    name        = models.CharField(max_length=100)
    shop_day    = models.DateField(null=True, blank=True) 
    last_maintenance_day    = models.DateField(null=True, blank=True)
    next_maintenance_day    = models.DateField(null=True, blank=True)
    maintenance_done        = models.BooleanField(default=False)
    use         = models.IntegerField(default=0)
    
    #  def save(self, *args, **kwargs):
    #     super(GroutDiceBreak, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} is used {self.use} times"