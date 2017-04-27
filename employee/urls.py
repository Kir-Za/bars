from django.conf.urls import url
from .views import (index, CreateCandidateView, CandidateQuestionView, DjejSelectView, DjedCandView, AddPadavanView,
                    CommonDjedView, OnePadavanView)

urlpatterns = [
    url(r'^$', index, name="base_page"),
    url(r'^create_cand/$', CreateCandidateView.as_view(), name="create_candidate"),
    url(r'^ask_cand/(?P<pk>.*)/$', CandidateQuestionView.as_view(), name="ask_candidate"),
    url(r'^dj_select/$', DjejSelectView.as_view(), name="select_djed"),
    url(r'^dj_cand/(?P<pk>.*)$', DjedCandView.as_view(), name="list_cand"),
    url(r'^add_padavan/$', AddPadavanView.as_view()),
    url(r'^common/$', CommonDjedView.as_view(), name="data_list"),
    url(r'^one_padavan/$', OnePadavanView.as_view(), name="data_one"),

]

