from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    contact = models.IntegerField()

    def __str__(self):
        return self.name
        

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE ,related_name='company_name')

    class Meta:
        db_table = 'contacts'
