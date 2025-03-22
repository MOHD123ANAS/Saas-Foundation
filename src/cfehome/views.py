from django.http import HttpResponse
import pathlib
from django.shortcuts import render

from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    return about_view(request,*args, **kwargs)


def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count() * 100) / qs.count()

    except:
        percent = 0
    my_title = "My Page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "total_page_visit_count": qs.count(),
        "percent": percent
    }
    path = request.path
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)

def my_old_home_page_visit(request,*args,**kwargs):
    my_title = "My Page"
    my_context = {
        "page_title" : my_title
    }
    html_ = """
    <!DOCTYPE html>
<html lang="en">
<body>
<h1>This is {page_title} Anything ? </h1>

</body>
</html>
    """. format(**my_context)
    # print(this_dir)
    # html_ = ''
    # html_file_path = this_dir/ "home.html"
    # html_ = html_file_path.read_text()
    return HttpResponse(html_)

