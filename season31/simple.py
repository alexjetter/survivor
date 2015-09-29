class SimpleCastawayEpisode:
	castawayname = ""
	castawayid = 0
	tribe = ""
	color = ""
	score = 0
	actions = []
	vote = None
	
class SimplePlayerEpisode:
	playername = ""
	playerid = 0
	loyalty_bonus = 0
	action_score = 0
	vote_off_score = 0
	jsp_score = 0
	week_score = 0
	total_score = 0
	movement = 0
	place = 0
	tpicks = []
	vpicks = []
	
class SimplePick:
	castawayname = ""
	castawayid = 0
	color = ""
	
class SimpleAction:
	name = ""
	score = 0
	icon_filename = ""
	description = ""
	
class SimpleEpisodeStats:
	topscore = 0
	topscorer = ""
	topmovement = 0
	topmover = ""
	correctpredictions = 0
	