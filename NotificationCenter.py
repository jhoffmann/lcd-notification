import subprocess
import urllib2, json
from datetime import datetime
import psutil
import transmissionrpc

class NotificationCenter:
    TEMP_SYS     = '/sys/class/thermal/thermal_zone0/temp'
    DATE_FMT     = '%a %b %d %H:%M'
    TORRENT_HOST = 'localhost'
    TORRENT_PORT = 9091
    TORRENT_USER = 'pi'
    TORRENT_PASS = 'pi'
    WEATHER_CITY = 'Kanata'
    DISK_FS      = ['/', '/media']

    def _splitCount(self, s, count):
         return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]

    def _fetchJson(self, url):
        """ Load a JSON result from the given URL """
        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
        except Exception:
            return {}
        return response.read()

    def status_date(self):
        """ Display the date, memory usage, and CPU temperature """
        mem = psutil.virtual_memory()

        try:
            cpu_temp = float([line.strip() for line in open(self.TEMP_SYS)][0]) / 1000
        except Exception:
            cpu_temp = 0.0

        return [datetime.now().strftime(self.DATE_FMT),
            'Mem: %4.1f%% %4.1f%c' % (mem.percent, cpu_temp, 223)]

    def status_torrents(self):
        """ Ping transmission-daemon over RPC and get an update """
        try:
            tc = transmissionrpc.Client(self.TORRENT_HOST,
                port=self.TORRENT_PORT, user=self.TORRENT_USER,
                password=self.TORRENT_PASS)
            stats  = tc.session_stats()
            down   = float(stats.downloadSpeed) / 1000
            up     = float(stats.uploadSpeed)   / 1000
            """ Show an infinity, or a turtle if alt speed enabled """
            turtle = 244 if stats.alt_speed_enabled else 243

            return ['Active: %2d (%3d)' % (stats.activeTorrentCount, stats.torrentCount),
                '%c %5dKB %4dKB' % (turtle, down, up)]
        except:
            return ['{:^16}'.format("UNABLE TO LOAD"),
                '{:^16}'.format("TORRENT DATA")]

    def status_weather(self):
        """ Grab the current, high, and low temperatures """
        url = 'http://api.openweathermap.org/data/2.5/weather?cnt=1&q=' + self.WEATHER_CITY

        try:
            data = json.loads(self._fetchJson(url))

            status    = data['weather'][0]['main'].encode('utf-8')
            desc      = data['weather'][0]['description'].encode('utf-8')
            """ Convert the temperatures from Kelvin to Celcius """
            tmp_curr  = data['main']['temp'] - 273.15

            return ['%-11s %3d%c' % (status[:11], tmp_curr, 223),
                '%-16s' % (desc[:16])]
        except Exception:
            return ['{:^16}'.format('UNABLE TO LOAD'),
                '{:^16}'.format('WEATHER')]

    def status_disk(self):
        """ Displays disk usage """
        try:
            resp = []
            for disk in self.DISK_FS:
                df = subprocess.Popen(['df', disk],
                    stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                output = df.communicate()[0]
                device, size, used, available, percent, mountpoint = \
                    output.split('\n')[1].split()
                resp.append('%-12s %3s' % (disk[:12], percent))
            return resp
        except Exception:
            return ['{:^16}'.format('UNABLE TO LOAD'),
                '{:^16}'.format('DISK USAGE')]

    def startup(self):
        return ['{:^16}'.format('MAIN SYSTEM'),
            '{:^16}'.format('TURN ON')]

    def fun1(self):
        return ['{:^16}'.format('WEAPONS'),
            '{:^16}'.format('ACTIVATED')]

    def random_quotes(self):
        """ Random quotes """
        try:
            p = subprocess.Popen(['/usr/games/fortune', '-s', '-n', '32'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = p.communicate()[0].replace('\n', '')
            return self._splitCount('%-32s' % output, 16)
        except Exception:
            return []

if __name__ == '__main__':
    nc = NotificationCenter()
    print '\n'.join(nc.random_quotes())
    print '----------------'
    print '\n'.join(nc.status_date())
    print '----------------'
    print '\n'.join(nc.status_torrents())
    print '----------------'
    print '\n'.join(nc.status_weather())
    print '----------------'
    print '\n'.join(nc.status_disk())
    print '----------------'
