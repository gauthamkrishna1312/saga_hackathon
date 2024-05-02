from django import forms
from .models import Hospital
from users.models import Doctor

class HospitalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["beds"].widget.attrs["placeholder"] = "Beds"
        self.fields["rooms"].widget.attrs["placeholder"] = "Rooms"
        self.fields["description"].widget.attrs["placeholder"] = "Description"

    class Meta:
        model = Hospital
        fields = ['beds', 'rooms', 'description']

class DoctorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["qualification"].widget.attrs["placeholder"] = "Qualification"
        self.fields["experties"].widget.attrs["placeholder"] = "Experties"
        self.fields["experience"].widget.attrs["placeholder"] = "Experience"
        self.fields["bio"].widget.attrs["placeholder"] = "Bio"

    class Meta:
        model = Doctor
        fields = ['qualification', 'experties', 'experience', 'bio']


class adddateForm(forms.Form):
    time = forms.DateTimeField(widget=forms.DateTimeInput())