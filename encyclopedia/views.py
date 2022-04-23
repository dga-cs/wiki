import random
from attr import attr, field
import django
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
import markdown2
from . import util


class EditEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=20, widget=forms.TextInput(
        attrs={'class':'form-control', 'readonly': True}
    ))
    # title.widget.attrs['readonly'] = True
    content = forms.CharField(label="Entry Markdown content",
    widget=forms.Textarea(
        attrs={
            'class':"form-control",
            'rows':"5",
        }))


class NewEntryForm(EditEntryForm):
    title = forms.CharField(label="Title", max_length=20, widget=forms.TextInput(
        attrs={'class':'form-control', 'readonly': False}
    ))
    def clean_title(self):
        title = self.cleaned_data['title']
        for item in util.list_entries():
                if title.lower() == item.lower():
                    raise ValidationError("Entry with this title is already exist")
        return title


def index(request):
    if request.method == "POST":
        search_value = request.POST["q"]
        for item in util.list_entries():
            if search_value.strip().lower() == item.lower():
                return HttpResponseRedirect("wiki/"+item)
        return render(request, "encyclopedia/index.html", {
        "entries": [item for item in util.list_entries() 
            if item.lower().find(search_value.strip().lower()) != -1]
    })
    else: 
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })

def entry_page(request, entry_title):
    return render(request, "encyclopedia/entry_page.html",{
        "entry_title": entry_title,
        "entry_content": markdown2.markdown(util.get_entry(entry_title)),
    })

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            new_entry_title = form.cleaned_data["title"]
            util.save_entry(new_entry_title, form.cleaned_data["content"])
            return HttpResponseRedirect("wiki/"+new_entry_title)
    else:
        form = NewEntryForm()
    return render(request, "encyclopedia/add_entry.html", {
                "form": form 
            })


def random_entry(request):
    random_item_number = random.randint(0, len(util.list_entries())-1)
    return HttpResponseRedirect("wiki/"+util.list_entries()[random_item_number])


def edit_entry(request, entry_title):
    dict_for_form = {
        "title": entry_title,
        "content": util.get_entry(entry_title), 
    }
    form = EditEntryForm(dict_for_form)
    return render(request, "encyclopedia/edit_entry.html",{
        "entry_name": entry_title,
        "form": form,
    })

def save_ed_entry(request):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
            return HttpResponseRedirect("wiki/"+form.cleaned_data["title"])
    else:
        return HttpResponseRedirect("/")