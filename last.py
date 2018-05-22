# -*- coding: utf-8 -*-

import pylast

API_KEY = 'af8203a63267d6e7d73f184cfcfef060'
API_SECRET = '65261b78d4f3c3452eb6bb8573ede975'

username = "Parth_M"
password_hash = pylast.md5("0G&vr6fAX")

network = pylast.LastFMNetwork(api_key = API_KEY)

per = pylast.PERIOD_OVERALL

class CustomUser(pylast.User):
    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)
    def input():
        while True:
            num = int(input("Possible values: \n1. PERIOD_OVERALL \n2. PERIOD_7DAYS \n3. PERIOD_1MONTH  \n4. PERIOD_3MONTHS \n5. PERIOD_6MONTHS \n6. PERIOD_12MONTHS\n"))
            if 1 <= num <= 6:
                global per
                print ('Value selected')
                if num == 1:
                    per = pylast.PERIOD_OVERALL
                    print ('All')
                    #break
                if num == 2:
                    per = pylast.PERIOD_7DAYS
                    print ('7 days')
                    #break
                if num == 3:
                    per = pylast.PERIOD_1MONTH
                    print ('1 month')
                    #break
                if num == 4:
                    per = pylast.PERIOD_3MONTHS
                    print ('3 months')
                    #break
                if num == 5:
                    per = pylast.PERIOD_6MONTHS
                    print ('6 months')
                    #break
                if num == 6:
                    per = pylast.PERIOD_12MONTHS
                    print ('12 months')
                    #break

                break
        else:
            print ('number out of range')



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

        #print("Possible values: \no PERIOD_OVERALL \no PERIOD_7DAYS \no PERIOD_1MONTH  \no PERIOD_3MONTHS o PERIOD_6MONTHS \no PERIOD_12MONTHS")
        #type(per)


    input()
    def get_top_tracks(
            self, period=per, limit=1, page=1, cacheable=True):
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
params['period'] = pylast.PERIOD_1MONTH
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
