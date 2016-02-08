import logging
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from ads_monitor.models import RuleExecutionResult, AdInsight

logger = logging.getLogger(__name__)


class ServerJSTemplateView(TemplateResponseMixin, ContextMixin, View):
    def __init_called_js(self):
        self.__called_js = []

    def call_js(self, jsmodule, jsfunction, jsondata):
        if not self.__called_js:
            self.__init_called_js()
        self.__called_js.append({
            'file': jsmodule,
            'module': jsmodule,
            'function': jsfunction,
            'data': jsondata,
        })

    def __get_server_js(self):
        return 'console.log("hello,world")'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['server_js'] = self.__get_server_js()
        return self.render_to_response(context)


class RuleExecutionResultsView(ServerJSTemplateView):

    template_name = "ads_monitor/rule_execution_results.html"

    def get_context_data(self, **kwargs):
        context = \
            super(RuleExecutionResultsView, self).get_context_data(**kwargs)
        r = RuleExecutionResult.objects.filter(result=False)
        r.select_related('adinsight')
        objs = r.all()
        if objs.count() > 0:
            context['rule_execution_results_headers'] = objs[0].to_dict().keys()
            context['rule_execution_results'] = \
                    [item.to_dict().values() for item in objs]
        return context

