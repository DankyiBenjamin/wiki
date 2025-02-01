from django.shortcuts import render , redirect

from . import util
# mardown for converting to html
import markdown2
# used to generate random pages
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# retrieve the content of the entry
def entry_pages(request, title):
    content = util.get_entry(title)
#    if the entry is not found, return an error message from the error.html
    if content:
        # converting into html
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
        # return an error message from the error.html 
        return render(request, "encyclopedia/error.html", {
            "message": f"{title} not found",
            "title": title
        })
    
# work on the search view
def search(request):
    # get the query from the search form
    query = request.GET.get('q', '').strip()
    # check if the query is an entry
    if query in util.list_entries():
        return entry_pages(request, query)
    else:
        # if the query is not an entry, check if it is a substring of an entry
        entries = util.list_entries()
        # create a list to store the results
        results = []
        # loop through the entries and check if the query is a substring of the entry
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)
        
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })
    
# work on the new view

def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        #  case sensitivity where the title is not case sensitive
        title = title.capitalize()
        # check if the title already exists
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": f"{title} already exists",
                "title": title
            })
        else:
            # save the new entry
            util.save_entry(title, content)
            # redirect to the new entry page
            return redirect("entry_page", title)
    return render(request, "encyclopedia/new.html")

# work on the edit view
def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry_page", title)
        # return entry_pages(request, title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    

#  random page view
def random_page(request):
    # getting all entries
    entries = util.list_entries()
    # choosing a random entry
    title = random.choice(entries)
    # passing it to the entry_pages view
    return entry_pages(request , title)
