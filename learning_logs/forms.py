from django import forms
from .models import Topic
from .models import Entry
class TopicForm(forms.ModelForm):
    """Form for adding a new topic."""
    class Meta:
        model = Topic
        fields = ['text']  # only the 'text' field (topic name)
class EntryForm(forms.ModelForm):
    """Form for adding a new entry to a topic."""
    class Meta:
        model = Entry
        fields = ['text']  # only the 'text' field (entry content)

