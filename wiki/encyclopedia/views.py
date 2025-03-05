from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib import messages
import random
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        }, status=404)
    else:
        html_entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": html_entry
        })

def search(request):
    query = request.GET.get('q')
    if not query:
        return render(request, "encyclopedia/error.html")
    
    entries = util.list_entries()

    if query in entries:
        return redirect("entry", title=query)
    

    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def createPage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")

        if title in util.list_entries():
            messages.error(request, "Page already exists.")
            return redirect("createPage")
        
        util.save_entry(title, text)

        return redirect("entry", title=title)

    return render(request, "encyclopedia/createPage.html")

def edit(request, title):
    content =  util.get_entry(title)

    if content is None: 
        messages.error(request, "Page doesn't exists")
        return redirect("index")

    if request.method == "POST":
        newContent = request.POST.get("content")

        util.save_entry(title, newContent)

        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def randomPage(request):
    entries = util.list_entries()

    randomEntry = random.choice(entries)
    return redirect("entry", title=randomEntry)