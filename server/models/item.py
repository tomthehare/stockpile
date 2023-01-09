from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %I:%M:%S %p'

class Item:

    def __init__(self, the_id):
        self.id = the_id
        self.description = ''
        self.location = ''
        self.tags = []
        self.created_ts = None
        self.last_update_ts = None

    def set_last_update_ts(self, ts):
        self.last_update_ts = ts

    def set_created_ts(self, ts):
        self.created_ts = ts

    def get_last_update_ts_formatted(self):
        if self.last_update_ts:
            return datetime.fromtimestamp(self.last_update_ts).strftime(DATE_FORMAT)

    def get_created_ts_formatted(self):
        if self.created_ts:
            return datetime.fromtimestamp(self.created_ts).strftime(DATE_FORMAT)

    def get_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'location': self.location,
            'created_ts': self.created_ts,
            'last_update_ts': self.last_update_ts
        }


