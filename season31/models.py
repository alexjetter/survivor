import logging
import pytz
from pytz import timezone
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class Castaway(models.Model):
	name = models.CharField(max_length = 32)
	full_name = models.CharField(max_length = 32)
	age = models.PositiveIntegerField(default = 0)
	occupation = models.CharField(max_length = 32)
	tribe_name = models.CharField(max_length = 16)
	place = models.PositiveIntegerField(default = 0)
	out_episode_number = models.PositiveIntegerField(default = 0)
	def __unicode__(self):
		return self.name
	def get_tribe(self):
		tribe = self.castawayepisode_set.latest().tribe
		if tribe.name != self.tribe_name:
			self.tribe_name = tribe.name
			self.save()
		return tribe
	def get_first_initial(self):
		return self.name[0]
	def voted_out(self):
		if self.out_episode_number > 0:
			return True
		else:
			return False
	class Meta:
		ordering = ('place','tribe_name','name',)

class Player(models.Model):
	user = models.OneToOneField(User)
	username = models.CharField(max_length = 32, default = "")
	paid = models.BooleanField(default = False)
	hidden = models.BooleanField(default = False)
	show_help_text = models.BooleanField(default = True)
	def __unicode__(self):
		return self.user.username
	def get_full_name(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)
	def get_latest_player_episode(self):
		return PlayerEpisode.objects.filter(player = self).latest()
	def get_latest_episode(self):
		try:
			latestepisode = Episode.objects.filter(is_locked = True).latest()
		except:
			latestepisode = None;
		return latestepisode
	def get_next_episode(self):
		try:
			nextepisode = Episode.objects.filter(is_locked = False).latest()
		except:
			nextepisode = None;
		return nextepisode
	def get_leaderboard_player_episodes(self):
		players = Player.objects.filter(hidden = False)
		playerepisodes = PlayerEpisode.objects.filter(player__in = players)
		return playerepisodes.filter(episode = self.get_latest_episode()).order_by('-total_score')
	class Meta:
		ordering = ('username',)

class Tribe(models.Model):
	name = models.CharField(max_length = 16)
	color = models.CharField(max_length = 16)
	def __unicode__(self):
		return self.name
	def get_all_episodes(self):
		return get_all_episodes()
	class Meta:
		ordering = ('name',)

class Action(models.Model):
	name = models.CharField(max_length = 32)
	score = models.IntegerField(default = 1)
	icon_filename = models.CharField(max_length = 32)
	description = models.CharField(max_length = 64)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ('-score','name',)

