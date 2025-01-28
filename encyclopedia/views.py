from django.shortcuts import render

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# retrieve the content of the entry
def entry_pages(request, title):
    content = util.get_entry(title)
#    if the entry is not found, return an error message
    if content:
        # converting into html
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
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
        # list comprehension to get the entries that contain the query
        results = [entry for entry in entries if query.lower() in entry.lower()]
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
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": f"{title} already exists",
                "title": title
            })
        else:
            util.save_entry(title, content)
            return entry_pages(request, title)
    return render(request, "encyclopedia/new.html")

# work on the edit view
def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return entry_pages(request, title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    

# work on random pages and styling tomorrow
