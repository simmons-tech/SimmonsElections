from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('',
    url(r'^$', 'polls.views.index', name='poll_list'),
    url(r'^results/$',
        ListView.as_view(
            queryset=Poll.objects.all(),
            context_object_name='latest_poll_list',
            template_name='polls/results.html'),
        name='poll_results'),
    url(r'^(?P<poll_id>\d+)/$', 'polls.views.vote',
        name='poll_vote'),
)