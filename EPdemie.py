import csv

anzahl = 10

epdemie = []
sub_epdemie = [None] * anzahl
names = {}

war_heute_da = []

faktor_teilnehmer_anzahl = 1
teilnahme_anzahl = {}

faktor_letzter_vorschlag = 1
letzter_vorschlag = {}

score = {}

with open('epdemie.csv', mode='r', encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        epdemie.append(row)
        if line_count == 0:
             keys = list(row.keys())
             for i in range(0, len(keys)):
                 line = keys[i]
                 if line.startswith('Rating '):
                     name = line[7:len(line)]
                     names[name] = i
        line_count += 1



def letzte_x_zeilen_inv():
    index = 0

    for i in range(len(epdemie) - anzahl, len(epdemie)):
        line = epdemie[len(epdemie) - 1 - index]
        sub_epdemie[index] = line

        index += 1

def berechne_teilnahme_anzahl():
    index = 0
    for row in sub_epdemie:
        for name in list(names.keys()):
            if row["Rating " + name] != "":
                if index == 0:
                    war_heute_da.append(name)


                if name not in teilnahme_anzahl:
                    teilnahme_anzahl[name] = 1
                else:
                    teilnahme_anzahl[name] = teilnahme_anzahl[name] + 1


        index += 1

def berechne_letzter_vorschlag():
    index = 0
    for row in sub_epdemie:
        for name in list(names.keys()):
            if row["By"] == name:
                if name not in letzter_vorschlag:
                    letzter_vorschlag[name] = anzahl - index
        index += 1

def berechne_score():
    for name in names:
        anzahl_score = teilnahme_anzahl[name] if name in teilnahme_anzahl else 0
        vorschlag_sore = letzter_vorschlag[name] if name in letzter_vorschlag else 0

        score[name] = anzahl_score * faktor_teilnehmer_anzahl - vorschlag_sore + faktor_letzter_vorschlag





letzte_x_zeilen_inv()
berechne_letzter_vorschlag()
berechne_teilnahme_anzahl()
berechne_score()

score_sorted = dict(sorted(score.items(), key=lambda x: x[1], reverse=True))
for row in score_sorted:
    if row in war_heute_da:
        print(f'{row}: {score_sorted[row]}')


