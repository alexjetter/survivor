from datetime import datetime
from decimal import *
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from pytz import timezone
from django.views import generic
from random import randint

from .forms import UserForm
from django.contrib.auth.models import User
from .models import Player, Castaway, TeamPick, VotePick, Episode, PlayerEpisode, CastawayEpisode, Tribe, Vote, Action

class LeaderboardView(generic.ListView):
	context_object_name = 'playerepisodes'
	template_name = 'season31/leaderboard.html'
	try:
		latestepisode = Episode.objects.filter(is_locked = True).latest()
	except:
		latestepisode = Episode.objects.latest()
	queryset = PlayerEpisode.objects.filter(player__hidden = False, episode= latestepisode).order_by('-total_score')
	def get_context_data(self, **kwargs):
		context = super(LeaderboardView, self).get_context_data(**kwargs)
		context['latestepisode'] = self.latestepisode
		return context

class CastawaysView(generic.ListView):
	context_object_name = 'castaways'
	template_name = 'season31/castaways.html'
	queryset = Castaway.objects.all()
	def get_context_data(self, **kwargs):
		context = super(CastawaysView, self).get_context_data(**kwargs)
		context['episodes'] = Episode.objects.all()
		context['tribes'] = Tribe.objects.all()
		return context

class PlayersView(generic.ListView):
	context_object_name = 'players'
	template_name = 'season31/players.html'
	queryset = Player.objects.filter(hidden = False)

class EpisodesView(generic.ListView):
	context_object_name = 'episodes'
	template_name = 'season31/episodes.html'
	queryset = Episode.objects.all()

class ActionsView(generic.ListView):
	template_name = 'season31/actions.html'
	context_object_name = 'actions'
	def get_queryset(self):
		return Action.objects.all()

class PlayerView(generic.DetailView):
	model = Player
	template_name = 'season31/player.html'
	def get_context_data(self, **kwargs):
		context = super(PlayerView, self).get_context_data(**kwargs)
		context['pastplayerepisodes'] = PlayerEpisode.objects.filter(player = context['player'], episode__is_locked = True)
		context['futureplayerepisodes'] = PlayerEpisode.objects.filter(player = context['player'], episode__is_locked = False)
		return context

class CastawayView(generic.DetailView):
	model = Castaway
	template_name = 'season31/castaway.html'

class EpisodeView(generic.DetailView):
	model = Episode
	template_name = 'season31/episode.html'
	def get_context_data(self, **kwargs):
		context = super(EpisodeView, self).get_context_data(**kwargs)
		context['episodes'] = Episode.objects.all()
		context['actions'] = Action.objects.all()
		context['tribes'] = Tribe.objects.all()
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
			player.username = user.username.lower()
			player.save()
			for episode in Episode.objects.all():
				playerepisode = PlayerEpisode(player = player, episode = episode)
				playerepisode.save()
			firstepisode = Episode.objects.order_by('air_date').first()
			if firstepisode.check_lock():
				pickrandomifempty(firstepisode)
			for episode in Episode.objects.filter(number__gt = 1):
				rolloverteam(episode)
			registered = True 
			user = authenticate(username = request.POST['username'], password = request.POST['password'])
			login(request, user)
			return HttpResponseRedirect('/season31/player/%d' % (user.player.id))
		else:
			print user_form.errors
	else:
		user_form = UserForm()
	return render_to_response('season31/register.html', {'user_form': user_form, 'registered': registered}, context)

def backfillteams(request):
	pickrandomifempty(Episode.objects.order_by('air_date').first())
	for episode in Episode.objects.filter(is_locked = True):
		rolloverteam(episode)
	return HttpResponseRedirect('/season31/episode/%d' % (Episode.objects.latest().id))
	
def pickrandomifempty(episode):
	for player in Player.objects.all():
		if not TeamPick.objects.filter(episode = episode, player = player):
			teampicks = episode.castawayepisode_set.order_by('?')[:episode.team_size]
			for ce in teampicks:
				pick = TeamPick(episode = episode, player = player, castaway = ce.castaway)
				pick.save()
		if not VotePick.objects.filter(episode = episode, player = player):
			votepicks = episode.castawayepisode_set.order_by('?')[:2]
			for ce in votepicks:
				pick = VotePick(episode = episode, player = player, castaway = ce.castaway)
				pick.save()
	calculatejspsforepisode(episode)

