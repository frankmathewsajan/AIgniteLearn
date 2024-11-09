from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def courses(request, lesson):
    return render(request, f"learn/courses/{lesson}.html", {
        "level": lesson,
        'lis': lessons[lesson]
    })


lessons = {
    'beginner': [
        {
            'title': 'Introduction to Oceans & Atmosphere',
            'id': 'oceans-atmosphere'
        },
        {
            'title': 'Phytoplankton - The Tiny Heroes of the Ocean',
            'id': 'phytoplankton'
        },
        {
            'title': 'PACE Mission Overview',
            'id': 'pace-mission'
        },
        {
            'title': 'PACE Data & Discoveries',
            'id': 'pace-data'

        }
    ]
}
