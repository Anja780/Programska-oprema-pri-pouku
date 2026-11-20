"""Sintetizirani zvočni učinki za video (brez tujih posnetkov, zato brez avtorskih omejitev).

Vsak zvok se ustvari z numpy in shrani kot 16-bitni mono WAV v mapo ``zvoki/``.
Datoteke se ustvarijo ob prvi uporabi; ob spremembi parametrov nastane nova datoteka.
"""

from pathlib import Path
import wave

import numpy as np

SR = 44100
MAPA = Path(__file__).parent / "zvoki"

# Durova pentatonika od C5 navzgor: veseli, »igrivi« toni, ki se nikoli ne tepejo med sabo.
PENTATONIKA = [523.25, 587.33, 659.26, 783.99, 880.00]


def ton(stopnja):
    """Frekvenca stopnje durove pentatonike (0 = C5, 5 = C6, ...)."""
    oktava, indeks = divmod(stopnja, len(PENTATONIKA))
    return PENTATONIKA[indeks] * 2 ** oktava


def _cas(trajanje):
    return np.arange(int(SR * trajanje)) / SR


def _shrani(pot, signal, vrh):
    signal = np.asarray(signal, dtype=float)
    najvecji = np.max(np.abs(signal)) or 1.0
    signal = signal / najvecji * vrh
    # Kratek izhod brez klika na koncu.
    izhod = min(len(signal), int(0.005 * SR))
    if izhod:
        signal[-izhod:] *= np.linspace(1, 0, izhod)
    pot.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(pot), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((signal * 32767).astype(np.int16).tobytes())


def _napad(t, trajanje=0.003):
    return np.clip(t / trajanje, 0, 1)


def _nizkoprepustni(signal, rezi):
    """Enopolni nizkoprepustni filter s (po potrebi časovno spremenljivo) mejno frekvenco."""
    rezi = np.broadcast_to(np.asarray(rezi, dtype=float), signal.shape)
    a = 1 - np.exp(-2 * np.pi * rezi / SR)
    izhod = np.empty_like(signal)
    y = 0.0
    for i, (x, k) in enumerate(zip(signal, a)):
        y += k * (x - y)
        izhod[i] = y
    return izhod


# --- Posamezni zvoki ----------------------------------------------------------------------------

def _pok(f0=480.0, f1=1150.0):
    # Mehurček: hiter dvig višine in kratko dušenje.
    t = _cas(0.12)
    f = f1 + (f0 - f1) * np.exp(-t / 0.012)
    faza = 2 * np.pi * np.cumsum(f) / SR
    ovojnica = _napad(t, 0.002) * np.exp(-t / 0.028)
    return np.sin(faza) * ovojnica + 0.15 * np.sin(2 * faza) * ovojnica


def _ksilofon(f=880.0, trajanje=0.55):
    # Leseni ton: osnovni ton + kratek višji (4×) prizvok, ki da »tok«.
    t = _cas(trajanje)
    ovojnica = _napad(t, 0.002)
    return ovojnica * (
        np.sin(2 * np.pi * f * t) * np.exp(-t / 0.16)
        + 0.35 * np.sin(2 * np.pi * 3.99 * f * t) * np.exp(-t / 0.025)
        + 0.12 * np.sin(2 * np.pi * 9.9 * f * t) * np.exp(-t / 0.008)
    )


def _vetrc(trajanje=1.0, vrh_pri=0.55, nizko=350.0, visoko=2600.0, seme=1):
    # Šum s filtrom, ki se odpre in zapre: »fuuš« pri premikanju predmetov.
    rng = np.random.default_rng(seme)
    t = _cas(trajanje)
    x = t / trajanje
    oblika = np.where(x < vrh_pri, x / vrh_pri, (1 - x) / (1 - vrh_pri))
    oblika = np.sin(np.pi / 2 * np.clip(oblika, 0, 1)) ** 2
    rezi = nizko + (visoko - nizko) * oblika
    sum_ = rng.standard_normal(len(t))
    pas = _nizkoprepustni(sum_, rezi) - _nizkoprepustni(sum_, rezi * 0.25)
    return pas * oblika


