from django.db import models

# Create your models here.
class currency_data(models.Model):
    uploaded_note = models.ImageField()
    pred = models.CharField(max_length=50)

    def __str__(self) -> str:
        return super().__str__()
