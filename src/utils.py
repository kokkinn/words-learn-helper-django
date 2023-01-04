import json
from django.urls import reverse_lazy, reverse

from django.http import JsonResponse


def get_searches(request):
    res = {'refs_objects': [
        {'name': 'Add word', 'url': reverse('words:create')},
        {'name': 'Add set', 'url': reverse('words:group_create')},
        {'name': 'My vocabulary', 'url': reverse('words:list')},
        {'name': 'My sets', 'url': reverse('words:groups_list')},
        {'name': 'Tests', 'url': reverse('words:tests_home')},
        {'name': 'Test results', 'url': reverse('words:test_results')},
        {'name': 'Contacts', 'url': reverse('contacts')},
        {'name': 'Change password', 'url': reverse('password_change')},
        {'name': 'Profile', 'url': reverse('accounts:profile')},
        {'name': 'Password reset', 'url': reverse('password_reset')},
        {'name': 'Source code', 'url': 'https://github.com/kokkinn/Words-Learn-Helper-Django-Docker'},
        {'name': 'Home', 'url': reverse('index')},

    ]}
    return JsonResponse({'res': json.dumps(res)}, status=200)
