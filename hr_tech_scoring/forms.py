from django import forms
from .models import user_char_db
class SelectionForm(forms.Form):
    SCORE_CHOICES = [(0, '不適合'), (1, '適合'), (2, '非常適合')]

    score_1 = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, required=False)
    score_2 = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, required=False)
    score_3 = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, required=False)
    score_4 = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, required=False)
    score_5 = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, required=False)
    score_6 = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, required=False)
    marked = forms.BooleanField(required=False)
    notes = forms.CharField(max_length=100, help_text="備註", required=False)


class LoginForm(forms.Form):
    user_code = forms.CharField(max_length=100, help_text="請輸入數字及英文所組成的使用者名稱")
    password = forms.CharField(widget=forms.PasswordInput, help_text="請輸入您的密碼")

# class UserCodeForm(forms.ModelForm):
#     class Meta:
#         model = user_char_db
#         fields = ['user_code', 'user_password', 'user_birthday', 'user_gender', 'user_company', 'user_position']

