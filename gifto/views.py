from django.views.generic import View, TemplateView

from gifto.models import Hobby


class RandomFeedbackSurvey(TemplateView):
  template_name = "feedback.html"


class Home(TemplateView):
  template_name = "home.html"

  def get_context_data(self, **kwargs):
    return {
      **super().get_context_data(**kwargs),
      "all_hobbies": Hobby.objects.all()
    }