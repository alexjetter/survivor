from datetime import datetime
from decimal import *
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.utils import timezone
from django.views import generic
from random import randint

from .forms import UserForm
from .models import Player, Castaway, Pick, Episode, PlayerEpisode, CastawayEpisode, Tribe, Vote, Action, League

def index(request):
	template = loader.get_template('season31/index.html')
	return HttpResponseRedirect('/season31/episode/%d' % Episode.objects.all().latest().id)

class CastawaysView(generic.ListView):
	context_object_name = 'castaways'
	template_name = 'season31/castaways.html'
	queryset = Castaway.objects.all()
	def get_context_data(self, **kwargs):
		context = super(CastawaysView, self).get_context_data(**kwargs)
		context['episodes'] = Episode.objects.all()
		return context

class PlayersView(generic.ListView):
	context_object_name = 'players'
	template_name = 'season31/players.html'
	queryset = Player.objects.all()
		
class TribesView(generic.ListView):
	template_name = 'season31/tribes.html'
	context_object_name = 'tribes'
	def get_queryset(self):
		return Tribe.objects.all()

class ActionsView(generic.ListView):
	template_name = 'season31/actions.html'
	context_object_name = 'actions'
	def get_queryset(self):
		return Action.objects.all()

class PlayerView(generic.DetailView):
	model = Player
	template_name = 'season31/player.html'

class CastawayView(generic.DetailView):
	model = Castaway
	template_name = 'season31/castaway.html'

class EpisodeView(generic.DetailView):
	model = Episode
	template_name = 'season31/episode.html'
	def get_context_data(self, **kwargs):
		context = super(EpisodeView, self).get_context_data(**kwargs)
		context['actions'] = Action.objects.all()
		context['tribes'] = Tribe.objects.all()
		return context

class TribeView(generic.DetailView):
	model = Tribe
	template_name = 'season31/tribe.html'
	def get_context_data(self, **kwargs):
		context = super(TribeView, self).get_context_data(**kwargs)
		context['episodes'] = Episode.objects.all()
		return context

def register(request):
	context = RequestContext(request)
	registered = False
	player = None
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			player = Player()
			player.user = user
			player.save()
			for episode in Episode.objects.all():
				playerepisode = PlayerEpisode(player = player, episode = episode)
				playerepisode.save()
				teampicks = episode.castawayepisode_set.order_by('?')[:episode.team_size]
				votepicks = episode.castawayepisode_set.order_by('?')[:2]
				for ce in teampicks:
					pick = Pick(player_episode = playerepisode, castaway_episode = ce, type = "TM")
					pick.save()
				for ce in votepicks:
					pick = Pick(player_episode = playerepisode, castaway_episode = ce, type = "VO")
					pick.save()
			registered = True
			return render_to_response('season31/login.html', {}, context)
		else:
			print user_form.errors
	else:
		user_form = UserForm()
	return render_to_response('season31/register.html', {'user_form': user_form, 'registered': registered}, context)

def user_login(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return render(request, 'season31/player.html', {'player': user.player,})
			else:
				return HttpResponse("Your account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('season31/login.html', {}, context)

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/season31/')

def updatescores(request):
	for player in Player.objects.all():
		player.score = 0
		player.save()
	lastepisode = None
	for episode in Episode.objects.all():
		update_episode_score(episode)
	return HttpResponseRedirect('/season31/')

def update_episode_score(episode):
	try:
		lastepisode = Episode.objects.get(number = episode.number - 1)
	except:
		lastepisode = None
	castawayepisodes = episode.castawayepisode_set.all()
	for castawayepisode in castawayepisodes:
		castawayepisode.update_score()
		castawayepisode.save()
	for playerepisode in episode.playerepisode_set.all():
		player = playerepisode.player
		playerepisode.update_score()
		if lastepisode:
			last_pe = PlayerEpisode.objects.get(player = player, episode = lastepisode)
			player.score = last_pe.total_score
		else:
			player.score = 0
		player.score += playerepisode.week_score
		playerepisode.total_score = player.score
		player.save()
		playerepisode.save()
	lastplace = 0
	lastscore = 0
	for counter, playerepisode in enumerate(episode.playerepisode_set.order_by('-total_score').all()):
		player = playerepisode.player
		playerepisode.place = counter + 1
		if playerepisode.total_score == lastscore:
			playerepisode.place = lastplace
		player.place = playerepisode.place
		if lastepisode:
			last_pe = PlayerEpisode.objects.get(player = player, episode = lastepisode)
			playerepisode.movement = last_pe.place - playerepisode.place
		player.movement = playerepisode.movement
		playerepisode.save()
		player.save()
		lastplace = playerepisode.place
		lastscore = playerepisode.total_score

def addepisode(request): # TODO: Add random toggle
	le = Episode.objects.all().latest()
	try:
		teamsize = request.POST['teamsize']
	except:
		return HttpResponseRedirect('/season31/')
	ne = Episode(title = "New Episode", number = le.number + 1, air_date = timezone.now(), team_size = teamsize)
	ne.save()
	for c in Castaway.objects.all():
		if not c.voted_out():
			nce = CastawayEpisode(castaway = c, episode = ne, tribe = c.get_tribe())
			nce.save()
	for p in Player.objects.all():
		npe = PlayerEpisode(player = p, episode = ne)
		npe.save()
		if "random" in request.POST:
			teampicks = ne.castawayepisode_set.order_by('?')[:ne.team_size]
			votepicks = ne.castawayepisode_set.order_by('?')[:2]
			for ce in teampicks:
				pick = Pick(player_episode = npe, castaway_episode = ce, type = "TM")
				pick.save()
			for ce in votepicks:
				pick = Pick(player_episode = npe, castaway_episode = ce, type = "VO")
				pick.save()
	return HttpResponseRedirect('/season31/episode/%d' % (ne.id))

def updateceactions(request, e_id):
	action = Action.objects.get(id = int(request.POST['action']))
	ce_ids = request.POST.getlist('castaways')
	for id in ce_ids:
		ce = CastawayEpisode.objects.get(id = id)
		if "delete" in request.POST:
			try:
				badaction = ce.actions.get(name = action.name)
			except:
				badaction = None
			if badaction != None:
				ce.actions.remove(badaction)
		else:
			ce.actions.add(action)
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def updatecevotes(request, e_id):
	votee = Castaway.objects.get(id = int(request.POST['votee']))
	voter_ids = request.POST.getlist('voters')
	for id in voter_ids:
		ce = CastawayEpisode.objects.get(id = id)
		try:
			vote = ce.vote_set.first()
		except:
			vote = None
		if vote != None:
			vote.castaway = votee
		else:
			vote = Vote(castaway_episode = ce, castaway = votee)
		vote.save()
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def updateepisodescore(request, e_id):
	e = Episode.objects.get(id = e_id)
	if e:
		update_episode_score(e)
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))
	
