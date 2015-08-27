from django.contrib import admin

from .models import Player,Castaway,TeamPick,VotePick,Episode,PlayerEpisode,CastawayEpisode,Tribe,Vote,Action

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

class VoteInline(admin.TabularInline):
	model = Vote
	extra = 1

class CastawayActionInline(admin.StackedInline):
	model = CastawayEpisode.actions.through
	extra = 1

# ModelAdmins
class EpisodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['number','title']}),
		('Date',{'fields': ['air_date','is_locked']}),
	]
	inlines = [CastawayEpisodeEpisodeInline]
	list_display = ('number','title','air_date','is_locked')

class CastawayAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['name','age','occupation']}),
		('Full Name',{'fields': ['full_name']}),
		('Game Info',{'fields': ['tribe_name','place','out_episode_number']}),
	]
	inlines = [CastawayEpisodeInline]
	list_display = ('name','age','occupation','tribe_name','place','out_episode_number')

class PlayerAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['user','username','paid','hidden']}),
	]
	inlines = [PlayerEpisodeInline]
	list_display = ('user','username','paid','hidden')

class CastawayEpisodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['castaway','episode','tribe','score','score_has_changed']}),
	]
	inlines = [CastawayActionInline,VoteInline]
	list_filter = ['episode']
	list_display = ('castaway','episode','tribe','score','score_has_changed')

class PlayerEpisodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['player','episode','correctly_predicted_votes','week_score','total_score']}),
		('Score Breakdown',{'fields': ['loyalty_bonus','action_score','vote_off_score','jsp_score','score_has_changed']}),
		('Leaderboard',{'fields': ['movement','place']}),
	]
	list_filter = ['episode']
	list_display = ('player','episode','week_score','total_score','loyalty_bonus','action_score','vote_off_score','jsp_score','score_has_changed')

class TeamPickAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['episode','player','castaway']}),
	]
	list_filter = ['player']
	list_display = ('episode','player','castaway')

class VotePickAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['episode','player','castaway']}),
	]
	list_filter = ['player']
	list_display = ('episode','player','castaway')

class VoteAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['castaway_episode','castaway','is_ftc_vote']}),
	]
	list_filter = ['castaway']
	list_display = ('castaway_episode','castaway','is_ftc_vote')

class ActionAdmin(admin.ModelAdmin):
	fieldsets = [
		('General',{'fields': ['name','description','score','icon_filename']}),
	]
	list_display = ('name','score','icon_filename','description')

# Registrations
admin.site.register(Episode,EpisodeAdmin)
admin.site.register(Player,PlayerAdmin)
admin.site.register(Castaway,CastawayAdmin)
admin.site.register(TeamPick,TeamPickAdmin)
admin.site.register(VotePick,VotePickAdmin)
admin.site.register(PlayerEpisode,PlayerEpisodeAdmin)
admin.site.register(CastawayEpisode,CastawayEpisodeAdmin)
admin.site.register(Tribe)
admin.site.register(Action,ActionAdmin)
admin.site.register(Vote,VoteAdmin)