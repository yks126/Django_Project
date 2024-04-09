from django.db import models

class user_char_db(models.Model):
    # 定義您的字段
    user_code = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    # user_name = models.CharField(max_length=100)
    # user_birthday = models.CharField(max_length=100)
    # user_gender = models.CharField(max_length=100)
    # user_company = models.CharField(max_length=100)
    # user_position = models.CharField(max_length=100)
    # user_jobtype = models.CharField(max_length=100)
    # user_workyear = models.CharField(max_length=100)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_char"

class resume_scores_db(models.Model):
    # Define your fields
    user_code = models.CharField(max_length=100)
    row_id = models.CharField(max_length=100)
    score_1 = models.IntegerField(null=True, default=None)  # Allow null and default to None
    score_2 = models.IntegerField(null=True, default=None)
    score_3 = models.IntegerField(null=True, default=None)
    score_4 = models.IntegerField(null=True, default=None)
    score_5 = models.IntegerField(null=True, default=None)
    score_6 = models.IntegerField(null=True, default=None)
    marked = models.BooleanField(default=False)
    notes = models.CharField(null=True, max_length=100, default='')
    expand_edu = models.IntegerField(default=0)
    expand_experience = models.IntegerField(default=0)
    expand_intro = models.IntegerField(default=0)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "resume_scores"
