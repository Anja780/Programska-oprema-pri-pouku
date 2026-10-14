# Handoff – Programska oprema pri pouku

## Namen projekta

Repozitorij vsebuje gradivo in izdelke za predmet Programska oprema pri pouku na FMF UL (študijsko leto 2026/27). Trenutno delo je osredotočeno na izdelke za gimnazijsko matematiko, posebej racionalne funkcije.

## Struktura in ključne datoteke

- `README.md` – uvodni opis in kazalo povezav do izvornih datotek.
- `Pregled snovi/Pregled-snovi-matematika-racionalne-funkcije.tex` – izvorna datoteka s povzetkom definicij, postopkov, grafov, asimptot, enačb, neenačb in uporabe racionalnih funkcij.
- `Preizkus/Preizkus-racionalne-funkcije.tex` – 60-minutni preizkus, 6 nalog in 40 točk.
- `Rešitve/Resitve-preizkusa-racionalne-funkcije.tex` – rešitve in točkovnik; dokument izrecno opozarja, da preizkus še ni bil preverjen z dejanskim sošolcem oziroma sošolko.
- `HANDOFF.md` – dokument z opisom projekta, strukture in pomembnih smernic.

PDF izhodi so generirani lokalno z LaTeX orodjem in niso del repozitorija, ker repo vsebuje samo izvorno kodo.

## Pomembna vsebinska izhodišča

Pri racionalnih funkcijah je treba ohraniti izločene vrednosti tudi po krajšanju, razlikovati ničle, pole in luknje ter pri enačbah in neenačbah preverjati pogoje. Pregled sledi ciljem učnega načrta: analiza in skiciranje grafov, vodoravne in poševne asimptote, racionalne enačbe in neenačbe, presečišča grafov ter matematično in življenjsko modeliranje.

## Trenutno stanje in naslednji koraki

- Pregled racionalnih funkcij je zamenjal prejšnji splošni pregled; kazalo v README-ju je posodobljeno.
- Preizkus in rešitve so v izvorni LaTeX obliki, PDF izhodi pa se ustvarjajo lokalno ob gradnji dokumenta.
- Repozitorij je namenjen samo izvorni kodi, zato so generirani artefakti (`.pdf`, `.log`, `.aux`, `.fdb_latexmk`, `.fls`, itd.) izključeni iz Git s `.gitignore`.
- Dejanskega preizkusa na sošolcu še ni bilo. Za popolno izpolnitev te zahteve naj sošolec reši preizkus v 60 minutah, zabeleži nejasna navodila in porabo časa; nato ustrezno posodobi preizkus in zapis v rešitvah.
- Če želiš zagotoviti pregledno distribucijo, lahko dodajaš tudi lokalno generirane PDF datoteke, vendar ne v glavnem repozitoriju, ko je cilj samo izvorna koda.

## Preverjanje

Markdown datoteke so bile preverjene v urejevalniku. Za matematične spremembe ponovno preveri pogoje in računske rezultate, povezave v README-ju pa naj kažejo na obstoječe datoteke.