class Episode(models.Model):
	title = models.CharField(max_length = 64)
	number = models.PositiveIntegerField(default = 0)
	air_date = models.DateTimeField()
	players = models.ManyToManyField(Player, through = 'PlayerEpisode', through_fields = ('episode', 'player'))
	castaways = models.ManyToManyField(Castaway, through = 'CastawayEpisode', through_fields = ('episode', 'castaway'))
	team_size = models.PositiveIntegerField(default = 5)
	is_locked = models.BooleanField(default = False)
	def __unicode__(self):
		return "Episode %i" % (self.number)
	def get_playerepisodes(self):
		players = Player.objects.filter(hidden = False)
		playerepisodes = PlayerEpisode.objects.filter(player__in = players)
		return playerepisodes.filter(episode = self).order_by('-total_score')
	def update_scores(self):
		return update_scores()
	def get_prev_episode(self):
		try:
			prev_e = Episode.objects.get(number = self.number - 1)
		except:
			prev_e = None
		return prev_e
	def get_next_episode(self):
		try:
			next_e = Episode.objects.get(number = self.number + 1)
		except:
			next_e = None
		return next_e
	def short(self):
		return "E%s" % ("{0:02d}".format(self.number))
	def air_day(self):
		weekdays = {0: "Sunday",1: "Monday",2: "Tuesday",3: "Wednesday",4: "Thursday",5: "Friday",6: "Saturday",}
		return weekdays.get(self.air_date.weekday(),"ERROR")
	def check_lock(self):
		if self.is_locked:
			return True
		est = timezone('US/Eastern')
		if datetime.now(est) > self.air_date:
			self.is_locked = True
			self.save()
			return True
		return False
	def time_to_lock(self):
		est = timezone('US/Eastern')
		if self.is_locked:
			return "Locked"
		timedelta = self.air_date - datetime.now(est)
		if timedelta.days > 0:
			return "%i day(s), %i hour(s), %i minute(s)" % (timedelta.days, timedelta.seconds//3600, (timedelta.seconds//60)%60)
		if timedelta.days == 0 and timedelta.seconds//3600 > 0:
			return "%i hour(s), %i minute(s)" % (timedelta.seconds//3600, (timedelta.seconds//60)%60)
		return "%i minute(s)" % ((timedelta.seconds//60)%60)
	class Meta:
		ordering = ('number',)
		get_latest_by = 'air_date'

class PlayerEpisode(models.Model):
	player = models.ForeignKey(Player)
	episode = models.ForeignKey(Episode)
	loyalty_bonus = models.PositiveIntegerField(default = 0)
	action_score = models.IntegerField(default = 0)
	correctly_predicted_votes = models.PositiveIntegerField(default = 0)
	vote_off_score = models.PositiveIntegerField(default = 0)
	jsp_score = models.PositiveIntegerField(default = 0)
	week_score = models.IntegerField(default = 0)
	total_score = models.IntegerField(default = 0)
	movement = models.IntegerField(default = 0)
	place = models.PositiveIntegerField(default = 0)
	score_has_changed = models.BooleanField(default = False)
	def __unicode__(self):
		return "%s | %s" % (self.player.user.username, self.episode)
	def get_team_picks(self):
		return TeamPick.objects.filter(episode = self.episode, player = self.player)
	def get_vote_picks(self):
		return VotePick.objects.filter(episode = self.episode, player = self.player)
	def clear_team_picks(self):
		for pick in self.get_team_picks():
			pick.delete()
	def clear_vote_picks(self):
		for pick in self.get_vote_picks():
			pick.delete()
	def get_pick_options(self):
		return CastawayEpisode.objects.filter(episode = Episode.objects.latest())
	def replicate_picks(self):
		for pick in get_team_picks():
			print pick
	def update_score(self):
		if self.score_has_changed:
			try:
				lastplayerepisode = PlayerEpisode.objects.get(player = self.player, episode = Episode.objects.get(number = self.episode.number - 1))
			except:
				lastplayerepisode = None
			if lastplayerepisode:
				self.total_score = lastplayerepisode.total_score
			else:
				self.total_score = 0
			self.loyalty_bonus = 0
			self.week_score = 0
			self.action_score = 0
			self.jsp_score = 0
			self.correctly_predicted_votes = 0
			if lastplayerepisode:
				for pick in self.get_team_picks():
					for last_pick in lastplayerepisode.get_team_picks():
						if pick.castaway == last_pick.castaway:
							self.loyalty_bonus += 1
			for pick in self.get_team_picks():
				ce = pick.castaway_episode()
				if ce:
					self.action_score += ce.score
			for pick in self.get_vote_picks():
				try:
					vo_action = pick.castaway_episode().actions.filter(name = "Out") # TODO: dont hardcode this name
				except:
					vo_action = None
				if vo_action:
					self.correctly_predicted_votes += 1
			self.vote_off_score = self.correctly_predicted_votes * 10 # TODO: dont hardcode this score
			self.week_score = self.action_score + self.vote_off_score + self.jsp_score + self.loyalty_bonus
			self.total_score += self.week_score
			self.score_has_changed = False
			self.save()
	class Meta:
		ordering = ('episode', 'player')
		get_latest_by = 'episode'

class CastawayEpisode(models.Model):
	castaway = models.ForeignKey(Castaway)
	episode = models.ForeignKey(Episode)
	tribe = models.ForeignKey(Tribe)
	actions = models.ManyToManyField(Action, blank = True)
	score = models.IntegerField(default = 0)
	score_has_changed = models.BooleanField(default = False)
	def __unicode__(self):
		return "%s | %s" % (self.castaway.name, self.episode)
	def update_score(self):
		if self.score_has_changed:
			self.score = 0
			for action in self.actions.all():
				self.score += action.score
			self.score_has_changed = False
			self.save()
	class Meta:
		ordering = ('episode', 'tribe', '-score', 'castaway')
		get_latest_by = 'episode'

class TeamPick(models.Model):
	episode = models.ForeignKey(Episode)
	player = models.ForeignKey(Player)
	castaway = models.ForeignKey(Castaway)
	def __unicode__(self):
		return "%s | %s | %s | Team Pick" % (self.episode.short(), self.player.user.username, self.castaway.name)
	def castaway_episode(self):
		try:
			castawayepisode = CastawayEpisode.objects.get(castaway = self.castaway, episode = self.episode)
		except:
			castawayepisode = None
		return castawayepisode
	def player_episode(self):
		try:
			playerepisode = PlayerEpisode.objects.get(player = self.player, episode = self.episode)
		except:
			playerepisode = None
		return playerepisode
	class Meta:
		ordering = ('episode', 'player', 'castaway')
		
class VotePick(models.Model):
	episode = models.ForeignKey(Episode)
	player = models.ForeignKey(Player)
	castaway = models.ForeignKey(Castaway)
	def __unicode__(self):
		return "%s | %s | %s | Team Pick" % (self.episode.short(), self.player.user.username, self.castaway.name)
	def castaway_episode(self):
		try:
			castawayepisode = CastawayEpisode.objects.get(castaway = self.castaway, episode = self.episode)
		except:
			castawayepisode = None
		return castawayepisode
	def player_episode(self):
		try:
			playerepisode = PlayerEpisode.objects.get(player = self.player, episode = self.episode)
		except:
			playerepisode = None
		return playerepisode
	class Meta:
		ordering = ('episode', 'player', 'castaway')

class Vote(models.Model):
	castaway_episode = models.ForeignKey(CastawayEpisode)
	castaway = models.ForeignKey(Castaway)
	is_ftc_vote = models.BooleanField(default = False)
	def __unicode__(self):
		return "%s | %s voted for %s" % (self.castaway_episode.episode, self.castaway_episode.castaway.name, self.castaway.name)
	class Meta:
		ordering = ('castaway_episode', 'castaway')