def rolloverteam(episode):
	lastepisode = episode.get_prev_episode()
	for player in Player.objects.all():
		# Bring over still valid picks
		#print "-----------------------"
		#print "%s rollover" % (player)
		if lastepisode:
			if not TeamPick.objects.filter(episode = episode, player = player):
				lastepisodeteampicks = TeamPick.objects.filter(player = player, episode = lastepisode)
				for pick in lastepisodeteampicks:
					if pick.castaway.out_episode_number == 0:
						newpick = TeamPick(episode = episode, player = player, castaway = pick.castaway)
						newpick.save()
			if not VotePick.objects.filter(episode = episode, player = player):
				lastepisodevotepicks = VotePick.objects.filter(player = player, episode = lastepisode)
				for pick in lastepisodevotepicks:
					if pick.castaway.out_episode_number == 0:
						newpick = VotePick(episode = episode, player = player, castaway = pick.castaway)
						newpick.save()
		# Drop random if necessary
		teampicks = TeamPick.objects.filter(episode = episode, player = player).order_by('?')
		votepicks = VotePick.objects.filter(episode = episode, player = player).order_by('?')
		currentteamsize = len(teampicks)
		currentvotesize = len(votepicks)
		while currentteamsize > int(episode.team_size):
			#print "t(%i) v(%i) ets(%s) | dropping someone from team" % (currentteamsize, currentvotesize, episode.team_size)
			TeamPick.objects.filter(episode = episode, player = player).order_by('?').first().delete()
			currentteamsize -= 1
		while currentvotesize > 2:
			#print "t(%i) v(%i) ets(%s) | dropping someone from votes" % (currentteamsize, currentvotesize, episode.team_size)
			VotePick.objects.filter(episode = episode, player = player).order_by('?').first().delete()
			currentvotesize -= 1
		# Pick up random if necessary
		if currentteamsize < int(episode.team_size):
			randomteampicks = Castaway.objects.filter(out_episode_number = 0).order_by('?')[:episode.team_size]
			for castaway in randomteampicks:
				try:
					existingpick = TeamPick.objects.get(player = player, episode = episode, castaway = castaway)
				except:
					existingpick = None
				if not existingpick:
					#print "t(%i) v(%i) ets(%s) | adding %s to team" % (currentteamsize, currentvotesize, episode.team_size, castaway)
					randpick = TeamPick(player = player, episode = episode, castaway = castaway)
					randpick.save()
					currentteamsize += 1
					if currentteamsize >= int(episode.team_size):
						break
		if currentvotesize < 2:
			randomvotepicks = Castaway.objects.filter(out_episode_number = 0).order_by('?')[:2]
			for castaway in randomvotepicks:
				try:
					existingpick = VotePick.objects.get(player = player, episode = episode, castaway = castaway)
				except:
					existingpick = None
				if not existingpick:
					#print "t(%i) v(%i) ets(%s) | adding %s to votes" % (currentteamsize, currentvotesize, episode.team_size, castaway)
					randpick = VotePick(player = player, episode = episode, castaway = castaway)
					randpick.save()
					currentvotesize += 1
					if currentvotesize >= 2:
						break
		playerepisode = PlayerEpisode.objects.get(episode = episode, player = player)
		playerepisode.score_lbs()
		playerepisode.save()
		calculatejspsforepisode(episode)
		

def calculatejspsforepisode(episode):
	for player in Player.objects.all():
		calculatejspsforplayerepisode(player, episode)

def calculatejspsforplayerepisode(player, episode):
	for castaway in Castaway.objects.all():
		try:
			pick = TeamPick.objects.get(castaway = castaway, episode = episode, player = player)
		except:
			pick = None
		if not pick:
			continue
		castawaypicks = TeamPick.objects.filter(castaway = castaway, episode__number__lte = episode.number, player = player)
		pick.jsp_score = len(castawaypicks)
		pick.save()

