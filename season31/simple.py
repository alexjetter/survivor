from operator import attrgetter
from .models import Player, Castaway, TeamPick, VotePick, Episode, PlayerEpisode, CastawayEpisode, Tribe, Vote, Action

# Classes

class SimpleCastawayEpisode:
	id = ""
	castawayid = 0
	castawayname = ""
	tribe = ""
	color = ""
	score = 0
	actions = []
	vote = None
	
class SimplePlayerEpisode:
	id = 0
	playerid = 0
	playername = ""
	loyalty_bonus = 0
	action_score = 0
	vote_off_score = 0
	jsp_score = 0
	week_score = 0
	total_score = 0
	score_delta = 0
	movement = 0
	place = 0
	tpicks = []
	vpicks = []
	
class SimplePerson:
	id = 0
	name = ""
	color = ""
	
class SimpleAction:
	id = 0
	name = ""
	score = 0
	icon_filename = ""
	description = ""
	
class SimpleEpisode:
	id = 0
	name = ""
	short = ""
	title = ""
	number = 0
	air_date = ""
	team_size = 0
	is_locked = False
	score_jsps = False

class SimpleEpisodeStats:
	topcastawayscore = 0
	topcastawayscorers = []
	topplayerscore = 0
	topplayerscorers = []
	topplayermovement = 0
	topplayermovers = []
	mostteamcastawaycount = 0
	mostteamcastaways = []
	mostvotecastawaycount = 0
	mostvotecastaways = []
	correctpredictions = 0

class SimpleObjectWithChildren:
	name = ""
	value = 0
	children = []

class SimpleObject:
	name = ""
	value = 0

# Functions

def getcastawaycolordict(episode):
	try:
		castawayepisodes = CastawayEpisode.objects.filter(episode= episode)
	except:
		castawayepisodes = None
	castawaycolordict = {}
	if castawayepisodes:
		for castawayepisode in castawayepisodes:
			if castawayepisode.castaway.out_episode_number == episode.number:
				castawaycolordict[str(castawayepisode.castaway.name)] = "out"
			else:
				castawaycolordict[str(castawayepisode.castaway.name)] = str(castawayepisode.tribe.color)
	return castawaycolordict

def getsimplecastawayepisodes(episode, castawaycolordict):
	simplecastawayepisodes = []
	for castawayepisode in CastawayEpisode.objects.filter(episode = episode).order_by('tribe', '-score', 'castaway'):
		sce = SimpleCastawayEpisode()
		sce.id = castawayepisode.id
		sce.castawayid = castawayepisode.castaway.id
		sce.castawayname = castawayepisode.castaway.name
		sce.tribe = castawayepisode.tribe.name
		sce.color = castawaycolordict[str(sce.castawayname)]
		sce.score = castawayepisode.score
		sce.actions = []
		for action in castawayepisode.actions.all():
			sa = SimpleAction()
			sa.name = action.name
			sa.score = action.score
			sa.icon_filename = action.icon_filename
			sa.description = action.description
			sce.actions.append(sa)
		try:
			vote = Vote.objects.get(castaway_episode = castawayepisode)
		except:
			vote = None
		if vote:
			sce.vote = SimplePerson()
			sce.vote.id = vote.id
			sce.vote.name = vote.castaway.name
			sce.vote.color = castawaycolordict[str(sce.vote.name)]
		simplecastawayepisodes.append(sce)
	return simplecastawayepisodes

