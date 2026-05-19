from django import forms
from .models import CustomUser, Recipe


class SignUpForm(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'autocomplete': 'off'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password (min 6 chars)'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    role = forms.ChoiceField(
        choices=[('', 'Select Role'), ('admin', 'Admin'), ('user', 'User')],
        widget=forms.Select()
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cpw = cleaned.get('confirm_password')
        if pw and cpw and pw != cpw:
            self.add_error('confirm_password', "Passwords do not match.")
        if not cleaned.get('role'):
            self.add_error('role', "Please select a role.")
        return cleaned


class SignInForm(forms.Form):
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RecipeForm(forms.ModelForm):
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Step 1: Preheat oven...\nStep 2: Mix ingredients...',
            'rows': 5,
            'class': 'form-ctrl',
        }),
        help_text="One step per line. Each line becomes a numbered instruction."
    )

    class Meta:
        model  = Recipe
        fields = ['name', 'course', 'description', 'image', 'instructions']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter recipe name...', 'class': 'form-ctrl'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter recipe description...', 'rows': 3, 'class': 'form-ctrl'
            }),
            'course': forms.Select(attrs={'class': 'form-ctrl'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
        self.fields['image'].widget.attrs.update({'class': 'form-ctrl', 'id': 'id_image'})
