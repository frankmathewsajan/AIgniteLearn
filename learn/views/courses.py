from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def courses(request, lesson):
    return render(request, f"learn/courses/{lesson}.html", )

