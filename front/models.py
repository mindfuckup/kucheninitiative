# coding=utf-8

from django.db import models
from django.contrib.auth import models as auth_models


class UserProfile(models.Model):
    COURSE_CHOICES = (
        ('B', 'Bauingenieurwesen'),
        ('E', 'Elektrotechnik'),
        ('EEU', 'Erneuerbare Energien'),
        ('I', 'Informatik'),
        ('L', 'Landschaftsarchitektur'),
        ('M', 'Maschinentechnik'),
        ('R', 'Raumplanung'),
    )
    user = models.OneToOneField(auth_models.User)
    course = models.CharField(u'studiengang', max_length=3, choices=COURSE_CHOICES)
    phone = models.CharField(u'natel', max_length=13, null=True, blank=True)

    def __unicode__(self):
        return self.user.username


class Assignment(models.Model):
    User = models.ForeignKey(auth_models.User)
    date = models.DateField(u'datum')
    unfulfilled = models.BooleanField(u'nicht erfüllt', default=False)

    def __unicode__(self):
        return '%s: %s' % (self.date, self.User.username)

    class Meta:
        verbose_name = 'termin'
        verbose_name_plural = 'termine'
        unique_together = ('User', 'date')
        ordering = ['-date']


class Semester(models.Model):
    SEASON_CHOICES = (
        ('H', 'Herbstsemester'),
        ('F', 'Frühlingssemester'),
    )
    year = models.PositiveIntegerField(u'jahr')
    season = models.CharField(u'semester', max_length=1, choices=SEASON_CHOICES)
    start_date = models.DateField(u'semesterbeginn')
    end_date = models.DateField(u'semesterende')
    weekdays = models.CommaSeparatedIntegerField(u'kuchentage', max_length=9, null=True, blank=True,
            help_text=u'Kommagetrennte Liste der Wochentage (1-5), an welchen es Kuchen gibt.')

    def weekday_list(self):
        return [int(day) for day in self.weekdays.split(',')]

    def assignments(self):
        return Assignment.objects.filter(date__lte=self.start_date, date__gte=self.start_date)

    def __unicode__(self):
        return '%ss %s' % (self.season, self.year)

    class Meta:
        verbose_name_plural = 'semester'
        unique_together = ('year', 'season')
        ordering = ['start_date']


def name(self):
    """Return either full user first and last name or the username, if no
    further data is found."""
    if self.first_name or self.last_name:
        return ' '.join(filter(None, [self.first_name, self.last_name]))
    return self.username
auth_models.User.add_to_class('name', name)
