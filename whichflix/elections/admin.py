from django.contrib import admin

from whichflix.elections.models import Election, Participant, Candidate, Vote


admin.site.register(Election)
admin.site.register(Participant)
admin.site.register(Candidate)
admin.site.register(Vote)
