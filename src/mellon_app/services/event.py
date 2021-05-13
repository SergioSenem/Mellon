from ..models import Event


class EventService:
    def insert(self, request, params):
        event = self.build_event_from_form(request, params)
        event.save()
        return event

    @staticmethod
    def build_event_from_form(request, params):
        event = Event()
        event.name = params.get('name')
        event.message = params.get('message')
        event.date = params.get('date')
        event.has_reminder = params.get('has_reminder')
        event.day_of_week = params.get('day_of_week')
        event.user = request.user
        return event
