class SimpleCastawayEpisode:
	castawayname = ""
	castawayid = 0
	tribe = ""
	color = ""
	score = 0
	actions = []
	vote = None
	
class SimplePlayerEpisode:
	playerepisodeid = 0
	playername = ""
	playerid = 0
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
	name = ""
	id = 0
	color = ""
	
class SimpleAction:
	name = ""
	score = 0
	icon_filename = ""
	description = ""
	
class SimpleEpisodeStats:
	topplayerscore = 0
	topplayerscorers = []
	topcastawayscore = 0
	topcastawayscorers = []
	topplayermovement = 0
	topplayermovers = []
	mostpickedcastaway = ""
	leastpickedcastaway = ""
	mostvotecastaway = ""
	leastvotecastaway = ""
	correctpredictions = 0
	