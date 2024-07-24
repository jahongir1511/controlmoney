from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, default='unknown')

    def __str__(self):
        return f"{self.category} - {self.amount}"

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    source = models.CharField(max_length=100, default='unknown')

    def __str__(self):
        return f"{self.source} - {self.amount}"
