from django.db import models

# we haven't made any models for User
# but admin has it bydefault, grabbing it
# importing admin User
from django.contrib.auth.models import User



class Product(models.Model):

    title = models.CharField(max_length=200)
    url = models.TextField()
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    votes_total = models.IntegerField(default=1)

    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    # hunter is basically a user who has submitted a product
    # hunter is a id no. of the user who has submitted the product

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e, %Y')
