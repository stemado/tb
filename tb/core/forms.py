
from django import forms
from django.contrib.auth.models import User
# from tb.activities.models import EmailNotification
from django.utils.safestring import mark_safe


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
        self.fields['user_type'].widget.attrs['disabled'] = True
        self.fields['pinnumber'].widget.attrs['disabled'] = True


    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False)
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)

    providence = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    address1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    address2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    mobilenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    user_type = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=50,
        required=False)
    pinnumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        required=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'city', 'zipcode', 'address1', 'address2', 'providence', 'phonenumber', 'mobilenumber', 'user_type', 'pinnumber']


class EditProfileForm(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs['disabled'] = True
        self.fields['pinnumber'].widget.attrs['disabled'] = True

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False)
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)

    providence = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    address1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    address2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    mobilenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    user_type = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=50,
        required=False)
    pinnumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        required=False)



    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'city', 'zipcode', 'address1', 'address2', 'providence', 'phonenumber', 'mobilenumber', 'user_type', 'pinnumber']




class FirstSignUp(forms.ModelForm):
    #Do some form of the below to make the form uneditable.
    #Then have edit button to change the information and save.
    def __init__(self, *args, **kwargs):
        super(FirstSignUp, self).__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs['disabled'] = True

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False)
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)

    providence = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    address1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    address2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    mobilenumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    user_type = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=50,
        required=False)
    pinnumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        required=False)



    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'city', 'zipcode', 'address1', 'address2', 'providence', 'phonenumber', 'mobilenumber', 'user_type', 'pinnumber']

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

