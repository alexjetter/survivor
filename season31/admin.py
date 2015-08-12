from django.contrib import admin

from .models import Player, Castaway, Pick, Episode, PlayerEpisode, CastawayEpisode, Tribe, Vote, Action

# Inlines
class CastawayEpisodeInline(admin.TabularInline):
	model = CastawayEpisode
	extra = 1
	fk_name = 'castaway'
	
class CastawayEpisodeEpisodeInline(admin.TabularInline):
	model = CastawayEpisode
	extra = 1
	fk_name = 'episode'
	
class PlayerEpisodeInline(admin.TabularInline):
	model = PlayerEpisode
	extra = 1
	
class PickInline(admin.TabularInline):
	model = Pick
	extra = 1
	
class VoteInline(admin.TabularInline):
	model = Vote
	extra = 1
	
class CastawayActionInline(admin.StackedInline):
	model = CastawayEpisode.actions.through
	extra = 1
	
# ModelAdmins
class EpisodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['number','title']}),
		('Date',    {'fields': ['air_date']}),
	]
	inlines = [CastawayEpisodeEpisodeInline]
	
class CastawayAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['name','age','occupation']}),
		('Full Name',    {'fields': ['full_name']}),
	]
	inlines = [CastawayEpisodeInline]
	list_display = ('name', 'age', 'occupation')
	
class PlayerAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['user','paid','hidden']}),
	]
	inlines = [PlayerEpisodeInline]
	list_display = ('user', 'paid', 'hidden')
	
class CastawayEpisodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['castaway','episode','tribe','score']}),
	]
	inlines = [CastawayActionInline, VoteInline]
	list_filter = ['episode']
	list_display = ('castaway', 'episode', 'tribe', 'score')
	
class PlayerEpisodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['player','episode','correctly_predicted_votes','week_score','total_score']}),
		('Score Breakdown',    {'fields': ['action_score','vote_off_score','jsp_score']}),
		('Leaderboard',    {'fields': ['movement','place']}),
	]
	inlines = [PickInline]
	list_filter = ['episode']
	list_display = ('player','episode','week_score','total_score', 'action_score','vote_off_score','jsp_score')
	
class PickAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['player_episode','type','castaway_episode']}),
	]
	list_filter = ['castaway_episode']
	list_display = ('castaway_episode','type','player_episode')
	
class VoteAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['castaway_episode','castaway','is_ftc_vote']}),
	]
	list_filter = ['castaway']
	list_display = ('castaway_episode','castaway','is_ftc_vote')
	
class ActionAdmin(admin.ModelAdmin):
	fieldsets = [
		('General', {'fields': ['name','score','icon_filename']}),
	]
	list_display = ('name','score','icon_filename')

# Registrations
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Castaway, CastawayAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(PlayerEpisode, PlayerEpisodeAdmin)
admin.site.register(CastawayEpisode, CastawayEpisodeAdmin)
admin.site.register(Tribe)
admin.site.register(Action, ActionAdmin)
admin.site.register(Vote, VoteAdmin)