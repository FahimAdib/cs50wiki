from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import markdown2
from django.contrib import messages
import random

from . import util


def index(request):

    if request.method == "POST":
        form = query(request.POST)

        if form.is_valid():
            if util.get_entry(form.cleaned_data['entry']):
                data = form.cleaned_data['entry']
               # return HttpResponse("working so far")
                return HttpResponseRedirect(f"wiki/{data}/")
            else:
                #   return HttpResponse("working so far")
                data = form.cleaned_data['entry']
                return HttpResponseRedirect(f"search/{data}/")

    return render(request, "encyclopedia/index.html", {

        "entries": util.list_entries(),
        "form": query()
    })


def title(request, title):

    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(title)),
        "title": title,
        "form": query()
    })


def rand(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{title}/")


class query(forms.Form):
    entry = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))


def search(request, title):

    return render(request, "encyclopedia/search.html", {
        "entries": util.list_entries(),
        "title": title,
        "form": query()
    })


def new(request):
    if request.method == "POST":
        form = newEntry(request.POST)

        if form.is_valid():
            if util.get_entry(form.cleaned_data['title']):
                messages.error(request, 'Error: Entry already exists!')
                return HttpResponseRedirect(reverse("new"))
            else:
                title = form.cleaned_data['title']
                desc = form.cleaned_data['descr']
                util.save_entry(title, desc)
                return HttpResponseRedirect(f"/wiki/{title}/")

    return render(request, "encyclopedia/new.html", {
        "form": query(),
        "newEntry": newEntry()
    })


class newEntry(forms.Form):

    title = forms.CharField(label="Entry title",
                            widget=forms.TextInput(attrs={'size': '40'}))

    descr = forms.CharField(label="Description", widget=forms.Textarea())


class editEntry(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(editEntry, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(label="Entry title", widget=forms.TextInput(
            attrs={'size': '40'}), initial=request.session.get("sT"))
        self.fields['descr'] = forms.CharField(label="Description",
                                               widget=forms.Textarea(), initial=util.get_entry(request.session.get("sT")).replace('\r', ''))


def edit(request, title):
    request.session["sT"] = title
    if request.method == "POST":
        form = newEntry(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['descr']
          #  return(HttpResponse(f"{title}"))
            util.save_entry(title, desc)
            return HttpResponseRedirect(f"/wiki/{title}/")

    return render(request, "encyclopedia/edit.html", {
        "entries": util.list_entries(),
        "title": title,
        "form": query(),
        "editEntry": editEntry(request)
    })
