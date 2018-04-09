# -*- coding: utf-8 -*-

import pylast

API_KEY = 'af8203a63267d6e7d73f184cfcfef060'
API_SECRET = '65261b78d4f3c3452eb6bb8573ede975'

username = "Parth_M"
password_hash = pylast.md5("0G&vr6fAX")

network = pylast.LastFMNetwork(api_key = API_KEY)

class CustomUser(pylast.User):
    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)

    def _get_things(
        self, method, thing, thing_type, params=None, cacheable=True
    ):
        """Returns a list of the most played thing_types by this thing."""

        from pylast import TopItem, _extract, _number
        doc = self._request(
            self.ws_prefix + "." + method, cacheable, params)

        toptracks_node = doc.getElementsByTagName('toptracks')[0]
        total_pages = int(toptracks_node.getAttribute('totalPages'))

        seq = []
        for node in doc.getElementsByTagName(thing):
            title = _extract(node, "name")
            artist = _extract(node, "name", 1)
            mbid = _extract(node, "mbid")
            playcount = _number(_extract(node, "playcount"))

            thing = thing_type(artist, title, self.network)
            thing.mbid = mbid
            seq.append(TopItem(thing, playcount))

        return seq, total_pages

    def get_top_tracks(
            self, period=pylast.PERIOD_3MONTHS, limit=1, page=1, cacheable=True):
        """Returns the top tracks played by a user.
        * period: The period of time. Possible values:
          o PERIOD_OVERALL
          o PERIOD_7DAYS
          o PERIOD_1MONTH
          o PERIOD_3MONTHS
          o PERIOD_6MONTHS
          o PERIOD_12MONTHS
        """

        params = self._get_params()
        params['period'] = period
        params['page'] = page
        if limit:
            params['limit'] = limit

        return self._get_things(
            "getTopTracks", "track", pylast.Track, params, cacheable)

my_user = CustomUser('Parth_M', network)
params = my_user._get_params()
params['period'] = pylast.PERIOD_3MONTHS
params['limit'] = 1


page = 1
results,total_pages = my_user.get_top_tracks(page=page)
print (total_pages)
file = open("output.txt","w")
while len(results) != 0:
    for track in results:

        #lean = str(track.item.title + " - " + track.item.artist + track.weight)
        print (track.item.title, track.item.artist, track.weight)
        file.write(track.item.title + " - " + str(track.item.artist) + '\n')
    page += 1
    if(page == 31):
        file.close()
        break
    results,total_pages = my_user.get_top_tracks(page=page)
