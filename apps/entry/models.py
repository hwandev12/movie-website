from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["name"]
    
    def __str__(self):
        months = [
            "Yanvar", "Fevral", "Mart", "Aprel", "May",
            "Iyun", "Iyul", "Avgust", "Sentabr", "Oktyabr", 
            "Noyabr", "Dekabr"
        ]
        time_diff = self.time_created
        
        days = time_diff.day
        month = time_diff.month
        hours = time_diff.hour
        minute = time_diff.minute
        second = time_diff.second
        return "%s kategoriyasi %s - %s %s:%s:%s soniyada yaratildi" % (
            self.name,
            days,
            months[month],
            hours,
            minute,
            second
        )

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_category")
    name = models.CharField(max_length=110)
    time_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ["name"]
    
    def __str__(self):
        time_diff = timezone.now() - self.time_created
        
        days = time_diff.days
        hours, reminder = divmod(time_diff.seconds, 3600)
        minutes, _ = divmod(reminder, 60)
        return "%s kategoriyasi %s kun %s soat %s daqiqada yaratildi" % (
            self.category,
            days,
            hours,
            minutes
        )