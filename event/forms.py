from django import forms

from .models import Event

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl border"


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "category",
            "name",
            "description",
            "price",
            "image",
        )
        widgets = {
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES}),
            "price": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "image": forms.FileInput(attrs={"class": INPUT_CLASSES}),
        }


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("category", "name", "description", "price", "image", "is_sold") # Add 'category' here
        widgets = {
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),  # Add widget for 'category'
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES}),
            "price": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "image": forms.FileInput(attrs={"class": INPUT_CLASSES}),
        }
