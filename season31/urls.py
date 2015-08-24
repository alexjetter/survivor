from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^castaways/$', views.CastawaysView.as_view(), name='castaways'),
	url(r'^players/$', views.PlayersView.as_view(), name='players'),
	url(r'^episodes/$', views.EpisodesView.as_view(), name='episodes'),
	url(r'^actions/$', views.ActionsView.as_view(), name='actions'),
	url(r'^rules/', TemplateView.as_view(template_name="season31/rules.html"), name='rules'),
	url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerView.as_view(), name='player'),
	url(r'^castaway/(?P<pk>[0-9]+)/$', views.CastawayView.as_view(), name='castaway'),
	url(r'^episode/(?P<pk>[0-9]+)/$', views.EpisodeView.as_view(), name='episode'),
	url(r'^updatescores/$', views.updatescores, name='updatescores'),
	url(r'^addepisode/$', views.addepisode, name='addepisode'),
	url(r'^backfillteams/$', views.backfillteams, name='backfillteams'),
	url(r'^pickteams/(?P<pe_id>[0-9]+)/$', views.pickteams, name='pickteams'),
	url(r'^pickvotes/(?P<pe_id>[0-9]+)/$', views.pickvotes, name='pickvotes'),
	url(r'^updateceactions/(?P<e_id>[0-9]+)/$', views.updateceactions, name='updateceactions'),
	url(r'^updatecevotes/(?P<e_id>[0-9]+)/$', views.updatecevotes, name='updatecevotes'),
	url(r'^updateepisodescore/(?P<e_id>[0-9]+)/$', views.updateepisodescore, name='updateepisodescore'),
	url(r'^updatecetribes/(?P<e_id>[0-9]+)/$', views.updatecetribes, name='updatecetribes'),
	url(r'^addcastaway/$', views.addcastaway, name='addcastaway'),
	url(r'^deletecastaway/$', views.deletecastaway, name='deletecastaway'),
	url(r'^addtribe/$', views.addtribe, name='addtribe'),
	url(r'^deletetribe/$', views.deletetribe, name='deletetribe'),
	url(r'^addaction/$', views.addaction, name='addaction'),
	url(r'^deleteaction/$', views.deleteaction, name='deleteaction'),
	url(r'^deleteepisode/(?P<e_id>[0-9]+)/$', views.deleteepisode, name='deleteepisode'),
	url(r'^togglehelptext/(?P<p_id>[0-9]+)/$', views.togglehelptext, name='togglehelptext'),
	url(r'^updateepisodetitle/(?P<e_id>[0-9]+)/$', views.updateepisodetitle, name='updateepisodetitle'),
	url(r'^updateepisodedatetime/(?P<e_id>[0-9]+)/$', views.updateepisodedatetime, name='updateepisodedatetime'),
	url(r'^updateepisodeteamsize/(?P<e_id>[0-9]+)/$', views.updateepisodeteamsize, name='updateepisodeteamsize'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
]