def getsimpleplayerepisodes(episode, castawaycolordict, sortby):
	#build css reference
	try:
		castawayepisodes = CastawayEpisode.objects.filter(episode= episode)
	except:
		castawayepisodes = None
	castawaycolordict = {}
	if castawayepisodes:
		for castawayepisode in castawayepisodes:
			if castawayepisode.castaway.out_episode_number == episode.number:
				castawaycolordict[str(castawayepisode.castaway.name)] = "out"
			else:
				castawaycolordict[str(castawayepisode.castaway.name)] = str(castawayepisode.tribe.color)
	#build leaderboardPEs
	simpleplayerepisodes = []
	topplayerscore = 0
	for playerepisode in PlayerEpisode.objects.filter(player__hidden = False, episode = episode).order_by(sortby):
		spe = SimplePlayerEpisode()
		spe.id = playerepisode.id
		spe.playerid = playerepisode.player.id
		spe.playername = playerepisode.player.user.username
		spe.week_score = playerepisode.week_score
		spe.total_score = playerepisode.total_score
		topplayerscore = max(topplayerscore, playerepisode.total_score)
		spe.score_delta = playerepisode.total_score - topplayerscore
		spe.movement = playerepisode.movement
		spe.place = playerepisode.place
		spe.loyalty_bonus = playerepisode.loyalty_bonus
		spe.action_score = playerepisode.action_score
		spe.vote_off_score = playerepisode.vote_off_score
		spe.jsp_score = playerepisode.jsp_score
		spe.tpicks = []
		spe.vpicks = []
		for pick in TeamPick.objects.filter(episode = episode, player = playerepisode.player):
			sp = SimplePerson()
			sp.id = pick.castaway.id
			sp.name = pick.castaway.name
			sp.color = castawaycolordict[str(sp.name)]
			spe.tpicks.append(sp)
		# TODO: Sorting solution. This only works because "out" is last alphabetically
		#spe.tpicks = sorted(spe.tpicks, key=attrgetter('name'))
		for pick in VotePick.objects.filter(episode = episode, player = playerepisode.player):
			sp = SimplePerson()
			sp.id = pick.castaway.id
			sp.name = pick.castaway.name
			sp.color = castawaycolordict[str(sp.name)]
			spe.vpicks.append(sp)
		simpleplayerepisodes.append(spe)
	return simpleplayerepisodes
	
def getsimpleactions():
	simpleactions = []
	for action in Action.objects.all():
		sa = SimpleAction()
		sa.id = action.id
		sa.name = action.name
		sa.score = action.score
		sa.icon_filename = action.icon_filename
		sa.description = action.description
		simpleactions.append(sa)
	return simpleactions
	
def getsimpletribes():
	simpletribes = []
	for tribe in Tribe.objects.all():
		st = SimplePerson()
		st.id = tribe.id
		st.name = tribe.name
		st.color = tribe.color
		simpletribes.append(st)
	return simpletribes
	
def getsimpleepisodes():
	simpleepisodes = []
	for episode in Episode.objects.all():
		simpleepisodes.append(getsimpleepisode(episode))
	return simpleepisodes
	
def getsimpleepisode(episode):
	se = SimpleEpisode()
	se.id = episode.id
	se.name = "Episode %i" % (episode.number)
	se.short = episode.short()
	se.title = episode.title
	se.number = episode.number
	se.air_date = episode.air_date
	se.air_day = episode.air_day()
	se.team_size = episode.team_size
	se.is_locked = episode.is_locked
	se.score_jsps = episode.score_jsps
	return se
	
def getsimplejspsforepisode(episode):
	if not episode.is_locked:
		return None
	simplejsps = []
	headerobject = SimpleObjectWithChildren()
	headerobject.name = "Player"
	headerobject.children = []
	for castaway in Castaway.objects.all():
		headerobject.children.append(castaway.name)
	simplejsps.append(headerobject)
	for player in Player.objects.filter(hidden = False):
		playerjsp = SimpleObjectWithChildren()
		playerjsp.name = player.user.username
		playerjsp.children = []
		for castaway in Castaway.objects.all():
			if castaway.out_episode_number == 0 or castaway.out_episode_number > episode.number:
				count = TeamPick.objects.filter(player = player, castaway = castaway, episode__number__lte = episode.number).count()
			else:
				count = 0
			playerjsp.children.append(count)
			playerjsp.value += count
		simplejsps.append(playerjsp)
	return simplejsps
	
def getsimplejspsforplayer(player):
	simplejsps = []
	headerobject = SimpleObjectWithChildren()
	headerobject.name = "Episode"
	headerobject.children = []
	for episode in Episode.objects.filter(is_locked = True):
		headerobject.children.append(episode.short)
	simplejsps.append(headerobject)
	for castaway in Castaway.objects.all():
		castawayjsp = SimpleObjectWithChildren()
		castawayjsp.name = castaway.name
		castawayjsp.children = []
		for episode in Episode.objects.filter(is_locked = True):
			if castaway.out_episode_number == 0 or castaway.out_episode_number > episode.number:
				count = TeamPick.objects.filter(player = player, castaway = castaway, episode__number__lte = episode.number).count()
			else:
				count = 0
			castawayjsp.children.append(count)
		simplejsps.append(castawayjsp)
	return simplejsps

