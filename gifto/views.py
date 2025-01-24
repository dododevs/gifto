from django.views.generic import View, TemplateView

class RandomFeedbackSurvey(TemplateView):
  template_name = "feedback.html"