def _zvoncek(toni=(1046.5, 1318.5, 1568.0, 2093.0), razmik=0.07, trajanje=1.6):
    # Zmagoslavni arpeggio z zvončnimi prizvoki (za »aha« in pravilen račun).
    t = _cas(trajanje)
    izhod = np.zeros_like(t)
    for i, f in enumerate(toni):
        tt = np.clip(t - i * razmik, 0, None)
        vklop = (t >= i * razmik) * _napad(tt, 0.002)
        izhod += vklop * (
            np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.55)
            + 0.3 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-tt / 0.18)
            + 0.12 * np.sin(2 * np.pi * 5.4 * f * tt) * np.exp(-tt / 0.07)
        )
    return izhod


def _iskrice(toni=(1568.0, 1975.5, 2349.3, 2637.0, 3136.0), razmik=0.045):
    # Hiter vzpenjajoč se »čarobni« arpeggio (za poudarek in zamenjavo z n).
    t = _cas(0.7)
    izhod = np.zeros_like(t)
    for i, f in enumerate(toni):
        tt = np.clip(t - i * razmik, 0, None)
        izhod += (t >= i * razmik) * _napad(tt, 0.001) * np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.12)
    return izhod


def _svincnik(trajanje=3.0, seme=7):
    # Tiho praskanje svinčnika: visok šum z nepravilnimi potezami.
    rng = np.random.default_rng(seme)
    t = _cas(trajanje)
    sum_ = rng.standard_normal(len(t))
    visok = sum_ - _nizkoprepustni(sum_, 2500.0)
    visok = _nizkoprepustni(visok, 7000.0)
    poteze = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 3.3 * t + 1.7 * np.sin(2 * np.pi * 0.9 * t)))
    vklop = np.clip(t / 0.08, 0, 1) * np.clip((trajanje - t) / 0.15, 0, 1)
    return visok * poteze * vklop


def _drsenje(f0=300.0, f1=900.0, trajanje=0.6):
    # Mehak drsni ton (»fiiju«), ki se dvigne ali spusti.
    t = _cas(trajanje)
    f = f0 * (f1 / f0) ** (t / trajanje)
    faza = 2 * np.pi * np.cumsum(f) / SR
    ovojnica = np.sin(np.pi * t / trajanje) ** 2
    return (np.sin(faza) + 0.2 * np.sin(2 * faza)) * ovojnica


def _pero(f0=523.25, f1=659.26, trajanje=0.5, seme=3):
    # Risanje ene črte: mehak drsni ton s pridihom flomastra; traja natanko toliko kot poteza.
    rng = np.random.default_rng(seme)
    t = _cas(max(trajanje, 0.04))
    T = t[-1] if len(t) > 1 else 1.0
    f = f0 * (f1 / f0) ** (t / T)
    faza = 2 * np.pi * np.cumsum(f) / SR
    ton_ = np.sin(faza) + 0.25 * np.sin(2 * faza) + 0.08 * np.sin(3 * faza)
    sum_ = rng.standard_normal(len(t))
    flomaster = _nizkoprepustni(sum_ - _nizkoprepustni(sum_, 1500.0), 5000.0)
    ovojnica = np.clip(t / 0.015, 0, 1) * np.clip((T - t) / 0.05, 0, 1) * (1 + 0.08 * np.sin(2 * np.pi * 11 * t))
    return (ton_ + 0.6 * flomaster) * ovojnica


def _pasovni(signal, f, q):
    """Pasovno prepustni filter (biquad, RBJ) s središčem f in kakovostjo q."""
    w = 2 * np.pi * f / SR
    alfa = np.sin(w) / (2 * q)
    b0, b2 = alfa, -alfa
    a0, a1, a2 = 1 + alfa, -2 * np.cos(w), 1 - alfa
    b0, b2, a1, a2 = b0 / a0, b2 / a0, a1 / a0, a2 / a0
    izhod = np.zeros_like(signal)
    x1 = x2 = y1 = y2 = 0.0
    for i, x in enumerate(signal):
        y = b0 * x + b2 * x2 - a1 * y1 - a2 * y2
        izhod[i] = y
        x2, x1 = x1, x
        y2, y1 = y1, y
    return izhod


