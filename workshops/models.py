from django.db import models

#------------------------------------------------------------

STR_SHORT   =  10         # length of short strings
STR_MED     =  40         # length of medium strings
STR_LONG    = 100         # length of long strings
STR_REG_KEY =  20         # length of Eventbrite registration key

#------------------------------------------------------------

class Site(models.Model):
    '''Represent a site where workshops are hosted.'''

    domain     = models.CharField(max_length=STR_LONG, unique=True)
    fullname   = models.CharField(max_length=STR_LONG, unique=True)
    country    = models.CharField(max_length=STR_LONG, null=True)

    def __str__(self):
        return self.domain

#------------------------------------------------------------

class Airport(models.Model):
    '''Represent an airport (used to locate instructors).'''

    iata      = models.CharField(max_length=STR_SHORT, unique=True)
    fullname  = models.CharField(max_length=STR_LONG, unique=True)
    country   = models.CharField(max_length=STR_LONG)
    latitude  = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.iata

#------------------------------------------------------------

class Person(models.Model):
    '''Represent a single person.'''

    personal   = models.CharField(max_length=STR_LONG)
    middle     = models.CharField(max_length=STR_LONG, null=True)
    family     = models.CharField(max_length=STR_LONG)
    email      = models.CharField(max_length=STR_LONG, unique=True, null=True)
    gender     = models.CharField(max_length=STR_SHORT, null=True)
    active     = models.NullBooleanField()
    airport    = models.ForeignKey(Airport, null=True)
    github     = models.CharField(max_length=STR_MED, unique=True, null=True)
    twitter    = models.CharField(max_length=STR_MED, unique=True, null=True)
    url        = models.CharField(max_length=STR_LONG, null=True)

    def __str__(self):
        middle = ''
        if self.middle is not None:
            middle = ' {0}'.format(self.middle)
        return '{0}{1} {2} <{3}>'.format(self.personal, middle, self.family, self.email)

#------------------------------------------------------------

class Project(models.Model):
    '''Keep track of the kinds of project we support.'''

    slug       = models.CharField(max_length=STR_SHORT, unique=True)
    name       = models.CharField(max_length=STR_MED, unique=True)
    details    = models.CharField(max_length=STR_LONG)

    def __str__(self):
        return self.slug

#------------------------------------------------------------

class Event(models.Model):
    '''Represent a single event.'''

    site       = models.ForeignKey(Site)
    project    = models.ForeignKey(Project)
    organizer  = models.ForeignKey(Site, related_name='organizer', null=True)
    start      = models.DateField()
    end        = models.DateField(null=True)
    slug       = models.CharField(max_length=STR_LONG, unique=True)
    url        = models.CharField(max_length=STR_LONG, unique=True, null=True)
    reg_key    = models.CharField(max_length=STR_REG_KEY, null=True)
    attendance = models.IntegerField(null=True)
    admin_fee  = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.slug

#------------------------------------------------------------

class Role(models.Model):
    '''Enumerate roles in workshops.'''

    name       = models.CharField(max_length=STR_MED)

    def __str__(self):
        return self.name

#------------------------------------------------------------

class Task(models.Model):
    '''Represent who did what at events.'''

    event      = models.ForeignKey(Event)
    person     = models.ForeignKey(Person)
    role       = models.ForeignKey(Role)

    def __str__(self):
        return '{0}/{1}={2}'.format(self.event, self.person, self.task)

#------------------------------------------------------------

class Cohort(models.Model):
    '''Represent a training cohort.'''

    start      = models.DateField()
    name       = models.CharField(max_length=STR_MED)
    active     = models.BooleanField(default=True)
    venue      = models.ForeignKey(Site, null=True) # null for online
    qualifies  = models.BooleanField(default=True)

    def __str__(self):
        return self.name

#------------------------------------------------------------

class Trainee(models.Model):
    '''Represent someone taking the instructor training course.'''

    person     = models.ForeignKey(Person)
    cohort     = models.ForeignKey(Cohort)
    complete   = models.NullBooleanField()

    def __str__(self):
        return '{0}/{1}={2}'.format(self.person, self.cohort, self.complete)

#------------------------------------------------------------

class Skill(models.Model):
    '''Represent a skill someone might teach.'''

    name       = models.CharField(max_length=STR_MED)

    def __str__(self):
        return self.name

#------------------------------------------------------------

class Qualification(models.Model):
    '''What is someone qualified to teach?'''

    person     = models.ForeignKey(Person)
    skill      = models.ForeignKey(Skill)

    def __str__(self):
        return '{0}/{1}'.format(self.person, self.skill)

#------------------------------------------------------------

class Badge(models.Model):
    '''Represent a badge we award.'''

    name       = models.CharField(max_length=STR_MED)
    title      = models.CharField(max_length=STR_MED)
    criteria   = models.CharField(max_length=STR_LONG)

    def __str__(self):
        return self.name

#------------------------------------------------------------

class Award(models.Model):
    '''Represent a particular badge earned by a person.'''

    person     = models.ForeignKey(Person)
    badge      = models.ForeignKey(Badge)
    awarded    = models.DateField()

    def __str__(self):
        return '{0}/{1}/{2}'.format(self.person, self.badge, self.awarded)
