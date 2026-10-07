# Handoff – Programska oprema pri pouku

## Namen projekta

Repozitorij vsebuje gradivo in izdelke za predmet Programska oprema pri pouku na FMF UL (študijsko leto 2026/27). Trenutno delo je osredotočeno na izdelke za gimnazijsko matematiko, posebej racionalne funkcije.

## Struktura in ključne datoteke

- `README.md` – uvodni opis in kazalo povezav do izdelkov.
- `Pregled-snovi-matematika-racionalne-funkcije.md` – dijakom namenjen povzetek definicij, postopkov, grafov, asimptot, enačb, neenačb in uporabe racionalnih funkcij.
- `Preizkus-racionalne-funkcije.md` – 60-minutni preizkus, 6 nalog in 40 točk.
- `Resitve-preizkusa-racionalne-funkcije.md` – rešitve in točkovnik; dokument izrecno opozarja, da preizkus še ni bil preverjen z dejanskim sošolcem oziroma sošolko.
- `Učni načrt matematika.pdf` – uporabljeni vir za racionalne funkcije (poglavje »Racionalna funkcija«, str. 83). PDF je trenutno v korenu repozitorija kot nepripravljen Git dodatek.

## Pomembna vsebinska izhodišča

Pri racionalnih funkcijah je treba ohraniti izločene vrednosti tudi po krajšanju, razlikovati ničle, pole in luknje ter pri enačbah in neenačbah preverjati pogoje. Pregled sledi ciljem učnega načrta: analiza in skiciranje grafov, vodoravne in poševne asimptote, racionalne enačbe in neenačbe, presečišča grafov ter matematično in življenjsko modeliranje.

## Trenutno stanje in naslednji koraki

- Pregled racionalnih funkcij je zamenjal prejšnji splošni pregled; kazalo v README-ju je posodobljeno.
- Preizkus in rešitve so bili prej oddani v commitu `c7d5fce`; od takrat sta bila pregled in README dodatno spremenjena.
- Delovna kopija ima neoddane spremembe. Pred commitom preveri `git status` in `git diff` ter potrdi preimenovanje/odstranitev stare datoteke `Pregled-snovi-matematika.md`.
- Dejanskega preizkusa na sošolcu še ni bilo. Za popolno izpolnitev te zahteve naj sošolec reši preizkus v 60 minutah, zabeleži nejasna navodila in porabo časa; nato ustrezno posodobi preizkus in zapis v rešitvah.
- PDF dodaj v Git samo, če je vključitev izvornega gradiva v repozitorij namerna in dovoljena; sicer ga pusti zunaj commita.

## Preverjanje

Markdown datoteke so bile preverjene v urejevalniku. Za matematične spremembe ponovno preveri pogoje in računske rezultate, povezave v README-ju pa naj kažejo na obstoječe datoteke.
