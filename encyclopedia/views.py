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
            "message": "The requested page was not found.",
            "title": title
        })
    
# work on the search view