def updatecetribes(request, e_id):
	tribe = Tribe.objects.get(id = int(request.POST['tribe']))
	ce_ids = request.POST.getlist('castaways')
	for id in ce_ids:
		ce = CastawayEpisode.objects.get(id = id)
		ce.tribe = tribe
		ce.save()
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def updateepisodetitle(request, e_id):
	e = Episode.objects.get(id = e_id)
	try:
		title = request.POST['title']
	except:
		title = None
	if title:
		e.title = title
		e.save()
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def updateepisodedatetime(request, e_id):
	e = Episode.objects.get(id = e_id)
	airdatetime_str = request.POST['airdatetime']
	print airdatetime_str
	try:
		airdatetime = datetime.strptime(airdatetime_str, "%Y%m%d %H")
	except:
		airdatetime = None
	print airdatetime
	if airdatetime:
		e.air_date = airdatetime
		e.save()
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def updateepisodeteamsize(request, e_id):
	e = Episode.objects.get(id = e_id)
	try:
		teamsize = request.POST['teamsize']
	except:
		teamsize = None
	if teamsize:
		e.team_size = teamsize
		e.save()
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def deleteepisode(request, e_id):
	e = Episode.objects.get(id = e_id)
	if e:
		e.delete()
	return HttpResponseRedirect('/season31/')

def showleaguetoggle(request, p_id):
	p = Player.objects.get(id = p_id)
	p.show_league_only = not p.show_league_only
	p.save()
	return HttpResponseRedirect('/season31/player/%i' % int(p_id))
	
def addcastaway(request):
	name = request.POST['name']
	fullname = request.POST['fullname']
	occupation = request.POST['occupation']
	age = request.POST['age']
	c = Castaway(name = name, full_name = fullname, age = age, occupation = occupation)
	c.save()
	for e in Episode.objects.all():
		ce = CastawayEpisode(castaway = c, episode = e, tribe = Tribe.objects.first())
		ce.save()
	return HttpResponseRedirect('/season31/castaways/')

def deletecastaway(request):
	try:
		c = Castaway.objects.get(id = request.POST['id'])
	except:
		c = None
	if c:
		c.delete()
	return HttpResponseRedirect('/season31/castaways/')

def addtribe(request):
	name = request.POST['name']
	color = request.POST['color']
	t = Tribe(name = name, color = color)
	t.save()
	return HttpResponseRedirect('/season31/tribes/')

def deletetribe(request):
	try:
		t = Tribe.objects.get(id = request.POST['id'])
	except:
		t = None
	if t:
		t.delete()
	return HttpResponseRedirect('/season31/tribes/')

def addaction(request):
	name = request.POST['name']
	score = request.POST['score']
	icon_filename = request.POST['icon_filename']
	a = Action(name = name, score = score, icon_filename = icon_filename)
	a.save()
	return HttpResponseRedirect('/season31/actions/')

def deleteaction(request):
	try:
		a = Action.objects.get(id = request.POST['id'])
	except:
		a = None
	if t:
		a.delete()
	return HttpResponseRedirect('/season31/actions/')

# TODO: merge with below.  much is the same.
def pickteams(request, pe_id):
	pe = get_object_or_404(PlayerEpisode, pk=pe_id)
	picks = request.POST.getlist('picks')
	if len(picks) != pe.episode.team_size:
		return render(request, 'season31/player.html', {'player': pe.player, 'team_error_message': "You must select %i castaways" % int(pe.episode.team_size),})
	else:
		pe.clear_team_picks()
		for castawayname in picks:
			c = Castaway.objects.get(name = castawayname)
			ce = CastawayEpisode.objects.get(castaway = c, episode = pe.episode)
			pick = Pick(player_episode = pe, castaway_episode = ce, type = "TM")
			pick.save()
		return render(request, 'season31/player.html', {'player': pe.player,})

def pickvotes(request, pe_id):
	pe = get_object_or_404(PlayerEpisode, pk=pe_id)
	picks = request.POST.getlist('picks')
	if len(picks) != 2:
		return render(request, 'season31/player.html', {'player': pe.player, 'vote_error_message': "You must select 2 castaways",})
	else:
		pe.clear_vote_picks()
		for castawayname in picks:
			print castawayname
			c = Castaway.objects.get(name = castawayname)
			ce = CastawayEpisode.objects.get(castaway = c, episode = pe.episode)
			p = Pick(player_episode = pe, castaway_episode = ce, type = "VO")
			p.save()
		return render(request, 'season31/player.html', {'player': pe.player,})