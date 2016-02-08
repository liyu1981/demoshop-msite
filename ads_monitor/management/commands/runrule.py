import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from ads_monitor.rule import parse as rule_parse
from ads_monitor.rule import get_rule_examples
from ads_monitor.models import Rule, AdInsight, RuleExecutionResult
from datetime import datetime
from django.utils import timezone
import pprint


def _now():
    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    if settings.USE_TZ:
        # timeit shows that datetime.now(tz=utc) is 24% slower
        return datetime.utcnow().replace(tzinfo=timezone.utc)
    else:
        return datetime.now()


def usage():
        return '''Usage:
python manage.py runrule list                   -- list all rules
python manage.py runrule example                -- show some examples of rules
python manage.py runrule all                    -- execute each rules, one by one
python manage.py runrule once <rule_id>         -- run rule <rule_id> once
'''


class Command(BaseCommand):
    help = '''Evaluate all rules.'''

    def add_arguments(self, parser):
        parser.add_argument('action', nargs='?', type=str)
        parser.add_argument('params', nargs='*', type=str)

    def handle(self, *args, **options):
        if (not 'action' in options) or (not options['action']):
            self.stdout.write(usage())
            return

        action = options['action']
        getattr(self, 'handle_%s' % action)(args, options)

    def handle_example(self, args, options):
        self.stdout.write('\n'.join(get_rule_examples()) + '\n')

    def handle_list(self, args, options):
        rules = Rule.objects.all()
        for rule in rules:
            self.stdout.write('==rule %s==%s' % (rule.id, rule.rule_json))

    def _get_adinsight_data(self, adinsight):
        return [
            adinsight.id,
            adinsight.campaign_name,
            adinsight.campaign_id,
            adinsight.adset_name,
            adinsight.adset_id,
            adinsight.ad_name,
            adinsight.ad_id,
            adinsight.past_2d_cost,
            adinsight.past_2d_install,
            adinsight.past_2d_CPI,
            adinsight.past_7d_cost,
            adinsight.past_7d_install,
            adinsight.past_7d_CPI
        ]

    def _run_once_internal(self, rule):
        robj = rule_parse(rule.rule_json)
        adinsights = AdInsight.objects.all()
        data = [self._get_adinsight_data(adinsight) for adinsight in adinsights]
        results = robj.execute(data)
        for result in results:
            #self.stdout.write('will execute on data: %s' % (pprint.pformat(vars(adinsight))))
            rer = RuleExecutionResult()
            rer.result = result[1]
            rer.rule = rule
            self.stdout.write(str(result))
            rer.adinsight = AdInsight.objects.get(id=result[0])
            rer.execution_time = _now()
            rer.save()
            self.stdout.write(
                ('executed rule {} against adinsight {}, result={}').format(
                    rule.id, rer.adinsight.id, rer.result
                )
            )

    def _run_once(self, rule_id):
        try:
            r = Rule.objects.get(id=rule_id)
        except Rule.DoesNotExist:
            raise CommandError('no rule id=%s' % (rule_id))

        self.stdout.write('now running: rule %s' % (r.id))
        self._run_once_internal(r)

    def handle_all(self, args, options):
        rules = Rule.objects.all()
        for rule in rules:
            self._run_once(rule.id)

    def hadnle_once(self, args, options):
        params = options['params']
        if not params or len(params) <= 0:
            self.stdout.write(usage())
            return

        rule_id = params[0]
        self._run_once(rule_id)

