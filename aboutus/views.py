from django.views.generic import TemplateView


class AboutUs(TemplateView):
    template_name = 'aboutus/about.html'

