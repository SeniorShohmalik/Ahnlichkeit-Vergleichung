from django.db import models

class Y_ISH(models.Model):
    nomzod = models.CharField(max_length=200)
    pdf_ish = models.FileField(upload_to='pdf/' ,blank=False,null=False)

    def __str__(self) :
        return self.nomzod
