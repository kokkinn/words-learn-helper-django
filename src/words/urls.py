from django.urls import path
from .views import tests_views, words_views, groups_views

app_name = 'words'

urlpatterns = [
    path('list/', words_views.WordsListView.as_view(), name="list"),
    path('', words_views.home_view, name="home"),
    path("create/", words_views.WordCreateView.as_view(), name="create"),
    path("update/<uuid>/", words_views.WordUpdateView.as_view(), name="update"),
    path("delete/<uuid>/", words_views.delete_view, name="delete"),
    path("utils/get_ig", words_views.get_initial_groups_of_word, name='get_groups'),
    path("groups/", groups_views.GroupsListView.as_view(), name="groups_list"),
    path("groups/<uuid:uuid>", groups_views.WordsInGroupListView.as_view(), name='group'),
    path("groups/create", groups_views.GroupCreateView.as_view(), name="group_create"),
    path("groups/update/<uuid:uuid>", groups_views.GroupUpdateView.as_view(), name="group_update"),
    path("groups/delete/<uuid:uuid>", groups_views.GroupDeleteView.as_view(), name="group-delete"),
    path("tests", tests_views.TestsHomeView.as_view(), name="tests_home"),
    # path("tests/quick_test", views.QuickTest.as_view(), name="quick_test"),
    path("tests/<uuid:uuid>", tests_views.TestQuestionView.as_view(), name="test-question"),
    path("tests/group_of_words_test/results", tests_views.ResultsListView.as_view(), name="test_results"),
    path("tests/group_of_words_test/results/<uuid:uuid>", tests_views.TestsResultView.as_view(), name="single_result")
]


