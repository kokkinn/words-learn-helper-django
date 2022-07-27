from django.urls import path
from . import views
from .views import tests_views, words_views, groups_views

app_name = 'words'

urlpatterns = [
    path('list/', words_views.WordsListView.as_view(), name="list"),
    # path('add/', words_views.add_view),
    # path('test/', views.test_view),
    path('', words_views.home_view, name="home"),
    path('<uuid:uuid>/', words_views.one_word_view, name="single"),
    path("create/", words_views.WordCreateView.as_view(), name="create"),
    path("update/<uuid:uuid>/", words_views.WordUpdateView.as_view(), name="update"),
    path("delete/<uuid:uuid>/", words_views.delete_view, name="delete"),
    path("groups/", groups_views.GroupsListView.as_view(), name="groups_list"),
    path("groups/<uuid:uuid>", groups_views.WordsInGroupListView.as_view(), name='group'),
    path("groups/create", groups_views.GroupCreateView.as_view(), name="group_create"),
    path("groups/update/<uuid:uuid>", groups_views.GroupUpdateView.as_view(), name="group_update"),
    path("tests", tests_views.TestsHomeView.as_view(), name="tests_home"),
    # path("tests/quick_test", views.QuickTest.as_view(), name="quick_test"),
    path("tests/groups_of_words_test/<uuid:uuid>", tests_views.GroupOfWordsTest.as_view(), name="groups_of_words_test"),
    path("tests/group_of_words_test/results", tests_views.TestsResultsListView.as_view(), name="test_results"),
    path("tests/group_of_words_test/results/<uuid:uuid>", tests_views.TestsResultView.as_view(), name="single_result")
]
