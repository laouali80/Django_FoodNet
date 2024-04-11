from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class RegisterForm(forms.Form):
    # def validate_username(self, username_to_check):
    #     user = User.query.filter_by(username=username_to_check.data).first()

    #     if user:
    #         raise ValidationError('This Username Already exists! Please try a different username.')


    # def validate_email_address(self, email_address_to_check):
    #     email_address = User.query.filter_by(email=email_address_to_check.data).first()

    #     if email_address:
    #         raise ValidationError(' This Email Address Already exists! Please try a different email address.')
    
    username = forms.CharField(label='Username')
    email_address = forms.EmailField(help_text="A valid email address, please.", label='Email Adress')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    # password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    
    # title = forms.CharField(label="Title")
    # description = forms.CharField(widget=forms.Textarea, label="Description", required=False)
    # price = forms.IntegerField(label="Initial Price", validators=[MinValueValidator(1)])
    # img_url = forms.URLField(label="Img URL(optional)", required=False)
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control',
                                                                  'placeholder':'Username', 'required':'True'}))
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'placeholder':'password', 'required':'True', 
                                                                  'max_length':'80', 'render_value':'False'}))
    
#     def __init__(self, *args, **kwargs):
#         super(BidForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'

# class AddCommentForm(forms.Form):
#     comment = forms.CharField(widget=forms.Textarea, label="Add a comment")

#     def __init__(self, *args, **kwargs):
#         super(AddCommentForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