def user_login(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/season31/player/%d' % (user.player.id))
			else:
				return HttpResponse("Your account is disabled.")
		else:
			try:
				userexists = User.objects.get(username = username)
			except:
				userexists = None
			if userexists:
				return render(request, 'season31/login.html', {'error_message': "Incorrect password for %s" % (username),})
			return render(request, 'season31/login.html', {'error_message': "No user found for username %s" % (username),})
	else:
		return render_to_response('season31/login.html', {}, context)

def user_forgotpassword(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		user = User.objects.get(username = username)
		player = Player.objects.get(user = user)
		if player:
			player.forgot_password = True
			player.save()
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("Cant find a player with username: %s" % (username))
	else:
		return render_to_response('season31/login.html', {}, context)
		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/season31/')

def updatescores(request):
	for episode in Episode.objects.all():
		update_episode_score(episode)
	return HttpResponseRedirect('/season31/leaderboard/')

def tallyalljsps(request):
	for episode in Episode.objects.all():
		calculatejspsforepisode(episode)
	return HttpResponseRedirect('/season31/leaderboard/')

def update_episode_score(episode):
	for castawayepisode in episode.castawayepisode_set.all():
		castawayepisode.update_score()
	for playerepisode in episode.playerepisode_set.all():
		playerepisode.score_actions()
		playerepisode.score_votes()
		playerepisode.score_jsps()
		playerepisode.update_score()
	lastplace = 0
	lastscore = 0
	try:
		lastepisode = Episode.objects.get(number = episode.number - 1)
	except:
		lastepisode = None
	counter = 1
	for playerepisode in episode.playerepisode_set.order_by('-total_score').all():
		player = playerepisode.player
		playerepisode.place = counter
		if playerepisode.total_score == lastscore:
			playerepisode.place = lastplace
		if lastepisode:
			last_pe = PlayerEpisode.objects.get(player = player, episode = lastepisode)
			playerepisode.movement = last_pe.place - playerepisode.place
		playerepisode.save()
		lastplace = playerepisode.place
		lastscore = playerepisode.total_score
		if not player.hidden:
			counter += 1

def addepisode(request): # TODO: Add random toggle
	lastepisode = Episode.objects.all().latest()
	try:
		teamsize = request.POST['teamsize']
	except:
		return HttpResponseRedirect('/season31/')
	est = timezone('US/Eastern')
	newepisode = Episode(title = "New Episode", number = lastepisode.number + 1, air_date = datetime.now(est), team_size = teamsize)
	newepisode.save()
	viablepicks = []
	for c in Castaway.objects.all():
		if not c.voted_out():
			nce = CastawayEpisode(castaway = c, episode = newepisode, tribe = c.get_tribe())
			nce.save()
			viablepicks.append(c)
		else:
			c.out_episode_number = lastepisode.number
	for p in Player.objects.all():
		npe = PlayerEpisode(player = p, episode = newepisode)
		npe.save()
	rolloverteam(newepisode)
	return HttpResponseRedirect('/season31/episode/%d' % (newepisode.id))

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
				ce.save()
				if badaction.name == "Out":
					ce.castaway.out_episode_number = 0
					ce.castaway.save()
		else:
			ce.actions.add(action)
			ce.save()
			if action.name == "Out":
				ce.castaway.out_episode_number = ce.episode.number
				ce.castaway.save()
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
	episode = Episode.objects.get(id = e_id)
	if episode:
		update_episode_score(episode)
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def togglescorejsps(request, e_id):
	episode = Episode.objects.get(id = e_id)
	if episode:
		episode.score_jsps = not episode.score_jsps
		episode.save()
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def tallyepisodejsps(request, e_id):
	episode = Episode.objects.get(id = e_id)
	if episode:
		calculatejspsforepisode(episode)
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def unlockepisode(request, e_id):
	episode = Episode.objects.get(id = e_id)
	if episode:
		episode.is_locked = False
		episode.save()
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
	est = timezone('US/Eastern')
	airdatetime.replace(tzinfo = est)
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
	if "check1" in request.POST and "check2" in request.POST and e:
		e.delete()
		return HttpResponseRedirect('/season31/episodes')
	return HttpResponseRedirect('/season31/episode/%d' % int(e_id))

def toggleplayerpaidstatus(request, p_id):
	player = Player.objects.get(id = p_id)
	if "check" in request.POST and player:
		player.paid = not player.paid
		player.save()
	return HttpResponseRedirect('/season31/player/%d' % int(p_id))

def updatecastawayplace(request, c_id):
	castaway = Castaway.objects.get(id = c_id)
	try:
		place = request.POST['place']
	except:
		place = None
	if place:
		castaway.place = place
		castaway.save()
	return HttpResponseRedirect('/season31/castaway/%d' % int(c_id))

def updatecastawayname(request, c_id):
	castaway = Castaway.objects.get(id = c_id)
	try:
		name = request.POST['name']
	except:
		name = None
	if name:
		castaway.name = name
		castaway.save()
	return HttpResponseRedirect('/season31/castaway/%d' % int(c_id))

def togglehelptext(request, p_id):
	player = Player.objects.get(id = p_id)
	if player:
		player.show_help_text = not player.show_help_text
		player.save()
	return HttpResponseRedirect('/season31/player/%d' % int(p_id))

def resetpassword(request, p_id):
	context = RequestContext(request)
	player = Player.objects.get(id = p_id)
	if len(request.POST['password']) < 1:
		return render(request, 'season31/player.html', {'player': player, 'reset_password_error_message': "Password must not be blank",})
	if request.method == 'POST' and player:
		user = player.user
		user.set_password(request.POST['password'])
		user.save()
		player.forgot_password = False
		player.save()
		user = authenticate(username = user.username, password = request.POST['password'])
		login(request, user)
		return HttpResponseRedirect('/season31/player/%d' % (user.player.id))
	return HttpResponseRedirect('/season31/player/%d' % int(p_id))
		

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
	description = request.POST['description']
	a = Action(name = name, score = score, icon_filename = icon_filename, description = description)
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

def pickteams(request, pe_id):
	playerepisode = get_object_or_404(PlayerEpisode, pk=pe_id)
	est = timezone('US/Eastern')
	if playerepisode.episode.air_date < datetime.now(est):
		return render(request, 'season31/player.html', {'player': playerepisode.player, 'expired_error_message': "Episode air time has arrived. Your picks are locked",})
	picks = request.POST.getlist('picks')
	if len(picks) != playerepisode.episode.team_size:
		return render(request, 'season31/player.html', {'player': playerepisode.player, 'team_error_message': "You must select %i castaways" % int(playerepisode.episode.team_size),})
	else:
		playerepisode.clear_team_picks()
		makepick(playerepisode, picks, "TEAM")
		playerepisode.score_lbs()
		playerepisode.update_score()
		playerepisode.save()
		calculatejspsforplayerepisode(playerepisode.player, playerepisode.episode)
		return HttpResponseRedirect('/season31/player/%d' % (playerepisode.player.id))

def pickvotes(request, pe_id):
	playerepisode = get_object_or_404(PlayerEpisode, pk=pe_id)
	est = timezone('US/Eastern')
	if playerepisode.episode.air_date < datetime.now(est):
		return render(request, 'season31/player.html', {'player': playerepisode.player, 'expired_error_message': "Episode air time has arrived. Your picks are locked",})
	picks = request.POST.getlist('picks')
	if len(picks) != 2:
		return render(request, 'season31/player.html', {'player': playerepisode.player, 'vote_error_message': "You must select 2 castaways",})
	else:
		playerepisode.clear_vote_picks()
		makepick(playerepisode, picks, "VOTE")
		return HttpResponseRedirect('/season31/player/%d' % (playerepisode.player.id))

def makepick(playerepisode, picks, type):
	for castawayname in picks:
		castaway = Castaway.objects.get(name = castawayname)
		if type == "TEAM":
			pick = TeamPick(player = playerepisode.player, episode = playerepisode.episode, castaway = castaway)
			pick.save()
		if type == "VOTE":
			pick = VotePick(player = playerepisode.player, episode = playerepisode.episode, castaway = castaway)
			pick.save()
		playerepisode.update_score()
