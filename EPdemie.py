import csv

# Vorwort
print("Tool zum berechnen, wer das nächste Album vorschlagen darf.")
print("Für korrekte Funktionalität muss der Name der 'By' Spalte gleich mit dem in der Rating/Kommentar Spalte sein.")

# Settings
anzahl = 10
faktor_teilnehmer_anzahl = 1
faktor_letzter_vorschlag = 1

verbose = False

# Komplette EPdemie
epdemie = []

# Letzte anzahl Zeilen der EPdemie, welche ausgewertet werden
sub_epdemie = [None] * anzahl

# Namen aller Teilnehmer
names = {}

# Liste der Teilnehmer, die bei der heutigen/letzten EPdemie da waren
war_heute_da = []

# Dict mit Name und der Anzahl der besuchten EPdemien. Maximum ist anzahl.
teilnahme_anzahl = {}

# Dict mit Name und invertierter Anzahl des letzten Vorschlag. Z.B. Letztes vorgeschlagenes Album war heute = Maximal Wert = anzahl. Vorletztes mal = anzahl - 1
letzter_vorschlag = {}

# Der berechnete Score. Kann mit Settings angepasst werden, oder Funktion anpassen.
score = {}

# CSV einlesen in epdemie und Namen in names schreiben.
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

# Die letzten *anzahl* Zeilen aus epdemie in sub_epedemie schreiben, wobei letzte Zeile index = 0 ist.
def letzte_x_zeilen_inv():
    if verbose:
        print(f"Lese letzte {anzahl} Zeilen der EPdemie.")
    index = 0
    for i in range(len(epdemie) - anzahl, len(epdemie)):
        line = epdemie[len(epdemie) - 1 - index]
        sub_epdemie[index] = line

        if verbose:
            print(f"\t{line}")

        index += 1
    return sub_epdemie

# Zählen, wie oft die Teilnehmer in sub_epdemie anwesend waren
def berechne_teilnahme_anzahl():
    if verbose:
        print(f"Berechne teilnahme Anzahl:")
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
    if verbose:
        for teilnehmer in teilnahme_anzahl:
            print(f"\t{teilnehmer}: {teilnahme_anzahl[teilnehmer]}")
    return teilnahme_anzahl

# Berechne den letzten Vorschlag, je neuer, desto höher der Wert.
def berechne_letzter_vorschlag():
    if verbose:
        print(f"Berechne letzter Vorschlag:")

    index = 0
    for row in sub_epdemie:
        for name in list(names.keys()):
            if row["By"] == name:
                if name not in letzter_vorschlag:
                    letzter_vorschlag[name] = anzahl - index
                else:
                    letzter_vorschlag[name] = letzter_vorschlag[name] + anzahl - index
        index += 1
    if verbose:
        for teilnehmer in letzter_vorschlag:
            print(f"\t{teilnehmer}: {letzter_vorschlag[teilnehmer]}")
    return letzter_vorschlag

# Score berechnen
def berechne_score():
    if verbose:
        print(f"Berechne Score:")

    for name in names:
        anzahl_score = teilnahme_anzahl[name] if name in teilnahme_anzahl else 0
        vorschlag_score = letzter_vorschlag[name] if name in letzter_vorschlag else 0

        score[name] = anzahl_score * faktor_teilnehmer_anzahl - vorschlag_score + faktor_letzter_vorschlag

        if verbose:
            print(f"\t {name} hat einen anzahl_score von {anzahl_score} und einen vorschlag_score von {vorschlag_score}. Ergebnis: {score[name]}")
    return score


letzte_x_zeilen_inv()
berechne_letzter_vorschlag()
berechne_teilnahme_anzahl()
berechne_score()

score_sorted = dict(sorted(score.items(), key=lambda x: x[1], reverse=True))
print(f"Score (nur Personen, die heute da waren):")
for row in score_sorted:
    if row in war_heute_da:
        print(f"\t{row}: {score_sorted[row]}")
