# Handoff

Repozitorij vsebuje izvorna gradiva za tematiko racionalnih funkcij v obliki LaTeX dokumentov.

## Datoteke

- [Pregled snovi/Pregled-snovi-matematika-racionalne-funkcije.tex](Pregled%20snovi/Pregled-snovi-matematika-racionalne-funkcije.tex)
- [Preizkus/Preizkus-racionalne-funkcije.tex](Preizkus/Preizkus-racionalne-funkcije.tex)
- [Rešitve/Resitve-preizkusa-racionalne-funkcije.tex](Rešitve/Resitve-preizkusa-racionalne-funkcije.tex)

## Namen vsebine

Datoteke so namenjene poučevanju, preverjanju znanja in reševanju nalog s področja racionalnih funkcij.

- Pregled snovi: teoretični opis, definicije, primeri, asimptote in način skiciranja grafa.
- Preizkus: naloge za samostojno preverjanje znanja.
- Rešitve: razčlenjene rešitve in koraki do rezultata.

## Pravila repozitorija

- Repozitorij naj vsebuje izključno izvorne datoteke (.tex).
- Generirani artefakti, kot so PDF, AUX, LOG, FLS, FDB_LaTeXMK in podobni, so lokalni gradbeni izdelki in ne spadajo v verzioniranje.
- Če so v delovnem direktoriju prisotni, jih je treba odstraniti ali ignorirati pred objavo sprememb.

## Lokalna izdelava PDF

Za ustvarjanje PDF dokumenta uporabite `latexmk` v direktoriju z dokumentom:

```bash
cd "Programska-oprema-pri-pouku/Pregled snovi"
latexmk -pdf -interaction=nonstopmode -halt-on-error "Pregled-snovi-matematika-racionalne-funkcije.tex"
```

Možno je tudi spremljanje sprememb v realnem času:

```bash
cd "Programska-oprema-pri-pouku/Pregled snovi"
latexmk -pdf -pvc -interaction=nonstopmode -halt-on-error "Pregled-snovi-matematika-racionalne-funkcije.tex"
```

## Status

Projekt je pripravljeni izvorni material za uporabo in nadaljnje urejanje. Dokumenti so zasnovani tako, da jih je enostavno ponovno uporabljati, razširjati in prilagajati novim učnim ciljem.
