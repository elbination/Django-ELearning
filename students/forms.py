from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    # Use HiddenInput widget to not to show this field the user.
    # This form is used in the CourseDetailView
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
