
from django.shortcuts import render, redirect
from .forms import TopicForm
from .forms import EntryForm
from django.shortcuts import get_object_or_404
from .models import Entry

# Create your views here.


def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')
from .models import Topic

def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
from .models import Topic

def topic(request, topic_id):
    """Show a single topic and its entries."""

    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')

    context = {
        'topic': topic,
        'entries': entries
    }

    return render(request, 'learning_logs/topic.html', context)



def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted: create a blank form.
        form = TopicForm()
    else:
        # Data submitted: process the data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()  # save new Topic to database
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)



def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=entry.topic.id)

    return render(request, 'learning_logs/edit_entry.html', {'form': form})


def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic_id = entry.topic.id
    entry.delete()
    return redirect('learning_logs:topic', topic_id=topic_id)
def new_entry(request, topic_id):
    """Add a new entry for a topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Populate form with the current entry (instance).
        form = EntryForm(instance=entry)
    else:
        # Bind form to POST data and the instance.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()  # save updates to the entry
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

