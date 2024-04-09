from django import forms
from .models import tester_char_db

class LoginForm(forms.Form):
    user_code = forms.CharField(max_length=100, help_text="請輸入您的使用者名稱")
    password = forms.CharField(widget=forms.PasswordInput, help_text="請輸入您的密碼")


class UserCodeForm(forms.ModelForm):
    class Meta:
        model = tester_char_db
        fields = ['tester_code', 'tester_password', 'tester_birthday',
                  'tester_gender', 'tester_company', 'tester_position']

class SelectionForm(forms.Form):
    number_entered_1 = forms.CharField(required=False)
    number_entered_2 = forms.CharField(required=False)
    number_entered_3 = forms.CharField(required=False)

