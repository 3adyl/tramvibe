from datetime import datetime, timedelta

import requests
from dotenv import dotenv_values

config = dotenv_values(".env")


class Przystanek:

    def __init__(self, nazwa_i_numer, dane_przystankow):
        self.przystanek_nazwa, self.przystanek_numer = nazwa_i_numer.rsplit(sep=' ', maxsplit=1)
        for i in dane_przystankow.json()['result']:
            if i['values'][2]['value'] == self.przystanek_nazwa and i['values'][1]['value'] == self.przystanek_numer:
                self.values = i
        self.zespol = self.values['values'][0]['value']
        self.slupek = self.values['values'][1]['value']
        self.nazwa_zespolu = self.values['values'][2]['value']
        self.id_ulicy = self.values['values'][3]['value']
        self.szer_geo = self.values['values'][4]['value']
        self.dlug_geo = self.values['values'][5]['value']

    def dystans(self, szer, dlug):
        return round(
            (round((float(self.szer_geo) - szer), 6) ** 2 + (round((float(self.dlug_geo) - dlug), 6) ** 2)) ** (1 / 2),
            6)

    def rozklad_full(self, **kwargs):
        dostepne_linie = requests.get(
            f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId={self.zespol}&busstopNr={self.slupek}&apikey={config['API_KEY']}")
        z = []
        for i in dostepne_linie.json()['result']:
            dane_rozkladu = requests.get(
                f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId={self.zespol}&busstopNr={self.slupek}&line={i['values'][0]['value']}&apikey={config['API_KEY']}")
            z = z + dane_rozkladu.json()['result']
        return sorted(z, key=lambda x: x[5]['value'])

    def rozklad_wyswietlacz(self):
        dostepne_linie = requests.get(
            f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId={self.zespol}&busstopNr={self.slupek}&apikey={config['API_KEY']}")
        z = []
        for i in dostepne_linie.json()['result']:
            dane_rozkladu = requests.get(
                f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId={self.zespol}&busstopNr={self.slupek}&line={i['values'][0]['value']}&apikey={config['API_KEY']}")
            for j in dane_rozkladu.json()['result']:
                z.append([i['values'][0]['value'], j[3]['value'], j[5]['value']])
        z = sorted(z, key=lambda x: x[2])
        for i in z:
            godziny, minuty, sekundy = i[2].split(':')
            if int(godziny) >= 24:
                i[2] = f"{str(datetime.now().date() + timedelta(days=1))} {int(godziny) % 24:02d}:{minuty}:{sekundy}"
            else:
                i[2] = f"{str(datetime.now().date())} {i[2]}"
        z = [i for i in z if datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S') >= datetime.now()]
        z.append(['', 'KONIEC KURSOWANIA', ''])
        return z

    def rozklad_wyswietlacz_now(self):
        dostepne_linie = requests.get(
            f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId={self.zespol}&busstopNr={self.slupek}&apikey={config['API_KEY']}")
        z = []
        for i in dostepne_linie.json()['result']:
            dane_rozkladu = requests.get(
                f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId={self.zespol}&busstopNr={self.slupek}&line={i['values'][0]['value']}&apikey={config['API_KEY']}")
            for j in dane_rozkladu.json()['result']:
                z.append([i['values'][0]['value'], j[3]['value'], j[5]['value']])
        z = sorted(z, key=lambda x: x[2])
        for i in z:
            godziny, minuty, sekundy = i[2].split(':')
            if int(godziny) >= 24:
                i[2] = f"{str(datetime.now().date() + timedelta(days=1))} {int(godziny) % 24:02d}:{minuty}:{sekundy}"
            else:
                i[2] = f"{str(datetime.now().date())} {i[2]}"
        z = [i for i in z if datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S') >= datetime.now()]
        for i in z:
            a = int(round(-(datetime.now() - datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S')).total_seconds() / 60,0))
            if a ==0:
                i[2] = '<1 min'
            else:
                i[2] = str(a) + " min"
        z.append(['', 'KONIEC KURSOWANIA', ''])
        return z

# pr = 'Plac Politechniki 02'
# r = requests.get(f"https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey={config['API_KEY']}")
# szukany = Przystanek(pr, r)
# print(szukany.przystanek_nazwa)
# print(szukany.przystanek_numer)

# pr = 'Metro Kondratowicza 01'
# r = requests.get(f"https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey={config['API_KEY']}")
# szukany = Przystanek(pr, r)
# print(szukany.rozklad_wyswietlacz())

# print(float(szukany.dlug_geo))
# print(float(szukany.szer_geo))
# print(szukany.dystans(52.13,21.00))
