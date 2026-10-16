# Programska oprema pri pouku

To je repozitorij z gradivom za tematiko racionalnih funkcij v obliki LaTeX izvornih datotek.

## Vsebina

- Pregled snovi: [Pregled snovi/Pregled-snovi-matematika-racionalne-funkcije.tex](Pregled%20snovi/Pregled-snovi-matematika-racionalne-funkcije.tex)
- Preizkus: [Preizkus/Preizkus-racionalne-funkcije.tex](Preizkus/Preizkus-racionalne-funkcije.tex)
- Rešitve: [Rešitve/Resitve-preizkusa-racionalne-funkcije.tex](Rešitve/Resitve-preizkusa-racionalne-funkcije.tex)
- Handoff: [HANDOFF.md](HANDOFF.md)

## Namen projekta

Repozitorij vsebuje učne in preverjalne materiale za temo racionalnih funkcij:

- kratek pregled snovi,
- preizkus znanja,
- rešitve preizkusa.

Vse datoteke so napisane v LaTeX in so namenjene za kasnejšo izdelavo PDF dokumentov.

## Izdelava PDF

Za lokalno izdelavo PDF datotek uporabite `latexmk` iz ustreznega direktorija:

```bash
cd "Programska-oprema-pri-pouku/Pregled snovi"
latexmk -pdf -interaction=nonstopmode -halt-on-error "Pregled-snovi-matematika-racionalne-funkcije.tex"
```

Alternativno lahko za samodejno osveževanje v realnem času uporabite:

```bash
cd "Programska-oprema-pri-pouku/Pregled snovi"
latexmk -pdf -pvc -interaction=nonstopmode -halt-on-error "Pregled-snovi-matematika-racionalne-funkcije.tex"
```

## Pravila o artefaktih

Repozitorij naj vsebuje izključno izvorne datoteke (.tex). Generirani artefakti, kot so PDF, AUX, LOG, FLS, FDB_LaTeXMK in podobni, so lokalni gradbeni izdelki in ne predstavljajo izvorne vsebine projekta.

Pred objavo ali shranjevanjem sprememb je priporočljivo odstraniti ali ignorirati take datoteke, da ostane repozitorij čist in pregledno urejen.