def getsimpleepisodestats(episode, castawaycolordict):
	simpleepisodestats = SimpleEpisodeStats()
	for playerepisode in PlayerEpisode.objects.filter(player__hidden = False, episode = episode).order_by('-total_score'):
		if playerepisode.week_score > simpleepisodestats.topplayerscore:
			simpleepisodestats.topplayerscore = playerepisode.week_score
			simpleepisodestats.topplayerscorers = []
			sp = SimplePerson()
			sp.id = playerepisode.player.id
			sp.name = playerepisode.player.user.username
			simpleepisodestats.topplayerscorers.append(sp)
		elif playerepisode.week_score == simpleepisodestats.topplayerscore:
			sp = SimplePerson()
			sp.id = playerepisode.player.id
			sp.name = playerepisode.player.user.username
			simpleepisodestats.topplayerscorers.append(sp)
		if playerepisode.movement > simpleepisodestats.topplayermovement:
			simpleepisodestats.topplayermovement = playerepisode.movement
			simpleepisodestats.topplayermovers = []
			sp = SimplePerson()
			sp.id = playerepisode.player.id
			sp.name = playerepisode.player.user.username
			simpleepisodestats.topplayermovers.append(sp)
		elif playerepisode.movement == simpleepisodestats.topplayermovement:
			sp = SimplePerson()
			sp.id = playerepisode.player.id
			sp.name = playerepisode.player.user.username
			simpleepisodestats.topplayermovers.append(sp)
		if playerepisode.vote_off_score > 0:
			simpleepisodestats.correctpredictions += 1
	for castawayepisode in CastawayEpisode.objects.filter(episode = episode).order_by('-score'):
		if castawayepisode.score <= 0:
			continue
		if castawayepisode.score > simpleepisodestats.topcastawayscore:
			simpleepisodestats.topcastawayscore = castawayepisode.score
			simpleepisodestats.topcastawayscorers = []
			sp = SimplePerson()
			sp.id = castawayepisode.castaway.id
			sp.name = castawayepisode.castaway.name
			sp.color = castawaycolordict[str(sp.name)]
			simpleepisodestats.topcastawayscorers.append(sp)
		elif castawayepisode.score == simpleepisodestats.topcastawayscore:
			sp = SimplePerson()
			sp.id = castawayepisode.castaway.id
			sp.name = castawayepisode.castaway.name
			sp.color = castawaycolordict[str(sp.name)]
			simpleepisodestats.topcastawayscorers.append(sp)
	for castaway in Castaway.objects.all():
		teampicks = TeamPick.objects.filter(episode = episode, castaway = castaway)
		if teampicks.count() > simpleepisodestats.mostteamcastawaycount:
			simpleepisodestats.mostteamcastawaycount = teampicks.count()
			simpleepisodestats.mostteamcastaways = []
			sp = SimplePerson()
			sp.id = castaway.id
			sp.name = castaway.name
			sp.color = castawaycolordict[str(sp.name)]
			simpleepisodestats.mostteamcastaways.append(sp)
		elif teampicks.count() == simpleepisodestats.mostteamcastawaycount:
			sp = SimplePerson()
			sp.id = castaway.id
			sp.name = castaway.name
			sp.color = castawaycolordict[str(sp.name)]
			simpleepisodestats.mostteamcastaways.append(sp)
		votepicks = VotePick.objects.filter(episode = episode, castaway = castaway)
		if votepicks.count() > 0:
			if votepicks.count() > simpleepisodestats.mostvotecastawaycount:
				simpleepisodestats.mostvotecastawaycount = votepicks.count()
				simpleepisodestats.mostvotecastaways = []
				sp = SimplePerson()
				sp.id = castaway.id
				sp.name = castaway.name
				sp.color = castawaycolordict[str(sp.name)]
				simpleepisodestats.mostvotecastaways.append(sp)
			elif votepicks.count() == simpleepisodestats.mostvotecastawaycount:
				sp = SimplePerson()
				sp.id = castaway.id
				sp.name = castaway.name
				sp.color = castawaycolordict[str(sp.name)]
				simpleepisodestats.mostvotecastaways.append(sp)
	return simpleepisodestats
	