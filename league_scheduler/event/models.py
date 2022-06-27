from django.db import models
from django.db.models import UniqueConstraint
from users.models import MyUser

class Event(models.Model):
    """
    An event that participants sign up for. It lasts a number of rounds.
    It doesn't need to be a month long league. It could be a 1 day tournament.
    """
    name = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    participants = models.ManyToManyField(MyUser, through = "MyUserEvent")

class MyUserEvent(models.Model):
    user  = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    event  = models.ForeignKey(Event, on_delete = models.CASCADE)
    DROPPED = 0
    JOINED = 1
    STATUS_CHOICES = [
            (JOINED, "Joined"),
            (DROPPED, "Dropped"),
        ]
    status = models.PositiveSmallIntegerField(choices = STATUS_CHOICES, default = JOINED)

    class Meta:
        constraints = [
                UniqueConstraint(fields=['user', 'event'], name='unique_user_to_event')
            ]

class Round(models.Model):
    """
    An event is broken up into a number of rounds.
    """
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

class Match(models.Model):
    """
    A match is a game between two players in the event. Each player should get a match every round.
    """
    UNSCHEDULED = 0
    PLAYER_1_WIN = 1
    PLAYER_2_WIN = 2
    UNPLAYED = 3
    RESULT_CHOICES = [
            (UNSCHEDULED, "Unscheduled"),
            (PLAYER_1_WIN, "Player 1 Won"),
            (PLAYER_2_WIN, "Player 2 Won"),
            (UNPLAYED, "The game didn't happen."),
        ]
    player_1 = models.ForeignKey(MyUser, null = True, blank = True, on_delete = models.SET_NULL, related_name = "matches_as_first_player")
    player_2 = models.ForeignKey(MyUser, null = True, blank = True, on_delete = models.SET_NULL, related_name = "matches_as_second_player")
    roundd = models.ForeignKey(Round, on_delete = models.CASCADE, verbose_name = "round")
    result = models.PositiveSmallIntegerField(choices = RESULT_CHOICES, default = UNSCHEDULED)
    player_1_points = models.PositiveSmallIntegerField(null = True, blank = True)
    player_2_points = models.PositiveSmallIntegerField(null = True, blank = True)

class MatchReport(models.Model):
    """
    Both players submit scores for a match using a match report. If they agree, the match results are 
    finalized. Otherwise, an event admin has to step in to finalize the match result.
    """
    MATCH_REPORT_CHOICES = [
            (Match.PLAYER_1_WIN, "Player 1 Won"),
            (Match.PLAYER_2_WIN, "Player 2 Won"),
            (Match.UNPLAYED, "The game didn't happen."),
        ]
    match     = models.ForeignKey(Match,  on_delete = models.CASCADE)
    submitter = models.ForeignKey(MyUser, on_delete = models.CASCADE, related_name = "submitted_match_reports")
    player_1  = models.ForeignKey(MyUser, on_delete = models.CASCADE, related_name = "match_reports_as_first_player")
    player_2  = models.ForeignKey(MyUser, on_delete = models.CASCADE, related_name = "match_reports_as_second_player")
    result = models.PositiveSmallIntegerField(choices = MATCH_REPORT_CHOICES)
    player_1_points = models.PositiveSmallIntegerField()
    player_2_points = models.PositiveSmallIntegerField()

