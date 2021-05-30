from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                     "allowed.")

APPROVAL_CHOICES = (
    (u'1', u'opened'),
    (u'2', u'closed'),
    (u'2', u'canceled')
)


class Photo(models.Model):
    image = models.ImageField(upload_to='uploads/', blank=True)


class OrderMeta(models.Model):
    reward = models.IntegerField()
    order_date = models.DateTimeField('date order', blank=False)
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=APPROVAL_CHOICES)
    contact_email = models.EmailField()
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


class Order(models.Model):
    order_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    meta = models.ForeignKey(OrderMeta, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_date',)
