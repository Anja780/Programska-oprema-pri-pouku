cd manim-demo
uv run manim -pqh vsota_kotov.py VsotaKotov





# Videoposnetek: Vsota notranjih kotov

Animacija je dolga 60 sekund in je pripravljena za format TikTok/Instagram: pokončno razmerje 9:16, ločljivost 1080 × 1920 in 30 sličic na sekundo.

## Tema

Vsota notranjih kotov v trikotniku in splošno pravilo za večkotnike:

- trikotnik: $\alpha + \beta + \gamma = 180^\circ$
- večkotnik: $S = (n - 2) \cdot 180^\circ$

## Potek videa

1. Uvodno vprašanje o vsoti kotov poljubnega trikotnika.
2. Skozi vrh trikotnika narišemo vzporednico z nasprotno stranico.
3. Z enakostjo izmeničnih kotov prenesemo kota $\alpha$ in $\gamma$ na vzporednico.
4. Ker koti $\alpha$, $\beta$ in $\gamma$ ležijo na premici, je njihova vsota $180^\circ$.
5. Petkotnik razdelimo na tri trikotnike in izračunamo $3 \cdot 180^\circ = 540^\circ$.
6. Iz vzorca za trikotnik, štirikotnik, petkotnik in šestkotnik izpeljemo pravilo $S=(n-2)\cdot180^\circ$.

Vizualna zasnova se zgleduje po osnovnih barvah Univerze v Ljubljani: rdeči, sivih odtenkih in eni sekundarni modri. Ker pisava Univerza Sans ni na voljo, je uporabljena Arial.

Opis snemalne knjige je v datoteki [storyboard.md](storyboard.md).

## Zagon

```bash
cd "/Users/anjakozlevcar/Documents/POP/Programska-oprema-pri-pouku/manim-demo"
uv run manim -pqh vsota_kotov.py VsotaKotov
```

## Rezultat

Končni posnetek: [media/videos/vsota_kotov/1920p30/VsotaKotov.mp4](media/videos/vsota_kotov/1920p30/VsotaKotov.mp4)
