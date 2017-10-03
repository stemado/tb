
from django import forms
from django.contrib.auth.models import User
# from tb.activities.models import EmailNotification
from django.utils.safestring import mark_safe
from tb.authentication.models import Clinic
from django.core.validators import MinValueValidator, MaxValueValidator

class ProfileForm(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.
    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['disabled'] = True
        self.fields['last_name'].widget.attrs['disabled'] = True
        self.fields['email'].widget.attrs['disabled'] = True
        self.fields['city'].widget.attrs['disabled'] = True
        self.fields['providence'].widget.attrs['disabled'] = True
        self.fields['zipcode'].widget.attrs['disabled'] = True
        self.fields['address1'].widget.attrs['disabled'] = True
        self.fields['address2'].widget.attrs['disabled'] = True
        self.fields['phonenumber'].widget.attrs['disabled'] = True
        self.fields['mobilenumber'].widget.attrs['disabled'] = True
        self.fields['pharmacy'].widget.attrs['disabled'] = True
        self.fields['user_type'].widget.attrs['disabled'] = True
        self.fields['pinnumber'].widget.attrs['disabled'] = True
        self.fields['smsnotify'].widget.attrs['disabled'] = True
        self.fields['emailnotify'].widget.attrs['disabled'] = True
        self.fields['user_type'].is_hidden = True

    USER_CHOICES=(('0', 'Administrator'),('1', 'Patient'))

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False,
        label="First Name")
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False,
        label="Surname")
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False,
        label="Email")
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="City")
    providence = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Province")
    zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="ZIP Code")
    address1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Address 1")
    address2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Address 2")
    phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Phone Number")
    mobilenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Mobile Number")
    pharmacy = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=50,
        required=False,
        label="Pharmacy")
    user_type = forms.ChoiceField(
        widget = forms.Select(attrs={'class': 'form-control user-type'}), 
        choices = ([('0', 'Administrator'), ('1', 'Patient'),]), 
        initial='1',
        label="User Type")
    pinnumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        required=False,
        label="PIN Number")
    smsnotify = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}), 
        choices = ([(0,'No'), (1,'Yes'), ]),
        initial=True,
        label="SMS Notification?")
    emailnotify = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}), 
        choices = ([(0,'No'), (1,'Yes'), ]), 
        initial=True,
        label="Email Notification?")



    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'city', 'zipcode', 'address1', 'address2', 'providence', 'phonenumber', 'mobilenumber', 'pharmacy', 'user_type', 'pinnumber', 'smsnotify', 'emailnotify')


class EditProfileForm(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.

    USER_CHOICES=(('0', 'Administrator'),('1', 'Patient'))

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # self.fields['user_type'].widget.attrs['disabled'] = True
        # self.fields['user_type'].is_hidden = True
        # self.fields['pinnumber'].widget.attrs['disabled'] = True

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False,
        label="First Name")
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False,
        label="Surname")
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False,
        label="Email")
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="City")
    providence = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Province")
    zipcode = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="ZIP Code")
    address1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Address 1")
    address2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Address 2")
    phonenumber = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Phone Number")
    mobilenumber = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Mobile Number")
    pharmacy = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=50,
        required=False,
        label="Pharmacy")
    user_type = forms.ChoiceField(
        widget = forms.Select(attrs={'class': 'form-control user-type'}), 
        choices = ([('0', 'Administrator'), ('1', 'Patient'),]), 
        initial='1',
        label="User Type")
    pinnumber = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        required=False,
        label="PIN Number")
    smsnotify = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}), 
        choices = ([(0,'No'), (1,'Yes'), ]),
        initial=True,
        label="SMS Notification?")
    emailnotify = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}), 
        choices = ([(0,'No'), (1,'Yes'), ]), 
        initial=True,
        label="Email Notification?")




    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'city', 'zipcode', 'address1', 'address2', 'providence', 'phonenumber', 'mobilenumber', 'pharmacy', 'user_type', 'pinnumber', 'smsnotify', 'emailnotify')



class SignUpStep1(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.

    USER_CHOICES=(('0', 'Administrator'),('1', 'Patient'))

    def __init__(self, *args, **kwargs):
        super(SignUpStep1, self).__init__(*args, **kwargs)
        self.fields['user_type'].is_hidden = True

    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="City")

    providence = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Province")
    zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="ZIP Code")
    address1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Address 1")
    address2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Address 2")
    phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label="Phone Number")
    mobilenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True,
        label="Mobile Number")
    user_type = forms.ChoiceField(widget = forms.Select(attrs={'class': 'form-control user-type'}), 
        choices = ([('0', 'Administrator'), ('1', 'Patient'),]), 
        initial='1',
        label="User Type")
    pinnumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        label="PIN Number",
        required=False)



    class Meta:
        model = User
        fields = ('city', 'zipcode', 'address1', 'address2', 'providence', 'phonenumber', 'mobilenumber', 'user_type', 'pinnumber')


class SignUpStep2(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.


    tandc = forms.CharField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        required=True,
        label="Terms & Conditions",)

    class Meta:
        model = User
        fields = ('tandc', )

class SignUpStep3(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.

    def __init__(self, *args, **kwargs):
        super(SignUpStep3, self).__init__(*args, **kwargs)
        # self.fields['user'].widget.attrs['disabled'] = True

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Clinic Name")
    province = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Province")
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="City")
    street = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Street")
    suburb = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Suburb")
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput())

    class Meta:
        model = Clinic
        fields = ('name', 'province', 'city', 'street', 'suburb', 'user')

# class SignUpStep3(forms.ModelForm):
#     #Do some form of the below to make the form uneditable.
#     #Then have edit button to change the information and save.


#     pharmacy = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=False)

#     class Meta:
#         model = User
#         fields = ('pharmacy', )


class SignUpStep4(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.


    smsnotify = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}), 
        choices = ([(0,'No'), (1,'Yes'), ]),
        initial=1,
        label="SMS Notification?")
    emailnotify = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}), 
        choices = ([(0,'No'), (1,'Yes'), ]), 
        initial=1,
        label="Email Notification?")



    class Meta:
        model = User
        fields = ('smsnotify', 'emailnotify',)




class IndividualUserForm(forms.ModelForm):

    individualTest = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)



    class Meta:
        model = User
        fields = ['individualTest' ]


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class([
                'Old password don\'t match'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data


#CELERY FORM TEST
class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )

# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
#   def render(self):
#     return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

# class EmailNotificationForm(forms.ModelForm):

#     CHOICES = [(True, 'Yes',), (False, 'No',)]

#     emailNewResident = forms.CharField(
#     widget=forms.RadioSelect(choices=CHOICES, renderer=HorizontalRadioRenderer),
#     label="Resident Added: ",
#     required=True)
        
#     emailNewMedication = forms.CharField(
#     widget=forms.RadioSelect(choices=CHOICES, renderer=HorizontalRadioRenderer),
#     label="New Medication: ",
#     required=True)

#     emailPharmacy = forms.CharField(
#     widget=forms.RadioSelect(choices=CHOICES, renderer=HorizontalRadioRenderer),
#     label="Notify Pharmacy Refill: ",
#     required=True)

#     class Meta:

#         model = EmailNotification
#         fields = ['emailNewResident', 'emailNewMedication', 'emailPharmacy', 'user']

