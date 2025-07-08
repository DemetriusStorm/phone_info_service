from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneNumber(models.Model):
    full_number = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10)
    number = models.CharField(max_length=20)
    operator = models.CharField(max_length=100)
    old_operator = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_number} ({self.operator})"


class QueryHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
    query_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Query Histories"
        ordering = ['-query_date']

    def __str__(self):
        return f"{self.phone_number.full_number} queried at {self.query_date}"