# # TODO: Implement your data models here
# # Consider what data structures you'll need for:
# # - Storing URL mappings
# # - Tracking click counts
# # - Managing URL metadata


from threading import Lock
from datetime import datetime

class URLStore:
    def __init__(self):
        self._urls = {}
        self._lock = Lock()
    
    def add_url(self, short_code, long_url):
        with self._lock:
            if short_code in self._urls:
                return False
            self._urls[short_code] = {
                'url': long_url,
                'clicks': 0,
                'created_at': datetime.utcnow()
            }
            return True
    
    def get_url(self, short_code):
        with self._lock:
            return self._urls.get(short_code)
    
    def increment_clicks(self, short_code):
        with self._lock:
            if short_code in self._urls:
                self._urls[short_code]['clicks'] += 1