from requests_html import HTMLSession
import urllib
from diskcache import Cache


class URLhaus:
    """Simple client to query URLhaus by abuse.ch.
    :param query: domain, url or hash.
    :param cache_duration: Duration before refreshing the cache (in seconds).
                           Ignored if `cache_duration` is 0.
    :param cache_root: Path where to store the cached file.
    :type query: string
    :type cache_duration: int
    :type cache_root: str
    """
    def __init__(self,
                 query,
                 cache_duration=3600,
                 cache_root="/tmp/cortex/URLhaus"):
        self.URL = "https://urlhaus.abuse.ch/browse.php"
        self.query = query
        self.cache = None
        if cache_duration > 0:
            self.cache = Cache(cache_root)
            self.cache_duration = cache_duration

    __cache_key = __name__ + ':raw_data'

    def _get_raw_data(self):
        try:
            return self.cache['raw_data']
        except(AttributeError, TypeError):
            return self.fetch()
        except KeyError:
            self.cache.set(
                'raw_data',
                self.fetch(),
                expire=self.cache_duration)
            return self.cache['raw_data']

    def search(self):
        res = self._get_raw_data()
        return self.parse(res)

    def fetch(self):
        session = HTMLSession()
        return session.get(self.target_url())

    def parse(self, res):
        results = []
        table = res.html.find("table.table", first=True)
        rows = table.find("tr")[1:]
        for row in rows:
            cols = row.find("td")
            results.append({
                "dateadded": cols[0].text,
                "malware_url": cols[1].text,
                "link": cols[1].find("a", first=True).attrs.get("href"),
                "status": cols[2].text,
                "tags": cols[3].text.split(),
                "gsb": cols[4].text,
                "reporter": cols[5].text
            })
        return results

    def target_url(self):
        return "{}?{}".format(
            self.URL,
            urllib.parse.urlencode({"search": self.query})
        )
