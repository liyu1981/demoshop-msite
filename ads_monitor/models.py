from django.db import models


from django.db import models
from django.db.models.fields.related import ManyToManyField

class PrintableModel(models.Model):
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(
                        f.value_from_object(self).values_list('pk', flat=True)
                    )
            else:
                data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        abstract = True


class Rule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    rule_json = models.CharField(max_length=1024*1024)


class AdInsightSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    instruction_json = models.CharField(max_length=1024*1024)


class AdInsight(PrintableModel):
    id = models.AutoField(primary_key=True)
    retrieve_time = models.DateTimeField()
    campaign_name = models.CharField(max_length=1024)
    campaign_id = models.IntegerField()
    adset_name = models.CharField(max_length=1024)
    adset_id = models.IntegerField()
    ad_name = models.CharField(max_length=1024)
    ad_id = models.IntegerField()
    past_2d_cost = models.FloatField()
    past_2d_install = models.FloatField()
    past_2d_CPI = models.FloatField()
    past_7d_cost = models.FloatField()
    past_7d_install = models.FloatField()
    past_7d_CPI = models.FloatField()


class RuleExecutionResult(PrintableModel):
    rule = models.ForeignKey(Rule)
    adinsight = models.ForeignKey(AdInsight)
    result = models.BooleanField(default=True)
    execution_time = models.DateTimeField()


