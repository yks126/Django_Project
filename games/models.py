from django.db import models
import random
from django.utils import timezone
# Create your models here.
class tester_char_db(models.Model):
    # 定義您的字段
    tester_code = models.CharField(max_length=100)
    tester_password = models.CharField(max_length=100)
    tester_name = models.CharField(max_length=100)
    tester_birthday = models.CharField(max_length=100)
    tester_gender = models.CharField(max_length=100)
    tester_company = models.CharField(max_length=100)
    tester_position = models.CharField(max_length=100)
    tester_jobtype = models.CharField(max_length=100)
    tester_workyear = models.CharField(max_length=100)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tester_char"

class tester_bomb_score_db(models.Model):
    # 定義您的字段
    tester_code = models.CharField(max_length=100)
    current_round = models.IntegerField(default=0)
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_3 = models.IntegerField(default=0)
    score_4 = models.IntegerField(default=0)
    score_5 = models.IntegerField(default=0)
    bomb_1 = models.IntegerField(default=random.randint(6, 10))
    bomb_2 = models.IntegerField(default=random.randint(35, 45))
    bomb_3 = models.IntegerField(default=random.randint(35, 45))
    bomb_4 = models.IntegerField(default=random.randint(35, 45))
    bomb_5 = models.IntegerField(default=random.randint(35, 45))
    last_modify_date = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tester_bomb_score"

class tester_numerosity_score_db(models.Model):
    # 定義您的字段
    tester_code = models.CharField(max_length=100)
    score = models.IntegerField(null=True,default=0)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tester_numerosity_score"



class tester_set_score_db(models.Model):
    # 定义您的字段
    tester = models.ForeignKey(tester_char_db, on_delete=models.CASCADE, null=True)
    tester_code = models.CharField(max_length=100)
    correct = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
    wrong = models.IntegerField(default=0)
    skipped_count = models.IntegerField(default=0)
    answered_count = models.IntegerField(default=0)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "tester_set_score"

class PageVisit(models.Model):
    tester = models.ForeignKey(tester_char_db, on_delete=models.CASCADE, null=True)
    enter_time = models.DateTimeField(default=timezone.now)
    leave_time = models.DateTimeField(null=True, blank=True)
    stay_time = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=255, null=True, blank=True)