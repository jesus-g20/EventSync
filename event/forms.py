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
            "location",
            "event_date",
            "event_time",
        )
        widgets = {
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES}),
            "price": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "image": forms.FileInput(attrs={"class": INPUT_CLASSES}),
            "location": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "event_date": forms.DateInput(
                attrs={"type": "date", "class": INPUT_CLASSES}
            ),
            "event_time": forms.TimeInput(
                attrs={"type": "time", "class": INPUT_CLASSES}
            ),
        }


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "category",
            "name",
            "description",
            "price",
            "image",
            "location",  # Added 'location'
            "event_date",  # Added 'event_date'
            "event_time",  # Added 'event_time'
            "is_sold",
        )
        widgets = {
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES}),
            "price": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "image": forms.FileInput(attrs={"class": INPUT_CLASSES}),
            "location": forms.TextInput(attrs={"class": INPUT_CLASSES}),  # Added widget
            "event_date": forms.DateInput(
                attrs={"type": "date", "class": INPUT_CLASSES}
            ),  # Added widget
            "event_time": forms.TimeInput(
                attrs={"type": "time", "class": INPUT_CLASSES}
            ),  # Added widget
        }