def _risanje(trajanje, intervali=None, gladko=False, seme=0):
    """Realističen svinčnik po papirju.

    Grafit ne šumi enakomerno: zvok je gosto zaporedje drobnih praskov, ko konica drsi čez
    papirna vlakna, z rahlim »tok« ob dotiku papirja. intervali: (začetek, konec) v sekundah,
    ko se konica dotika papirja (vmes je dvignjena). gladko: hitrost (in glasnost) sledi smooth.
    """
    rng = np.random.default_rng(seme)
    t = _cas(trajanje)
    n = len(t)
    if intervali is None:
        intervali = [(0.0, trajanje)]

    # Dotik konice s papirjem (mehki robovi ob dvigu in spustu).
    dotik = np.zeros(n)
    for zac, kon in intervali:
        dolzina = max(kon - zac, 1e-3)
        rob = min(0.008, dolzina / 3)
        del_ = (t >= zac) & (t <= kon)
        tt = t[del_]
        dotik[del_] = np.minimum(np.clip((tt - zac) / rob, 0, 1), np.clip((kon - tt) / rob, 0, 1))

    # Hitrost poteze: ob gladki animaciji počasi na začetku in koncu.
    hitrost = 0.4 + 0.6 * np.sin(np.pi * t / trajanje) ** 2 if gladko else np.ones(n)
    # Pritisk roke niha počasi in nepravilno.
    pritisk = _nizkoprepustni(rng.standard_normal(n), 5.0)
    pritisk = 0.8 + 0.2 * pritisk / (np.max(np.abs(pritisk)) or 1.0)

    # Drobni praski: naključni impulzi, gostejši pri večji hitrosti.
    gostota = 2600.0 * hitrost * dotik / SR
    zadetki = rng.random(n) < gostota
    impulzi = np.zeros(n)
    impulzi[zadetki] = rng.lognormal(0.0, 0.7, zadetki.sum()) * rng.choice([-1.0, 1.0], zadetki.sum())
    praski = _pasovni(impulzi, 2400.0, 1.1) + 0.7 * _pasovni(impulzi, 4800.0, 1.6)

    # Tih, enakomeren šum drsenja grafita pod praski.
    sum_ = rng.standard_normal(n)
    drsenje = _pasovni(sum_, 3200.0, 0.9) * 0.18

    # Mehek »tok« ob vsakem dotiku papirja.
    dotiki = np.zeros(n)
    for zac, _ in intervali:
        i = int(zac * SR)
        if i < n:
            dotiki[i] = 2.5
    tok = _pasovni(dotiki, 1500.0, 2.0)

    return (praski + drsenje * hitrost) * dotik * pritisk + 0.5 * tok


def pot_risanja(trajanje, intervali=None, gladko=False, seme=0):
    """Pot do WAV z zvokom risanja ene poteze (ustvari jo, če še ne obstaja)."""
    import hashlib
    opis = repr((round(trajanje, 4), [tuple(round(v, 4) for v in i) for i in (intervali or [])], gladko, seme))
    pot = MAPA / f"svincnik_{hashlib.md5(opis.encode()).hexdigest()[:10]}.wav"
    if not pot.exists():
        _shrani(pot, _risanje(trajanje, intervali, gladko, seme), 0.3)
    return pot


_RECEPTI = {
    "pero": (_pero, 0.45),
    "pok": (_pok, 0.7),
    "ksilofon": (_ksilofon, 0.6),
    "vetrc": (_vetrc, 0.45),
    "zvoncek": (_zvoncek, 0.6),
    "iskrice": (_iskrice, 0.4),
    "svincnik": (_svincnik, 0.25),
    "drsenje": (_drsenje, 0.35),
}


def pot_zvoka(ime, **parametri):
    """Vrne pot do WAV datoteke zvoka ``ime`` z danimi parametri (ustvari jo, če še ne obstaja)."""
    funkcija, vrh = _RECEPTI[ime]
    oznaka = "_".join(f"{k}{v:g}" if isinstance(v, (int, float)) else f"{k}{len(v)}-{v[0]:g}"
                      for k, v in sorted(parametri.items()))
    pot = MAPA / (f"{ime}_{oznaka}.wav" if oznaka else f"{ime}.wav")
    if not pot.exists():
        _shrani(pot, funkcija(**parametri), vrh)
    return pot
