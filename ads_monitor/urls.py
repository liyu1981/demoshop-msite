from django.conf.urls import url

from ads_monitor.views import RuleExecutionResultsView

urlpatterns = [
    url(r'^results$', RuleExecutionResultsView.as_view(),
        name='rule-execution-results'),
]
