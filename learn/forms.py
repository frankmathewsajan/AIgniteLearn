# forms.py
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    interests = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Enter interests separated by commas."
    )
    goals = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Enter goals separated by commas."
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'email', 'age', 'learning_style', 'education_level', 'interests', 'goals', 'avatar',
                  'bio']

    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        return [interest.strip() for interest in interests.split(',') if interest.strip()]

    def clean_goals(self):
        goals = self.cleaned_data.get('goals')
        return [goal.strip() for goal in goals.split(',') if goal.strip()]
