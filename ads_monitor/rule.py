import json
import pprint

def parse(jsonstr):
    r = Rule()
    return r.parse(jsonstr)


class ConditionElement:
    def __init__(self, jsonobj, key):
        self.key = key
        self.condition_root = _parse_condition(jsonobj)

    def __repr__(self):
        return pprint.pformat({
                'key': self.key,
                'condition': repr(self.condition_root)
            })

    def execute(self, data):
        if self.key in data:
            return self.condition_root.execute(data[self.key])
        else:
            return False


class ConditionElementAnd:
    def __init__(self, jsonarray):
        self.op = 'and'
        self.condition_root_array = []
        for obj in jsonarray:
            self.condition_root_array.append(_parse_condition(obj))

    def __repr__(self):
        return pprint.pformat({
                'op': self.op,
                'condition_array': self.condition_root_array
            })

    def execute(self, data):
        if len(self.condition_root_array) <= 0:
            return True
        else:
            return all([condition_root.execute(data) \
                    for condition_root in self.condition_root_array])


class ConditionElementOr:
    def __init__(self, jsonarray):
        self.op = 'or'
        self.condition_root_array = []
        for obj in jsonarray:
            self.condition_root_array.append(_parse_condition(obj))

    def __repr__(self):
        return pprint.pformat({
                'op': self.op,
                'condition_array': self.condition_root_array
            })

    def execute(self, data):
        if len(self.condition_root_array) <= 0:
            return True
        else:
            return any([condition_root.execute(data) \
                    for condition_root in self.condition_root_array])


class ConditionElementLT:
    def __init__(self, value):
        self.op = '<'
        self.compare_to_value = value

    def __repr__(self):
        return pprint.pformat({
                'op': self.op,
                'compare_to_value': self.compare_to_value
            })

    def execute(self, data):
        return data < self.compare_to_value

class ConditionElementGT:
    def __init__(self, value):
        self.op = '>'
        self.compare_to_value = value

    def __repr__(self):
        return pprint.pformat({
                'op': self.op,
                'compare_to_value': self.compare_to_value
            })

    def execute(self, data):
        return data > self.compare_to_value


class ConditionElementLEQ:
    def __init__(self, value):
        self.op = '<='
        self.compare_to_value = value

    def __repr__(self):
        return pprint.pformat({
                'op': self.op,
                'compare_to_value': self.compare_to_value
            })

    def execute(self, data):
        return data <= self.compare_to_value


class ConditionElementGEQ:
    def __init__(self, value):
        self.op = '>='
        self.compare_to_value = value

    def __repr__(self):
        return pprint.pformat({
                'op': self.op,
                'compare_to_value': self.compare_to_value
            })

    def execute(self, data):
        return data >= self.compare_to_value


class ConditionElementEQ:
    def __init__(self, value):
        self.op = '='
        self.compare_to_value = value

    def __repr__(self):
        return pprint.pformat({
                'op': self.op,
                'compare_to_value': self.compare_to_value
            })

    def execute(self, data):
        return data == self.compare_to_value


_condition_class_map = {
    'and': ConditionElementAnd,
    'or': ConditionElementOr,
    '<': ConditionElementLT,
    '>': ConditionElementGT,
    '<=': ConditionElementLEQ,
    '>=': ConditionElementGEQ,
    '=': ConditionElementEQ
}


def _parse_condition(jsonobj):
    key = jsonobj.keys()[0]
    if key in _condition_class_map:
        return _condition_class_map[key](jsonobj[key])
    else:
        return ConditionElement(jsonobj[key], key)


class DataProviderPast2Days:
    def scan(self, datarray):
        for d in datarray:
            formated_data = {
                'id': d[0],
                'cost': d[7],
                'install': d[8],
                'CPI': d[9]
            }
            yield formated_data


class DataProviderPast7Days:
    def scan(self, datarray):
        for d in datarray:
            formated_data = {
                'id': d[0],
                'cost': d[10],
                'install': d[11],
                'CPI': d[12]
            }
            yield formated_data


_data_provider_class_map = {
    'past2days': DataProviderPast2Days,
    'past7days': DataProviderPast7Days
}


def _parse_data_provider(typestr):
    return _data_provider_class_map[typestr]()


class Rule:
    def __init__(self):
        self.orig_json = None
        self.data_provider = None
        self.condition_root = None

    def parse(self, jsonstr):
        self.orig_json = json.loads(jsonstr)
        self.data_provider = _parse_data_provider(self.orig_json['data'])
        self.condition_root = _parse_condition(self.orig_json['condition'])
        return self

    def execute(self, data):
        return [(d['id'], self.condition_root.execute(d)) \
                for d in self.data_provider.scan(data)]


def get_rule_examples():
    rule1json = """
{
    "data": "past2days",
    "condition": {
        "and": [
            { "cost": { ">": 20 } },
            { "install": { "=": 0 }}
        ]
    }
}
"""

    rule2json = """
{
    "data": "past7days",
    "condition": {
        "and": [
            { "cost": { ">": 100 } },
            { "CPI": { ">": 5 } }
        ]
    }
}
"""
    return ['rule example 1:', rule1json, 'rule example 2:', rule2json]


if __name__ == '__main__':
    rule1json = """
{
    "data": "past2days",
    "condition": {
        "and": [
            { "cost": { ">": 20 } },
            { "install": { "=": 0 }}
        ]
    }
}
"""

    rule2json = """
{
    "data": "past7days",
    "condition": {
        "and": [
            { "cost": { ">": 100 } },
            { "CPI": { ">": 5 } }
        ]
    }
}
"""

    data = [
        # id, campaign_name, campaign_id, adset_name, adset_id, ad_name, ad_id, past2days_cost, past2days_install, past2days_CPI, past7days_cost, past7days_install, past7days_CPI
        # 0,  1,             2,           3,          4,        5,       6,     7,              8,                 9,             10,             11,                12
        [1, 'Facebook_New York_IOS_English_Buyer', 1012345678, 'Men_16-64', 1112345678, 'mpa118-3', 1212345678, 21, 0, None, 13, 0, None],
        [2, 'Facebook_New York_IOS_English_Buyer', 1012345679, 'Women_16-64', 111234569, 'Motocycle-3', 1212345679, 13, 0, 6.5, 160, 30, 5.33]
    ]

    r1 = parse(rule1json)
    pprint.pprint(vars(r1))
    result = r1.execute(data)
    print result

    r2 = parse(rule2json)
    pprint.pprint(vars(r2))
    result = r2.execute(data)
    print result
