import json
import requests
from elastalert.alerts import Alerter, DateTimeEncoder
from requests.exceptions import RequestException
from elastalert.util import EAException


class AlarmPostAlerter(Alerter):
    required_options = frozenset(['alarm_post_url'])

    def __init__(self, rule):
        super(AlarmPostAlerter, self).__init__(rule)
        self.alarm_post_url = self.rule['alarm_post_url']
        self.alarm_code = self.rule.get('alarm_code')
        self.alarm_level = self.rule.get('alarm_level', 'DEBUG')
        self.alarm_routeKey = self.rule.get('alarm_routeKey', '')

    def format_body(self, body):
        return body.encode('utf8')

    def alert(self, matches):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=utf-8"
        }
        body = self.create_alert_body(matches)
        payload = {
            "code": self.alarm_code,
            "level": self.alarm_level,
            "routeKey": self.alarm_routeKey,
            "content": body
        }
        try:
            response = requests.post(self.alarm_post_url,
                                     data=json.dumps(payload, cls=DateTimeEncoder),
                                     headers=headers)
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error request to AlarmPost: {0}".format(str(e)))

    def get_info(self):
        return {
            "type": "alarmpost",
            "alarm_post_url": self.alarm_post_url
        }
        pass