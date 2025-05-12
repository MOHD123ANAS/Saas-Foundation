from django.conf.global_settings import LOGIN_URL
from django.http import HttpResponse
import pathlib
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings


from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

LOGIN_URL = settings.LOGIN_URL

def home_view(request, *args, **kwargs):

    print(request.user.is_authenticated,request.user)
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

VALID_CODE = "abc123"

def pw_protected_view(request,*args,**kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    if request.method == "POST":
        user_pw_sent = request.POST.get("code") or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
    if is_allowed:
        return render(request,"protected/view.html",{})
    return render(request, "protected/entry.html", {})

@login_required
def user_only_view(request,*args,**kwargs):
    # print(request.user.is_staff)
    return render(request,"protected/user-only.html",{})

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request,*args,**kwargs):
    return render(request,"protected/user-only.html",{})
