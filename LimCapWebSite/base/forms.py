from django import forms
from .models import User, Course
from django.contrib.auth.forms import UserCreationForm
from .models import genders, countryCodeList

passwordLength = 6


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", min_length=3, max_length=20, required=True,
                                 widget=forms.TextInput(attrs={
                                     "placeholder": "John...",
                                     "style": "min-width:80%",
                                 }))
    last_name = forms.CharField(label="Last Name", min_length=3, max_length=20, required=True,
                                widget=forms.TextInput(attrs={
                                    "placeholder": "Doe...",
                                    "style": "min-width:80%",
                                }))
    gender = forms.CharField(label="Select Gender", required=True, widget=forms.Select(choices=genders, attrs={
        "style": "min-width:80%",
    }))
    course = forms.CharField(label="Select Course", required=True, widget=forms.Select(attrs={
        "placeholder": "Select Course"
    }))
    countryCode = forms.CharField(label="Telphone", initial="+234", required=True,
                                  widget=forms.Select(choices=countryCodeList, attrs={
                                      "style": "min-width:50%",
                                  }))
    phoneNumber = forms.CharField(label="", min_length=5, max_length=15, required=True,
                                  widget=forms.TextInput(attrs={
                                      "style": "min-width:100%",
                                      #   "style": "margin-right: 0em",
                                      "placeholder": "Phone",
                                  }))
    email = forms.CharField(label="E-Mail", min_length=7, max_length=30, required=True,
                            widget=forms.EmailInput(attrs={
                                "placeholder": "johndoe@mail.com",
                                "style": "min-width:80%",
                            }))

    username = forms.CharField(label="Username", min_length=3, max_length=20, required=True,
                               widget=forms.TextInput(attrs={
                                   "placeholder": "johndoe...",
                                   "style": "min-width:80%",
                               }))
    password1 = forms.CharField(label="Password", min_length=passwordLength, required=True,
                                widget=forms.PasswordInput(attrs={
                                    "placeholder": "Password",
                                    "style": "min-width:80%",
                                }))
    password2 = forms.CharField(label="Confirm Password", min_length=passwordLength, required=True,
                                widget=forms.PasswordInput(attrs={
                                    "placeholder": "Confirm Password",
                                    "style": "min-width:80%",
                                }))
    avatar = forms.ImageField(label="Select Profile Picture", required=False, widget=forms.FileInput(attrs={
        "placeholder": "Choose File",
        "style": "max-width:100%",
        # "style": "margin-right:50%",
    }))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender", "course", "countryCode",
                  "phoneNumber", "email", "username", "password1", "password2",
                  "avatar"
                  ]


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name",
                                 widget=forms.TextInput(attrs={
                                     "placeholder": "John...",
                                     "style": "min-width:80%",
                                 }))
    last_name = forms.CharField(label="Last Name",
                                widget=forms.TextInput(attrs={
                                    "placeholder": "Doe...",
                                    "style": "min-width:80%",
                                }))
    gender = forms.CharField(label="Select Gender", required=True,
                             widget=forms.Select(choices=genders, attrs={
                                 "style": "min-width:80%",
                             }))
    course = forms.CharField(label="Select Course", required=True, widget=forms.Select(attrs={
        "placeholder": "Select Course"
    }))
    countryCode = forms.CharField(label="Telphone", initial="+234", required=True,
                                  widget=forms.Select(choices=countryCodeList, attrs={
                                      "style": "min-width:50%",
                                  }))
    phoneNumber = forms.CharField(label="", min_length=5, max_length=15, required=True,
                                  widget=forms.TextInput(attrs={
                                      "style": "min-width:100%",
                                      #   "style": "margin-right: 0em",
                                      "placeholder": "Phone",
                                  }))
    email = forms.CharField(label="E-Mail", min_length=7, max_length=30, required=True,
                            widget=forms.EmailInput(attrs={
                                "placeholder": "johndoe@mail.com",
                                "style": "min-width:80%",
                            }))
    bio = forms.CharField(label="Biography", max_length=500, min_length=7,
                          widget=forms.Textarea(attrs={
                              "placeholder": "Write a bit about yourself...",
                              "rows": 5,
                              "cols": 60,
                              "class": "bg-black text-center text-white self-center border-0 rounded-2xl focus:border-0",
                          }))
    avatar = forms.ImageField(label="Avatar",
                              widget=forms.FileInput(attrs={
                                  "class": "custom-file-input",
                              }))
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={
                                   "placeholder": "johndoe001...",
                                   "style": "min-width:60%",
                               }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'course', 'email', 'countryCode', 'phoneNumber', 'username',
                  'avatar', 'bio']


class CoursePaymentForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = []  # Specify the fields you want to include in the form

    userId = forms.CharField(max_length=1000, required=True)
    username = forms.CharField(label="Username", required=True)
    firstName = forms.CharField(label="First Name", min_length=3, required=True)
    lastName = forms.CharField(label="Last Name", min_length=3, required=True)
    email = forms.EmailField(label="Email", required=True)
    phoneNumber = forms.CharField(label="Phone Number", min_length=6, max_length=14, required=True)
    description = forms.CharField(label="Description", required=True)
    amount = forms.DecimalField(label="Price", required=True, max_digits=10, decimal_places=2)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None, label="Course", required=True)
