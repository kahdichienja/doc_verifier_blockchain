from django.db import models

# Create your models here.
# creating univesity model.


class Institution(models.Model):
    institution_name = models.CharField(max_length=191)


    def __str__(self):
        return self.institution_name



class DocumentBlockModel(models.Model):

    name = models.CharField(max_length=191)
    id_number = models.CharField(max_length=191)
    kra_pin = models.CharField(max_length=191)

    email_address = models.CharField(max_length = 191) 
    huduma_number = models.CharField(max_length = 191) 
    profile_url = models.FileField(upload_to="profiles") 

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    date_of_graduation = models.CharField(max_length = 191) 
    course = models.CharField(max_length = 191) 

    file_url = models.FileField(upload_to="docs") 
    verified = models.BooleanField(default=True) 
    file_name = models.CharField(max_length = 191) 



    def __str__(self):
        return self.name
