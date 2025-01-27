from django.views.generic import View, TemplateView

class RandomFeedbackSurvey(TemplateView):
  template_name = "feedback.html"


class Home(TemplateView):
  template_name = "home.html"