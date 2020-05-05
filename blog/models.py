from django.db import models


# Create your models here.
class Blog(models.Model):
    post_id = models.AutoField
    title = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    head1 = models.CharField(max_length=500, default="")
    head1text = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=500, default="")
    head2text = models.CharField(max_length=5000, default="")
    subhead21 = models.CharField(max_length=500, default="")
    subhead21text = models.CharField(max_length=5000, default="")
    thumbnail = models.ImageField(upload_to="blog/images", default="")

    def __str__(self):
        return str(self.id)+". "+self.title
