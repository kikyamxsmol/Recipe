
from .models import Recipe, Ingredient, Instruction, UserProfile, Category
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-input'
        }),
        required=True
    )
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'prep_time', 'cook_time', 
                  'servings', 'difficulty', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Recipe Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Describe your recipe...'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Preparation time in minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Cooking time in minutes'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Number of servings'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-input'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ingredient name'
            }),
            'quantity': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 2 cups, 1 tbsp'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Order'
            }),
        }

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['step_number', 'description']
        widgets = {
            'step_number': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Step number'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Describe this step...'
            }),
        }

# Formsets for ingredients and instructions
IngredientFormSet = inlineformset_factory(
    Recipe, 
    Ingredient,
    form=IngredientForm,
    extra=5,
    can_delete=True
)

InstructionFormSet = inlineformset_factory(
    Recipe,
    Instruction,
    form=InstructionForm,
    extra=5,
    can_delete=True
)


# Authentication and profile forms
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)


class UserProfileForm(forms.ModelForm):
    # Allow updating basic user fields alongside profile
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar')

    def __init__(self, *args, user=None, **kwargs):
        """Accept an optional `user` kwarg so the form can populate and save User fields.

        Usage: UserProfileForm(instance=profile, user=request.user)
        """
        self.user = user
        # merge provided initial with user values if present
        initial = kwargs.get('initial', {}) or {}
        if user:
            user_initial = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            # user-provided initial should override defaults
            merged = {**user_initial, **initial}
            kwargs['initial'] = merged
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save profile and also update related User fields if a user was provided
        profile = super().save(commit=False)
        if self.user and self.is_valid():
            self.user.first_name = self.cleaned_data.get('first_name') or self.user.first_name
            self.user.last_name = self.cleaned_data.get('last_name') or self.user.last_name
            self.user.email = self.cleaned_data.get('email') or self.user.email
            if commit:
                self.user.save()

        if commit:
            profile.save()
            # handle many-to-many if any in future
            try:
                self.save_m2m()
            except Exception:
                pass
        return profile
