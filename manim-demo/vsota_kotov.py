from manim import *
from manimpango import register_font
import numpy as np
from pathlib import Path
import sys


# Pokončni format za TikTok/Instagram.
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
# Brez predpomnilnika: pri animacijah iz predpomnilnika Manim tiho zavrže zvoke,
# dodane takoj za njimi (self.add_sound), zato bi v videu manjkala večina zvokov.
config.disable_caching = True

# Pisave Univerza Sans so vključene v projekt in registrirane za ta izris.
PROJEKT = Path(__file__).parent
# Zvočni učinki so sintetizirani v zvoki.py (isti imenik kot ta datoteka).
sys.path.insert(0, str(PROJEKT))
from zvoki import pot_risanja, pot_zvoka, ton  # noqa: E402
FONT_DIR = PROJEKT / "Univerza Sans TTF 0"
for font_file in FONT_DIR.glob("*.ttf"):
    register_font(str(font_file))

# Univerza Sans nima grških črk. Lucida Grande ima najbolj razločne oblike:
# α se ne zamenja z »a« in γ ne z »y« (pri Avenir Next se).
GRSKA_PISAVA = "Lucida Grande"
GRSKE_CRKE = "αβγ"

# Barve po barvni shemi UL (barvna-shema-UL.md): primarna rdeča in sivi ter ena sekundarna barva.
UL_RED = "#E03127"   # UL rdeča
UL_DARK = "#58595B"  # antracitno siva: glavne črte in besedilo
UL_GRAY = "#A7A8AA"  # siva 40 %: pomožne črte (ne za besedilo, premajhen kontrast)
UL_BLUE = "#2878AC"  # sinjemodra: sekundarna barva za kot β
# Dodatne sekundarne barve UL samo za nove kote na zadnjem kadru (vsak kot svoja barva).
UL_GREEN = "#00694E"      # zelena
UL_TURQUOISE = "#40AEAD"  # turkizna
UL_PINK = "#EC61A0"       # roza (rumena ima na beli podlagi premajhen kontrast)
BG = "#FFFFFF"       # bela podlaga: kontrast rdeče in modre doseže 4,5 : 1

config.background_color = BG

# Velikosti besedila, berljive na telefonu.
NASLOV = 42
BESEDILO = 34
OZNAKE = 32

# Tri debeline črt.
DEBELA = 6   # glavne črte: stranice, obris
SREDNJA = 4  # pomožne črte: premice, podaljški, diagonale
TANKA = 3    # loki kotov


# Zvoki premikov in prehodov (akcije) so za toliko dB tišji od zvokov poudarkov.
TISJE_AKCIJA = -9
# Skupna ojačitev miksa (dB): celoten video zveni okoli −15 LUFS, vrhovi ostanejo pod 0 dBFS.
GLASNOST_MIKSA = 5.5


class VsotaKotov(Scene):
    def zvok(self, ime, zamik=0.0, glasnost=0.0, akcija=False, **parametri):
        # Doda zvočni učinek ob trenutnem času videa (+ zamik v sekundah); glasnost v dB.
        # akcija=True: zvok premika ali prehoda (npr. prenos kota) je tišji od poudarkov.
        if akcija:
            glasnost += TISJE_AKCIJA
        self.add_sound(str(pot_zvoka(ime, **parametri)), time_offset=zamik, gain=glasnost + GLASNOST_MIKSA)

    def zvok_risanja(self, trajanje, intervali=None, gladko=False, zamik=0.0, glasnost=0, seme=0):
        # Mehak »vuš« za eno potezo (brez tonov in brez praskanja).
        pot = pot_risanja(trajanje, intervali, gladko, seme)
        self.add_sound(str(pot), time_offset=zamik, gain=glasnost + GLASNOST_MIKSA)

    def zvok_risanja_lika(self, st_stranic, trajanje, glasnost=0, seme=0):
        # Create riše lik v eni potezi po krivulji smooth. Vsaka stranica dobi svoj mehak
        # »vuš«, ob oglišču je kratek premor, tako se sliši vsaka stranica posebej.
        casi = np.linspace(0, 1, 2001)
        vrednosti = np.array([smooth(x) for x in casi])
        meje = [trajanje * float(np.interp(k / st_stranic, vrednosti, casi)) for k in range(st_stranic + 1)]
        premor = 0.025
        intervali = [(meje[k] + (premor if k else 0), meje[k + 1] - (premor if k < st_stranic - 1 else 0))
                     for k in range(st_stranic)]
        self.zvok_risanja(trajanje, intervali, gladko=True, glasnost=glasnost, seme=seme)

    def _pisava_za_grske(self, text, kwargs):
        t2f = dict(kwargs.pop("t2f", {}))
        for crka in GRSKE_CRKE:
            if crka in text:
                t2f.setdefault(crka, GRSKA_PISAVA)
        return t2f

    def txt(self, text, size=BESEDILO, color=UL_DARK, razmik=1.0, max_width=5.6, **kwargs):
        # Večvrstično besedilo (z "\n") je sredinsko poravnano, vrstice pa so
        # med seboj enako oddaljene po osnovni črti, ne glede na črke, kot sta š ali j.
        kwargs.pop("line_spacing", None)
        t2f = self._pisava_za_grske(text, kwargs)
        vrstice = text.split("\n")
        if len(vrstice) == 1:
            text_mobject = Text(text, font="Univerza Sans", font_size=size, color=color, t2f=t2f, **kwargs)
        else:
            text_mobject = VGroup()
            for i, vrstica in enumerate(vrstice):
                # Enak »opornik« Šj pred vsako vrstico določi njeno navpično lego, nato ga odstranimo.
                s_opornikom = Text("Šj" + vrstica, font="Univerza Sans", font_size=size, color=color, t2f=t2f, **kwargs)
                opornik = VGroup(s_opornikom[0], s_opornikom[1])
                korak = razmik * opornik.height
                s_opornikom.shift(UP * (-i * korak - opornik.get_center()[1]))
                text_mobject.add(VGroup(*s_opornikom[2:]).set_x(0))
            text_mobject.move_to(ORIGIN)
        # Reels UI overlaps the outer right edge and the lower caption area.
        if text_mobject.width > max_width:
            logger.warning(f"Besedilo je preširoko in bo pomanjšano: {text!r} ({text_mobject.width:.2f})")
            text_mobject.scale_to_fit_width(max_width)
        return text_mobject

    def mat(self, text, size=56, color=UL_RED, **kwargs):
        # Formule in oznake kotov v pisavi Univerza Sans (grške črke v Avenir Next), ne v LaTeXu.
        t2f = self._pisava_za_grske(text, kwargs)
        return Text(text, font="Univerza Sans", font_size=size, color=color, t2f=t2f, **kwargs)

    def heading(self, text, top=5.85):
        # Vsi naslovi: Univerza Sans Medium, enaka velikost, isti zgornji rob (pod zgornjo vrstico Instagrama).
        # Na vrhu zaslona ni gumbov, zato je dovoljena večja širina kot pri besedilu.
        vrstice = self.txt(text, size=NASLOV, color=UL_RED, weight="MEDIUM", max_width=7.5)
        return vrstice.move_to([0, top - vrstice.height / 2, 0])

    def construct(self):
        # 1. Prvi kader (kavelj): vprašanje in poljuben trikotnik s tremi koti, ki spreminja obliko.
        naslov = self.heading("VSOTA NOTRANJIH KOTOV\nV TRIKOTNIKU")

        # Nepravilen trikotnik z rahlo nagnjeno osnovnico. Desni del ostane levo od
        # stolpca gumbov Instagrama (x < 3,25 v spodnji polovici zaslona).
        A = np.array([-3.25, -2.45, 0])
        B = np.array([0.1, 1.95, 0])
        C = np.array([2.75, -1.8, 0])
        smer_AB = normalize(B - A)
        smer_BC = normalize(C - B)

        polmer_kota = 1.25
        odmik_oznake = 0.8
        VELIKOST_OZNAKE_KOTA = 40

        # Oznake ležijo na notranjih simetralah kotov, blizu posameznih oglišč.
        def simetrala(vrh, krak_1, krak_2):
            return normalize(normalize(krak_1 - vrh) + normalize(krak_2 - vrh))

        def smerni_kot(od, do):
            d = do - od
            return np.arctan2(d[1], d[0])

        def lok(vrh, zacetni_kot, koncni_kot, barva):
            return Arc(
                arc_center=vrh,
                start_angle=zacetni_kot,
                angle=(koncni_kot - zacetni_kot) % TAU,
                color=barva,
                radius=polmer_kota,
                stroke_width=TANKA,
            )

        def odsek(vrh, zacetni_kot, koncni_kot, barva, polnilo=0.18):
            return Sector(
                radius=polmer_kota,
                start_angle=zacetni_kot,
                angle=(koncni_kot - zacetni_kot) % TAU,
                color=barva,
                fill_opacity=polnilo,
                stroke_width=0,
            ).move_arc_center_to(vrh)

        # Oznake kotov po slovenskem učbeniškem dogovoru: zgornje oglišče je C, zato je zgornji kot γ.
        # Imena spremenljivk beta_* / gamma_* označujejo kot pri B (zgoraj) oz. C (spodaj desno).
        def skica_trikotnika(A, B, C):
            # Stranice, koti (odsek in lok) in oznake trikotnika; enako za mirujočo in živo skico.
            return {
                "AB": Line(A, B, color=UL_DARK, stroke_width=DEBELA),
                "BC": Line(B, C, color=UL_DARK, stroke_width=DEBELA),
                "CA": Line(C, A, color=UL_DARK, stroke_width=DEBELA),
                "alpha_odsek": odsek(A, smerni_kot(A, C), smerni_kot(A, B), UL_RED),
                "beta_odsek": odsek(B, smerni_kot(B, A), smerni_kot(B, C), UL_DARK),
                "gamma_odsek": odsek(C, smerni_kot(C, B), smerni_kot(C, A), UL_BLUE),
                "alpha_lok": lok(A, smerni_kot(A, C), smerni_kot(A, B), UL_RED),
                "beta_lok": lok(B, smerni_kot(B, A), smerni_kot(B, C), UL_DARK),
                "gamma_lok": lok(C, smerni_kot(C, B), smerni_kot(C, A), UL_BLUE),
                "alpha_dol": self.mat("α", size=VELIKOST_OZNAKE_KOTA, color=UL_RED).move_to(A + simetrala(A, B, C) * odmik_oznake),
                "beta_dol": self.mat("γ", size=VELIKOST_OZNAKE_KOTA, color=UL_DARK).move_to(B + simetrala(B, A, C) * odmik_oznake),
                "gamma_dol": self.mat("β", size=VELIKOST_OZNAKE_KOTA, color=UL_BLUE).move_to(C + simetrala(C, A, B) * odmik_oznake),
            }

        skica = skica_trikotnika(A, B, C)
        stranica_AB, stranica_BC, stranica_CA = skica["AB"], skica["BC"], skica["CA"]
        alpha_odsek, beta_odsek, gamma_odsek = skica["alpha_odsek"], skica["beta_odsek"], skica["gamma_odsek"]
        alpha_lok, beta_lok, gamma_lok = skica["alpha_lok"], skica["beta_lok"], skica["gamma_lok"]
        alpha_dol, beta_dol, gamma_dol = skica["alpha_dol"], skica["beta_dol"], skica["gamma_dol"]

        ang_A_to_B = smerni_kot(A, B)
        ang_A_to_C = smerni_kot(A, C)
        ang_B_to_A = smerni_kot(B, A)
        ang_B_to_C = smerni_kot(B, C)
        ang_C_to_A = smerni_kot(C, A)
        ang_C_to_B = smerni_kot(C, B)

        # Besedilo zgoraj (pod naslovom) in spodaj, nad območjem opisa na Instagramu.
        # Kavelj ne sprašuje »koliko« (odgovor 180° vsi poznajo), ampak »zakaj«.
        uvod_1 = self.txt("Vsak trikotnik ima 180°.\nAmpak zakaj?", t2c={"Ampak zakaj?": UL_RED}).move_to(UP * 3.8)
        uvod_2 = self.txt("Ne glede na obliko\nje vsota vedno 180°.").move_to(DOWN * 3.25)
        uvod_3 = self.txt("Poglejmo, zakaj.").move_to(DOWN * 3.25)
        vzporednica_txt = self.txt("Skozi zgornje oglišče\nnarišemo vzporednico p′\nk osnovnici.").move_to(DOWN * 3.42)

        # Živa skica: zgornje oglišče drsi vzporedno z osnovnico, koti se sproti prilagajajo.
        smer_p = normalize(C - A)
        zamik_B = ValueTracker(0.0)
        ziva_skica = always_redraw(
            lambda: VGroup(*skica_trikotnika(A, B + smer_p * zamik_B.get_value(), C).values())
        )
        # Prvi kader: naslov, vprašanje in trikotnik s koti so vidni že v prvi sličici
        # (predogled na Instagramu ni prazen, zadnja sličica videa je enaka prvi).
        self.add(naslov, uvod_1, ziva_skica)
        self.wait(1.0)
        for i, (cilj, trajanje) in enumerate(((-2.6, 1.3), (2.0, 1.7), (0.0, 1.1))):
            self.zvok_risanja(trajanje, gladko=True, glasnost=-3, seme=20 + i)  # oglišče drsi
            animacije = [zamik_B.animate.set_value(cilj)]
            if i == 0:
                animacije.append(FadeIn(uvod_2))
            self.play(*animacije, run_time=trajanje)
        self.wait(0.6)
        # Živo skico zamenjamo z enako mirujočo (isti položaj, ni vidnega skoka).
        self.remove(ziva_skica)
        self.add(*skica.values())
        self.play(FadeOut(uvod_2), run_time=0.4)
        self.play(FadeIn(uvod_3), run_time=0.5)
        self.wait(1.4)  # čas za branje: kaj bomo pokazali

        # 2. Stranice istega trikotnika podaljšamo v premice r, q in p ter osnovnici dodamo vzporednico p′.
        # Premice so pomožne (tanjše); stranice trikotnika ostanejo debele, da je trikotnik ves čas viden.
        podaljsek = 0.5
        r_konca = (A - smer_AB * podaljsek, B + smer_AB * podaljsek)
        q_konca = (B - smer_BC * podaljsek, C + smer_BC * podaljsek)
        p_konca = (A - smer_p * podaljsek, C + smer_p * podaljsek)
        r_crta = Line(A, B, color=UL_GRAY, stroke_width=SREDNJA).set_z_index(-1)
        q_crta = Line(B, C, color=UL_GRAY, stroke_width=SREDNJA).set_z_index(-1)
        p_crta = Line(C, A, color=UL_DARK, stroke_width=SREDNJA).set_z_index(-1)
        # p′ gre skozi B in pokriva isti vodoravni razpon kot p.
        pp = Line(
            B + smer_p * (p_konca[0][0] - B[0]) / smer_p[0],
            B + smer_p * (p_konca[1][0] - B[0]) / smer_p[0],
            color=UL_DARK,
            stroke_width=SREDNJA,
        ).set_z_index(-1)

        tezisce = (A + B + C) / 3

        def normala_navzven(smer, tocka_na_premici, stran_od=None):
            n = np.array([-smer[1], smer[0], 0.0])
            referenca = tezisce if stran_od is None else stran_od
            return n if np.dot(n, tocka_na_premici - referenca) > 0 else -n

        # Oznaka p leži nad premico (desno od C), da je podaljšek premice q ne seka.
        oznaka_p = self.txt("p", size=OZNAKE).move_to(
            p_konca[1] - smer_p * 0.15 - normala_navzven(smer_p, C) * 0.42
        )
        oznaka_pp = self.txt("p′", size=OZNAKE).move_to(
            pp.get_end() - smer_p * 0.2 + normala_navzven(smer_p, B) * 0.42
        )

        self.add(r_crta, q_crta, p_crta)
        # Stranice se podaljšajo v tri premice hkrati (brez zvoka).
        self.play(
            r_crta.animate.put_start_and_end_on(*r_konca),
            q_crta.animate.put_start_and_end_on(*q_konca),
            p_crta.animate.put_start_and_end_on(p_konca[1], p_konca[0]),
            FadeOut(uvod_3),
            run_time=1.4,
        )
        # Premica skupaj s pripadajočo stranico (za zatemnjevanje in prikaz).
        r = VGroup(r_crta, stranica_AB)
        q = VGroup(q_crta, stranica_BC)
        p = VGroup(p_crta, stranica_CA)
        # Imenujemo le premici, ki ju potrebujemo v razlagi: osnovnico p (in pozneje p′).
        self.zvok("pok", f1=1400, glasnost=-6)
        self.play(FadeIn(oznaka_p), run_time=0.4)
        self.zvok_risanja(1.2, gladko=True, seme=5)  # vzporednica p′ se nariše
        self.play(FadeIn(vzporednica_txt), Create(pp), run_time=1.2)
        # Oznaka p′ se pokaže šele, ko je premica narisana, skupaj s pokom (enako kot oznaka p).
        self.zvok("pok", f1=1600, glasnost=-6)
        self.play(FadeIn(oznaka_pp), run_time=0.4)
        self.wait(1.6)  # čas za branje: vzporednica p′

        # Kota α in β, ki ju bomo prenesli na vzporednico p′ v oglišče B.
        alpha_vrh = self.mat("α", size=VELIKOST_OZNAKE_KOTA, color=UL_RED).move_to(B + simetrala(B, A, B - smer_p) * odmik_oznake)
        gamma_vrh = self.mat("β", size=VELIKOST_OZNAKE_KOTA, color=UL_BLUE).move_to(B + simetrala(B, C, B + smer_p) * odmik_oznake)
        alpha_vrh_lok = lok(B, ang_C_to_A, ang_B_to_A, UL_RED).set_stroke(opacity=0)
        gamma_vrh_lok = lok(B, ang_B_to_C, ang_A_to_C, UL_BLUE).set_stroke(opacity=0)
        zasuk_alpha = (ang_C_to_A - ang_A_to_C) % TAU
        zasuk_gamma = ang_B_to_C - ang_C_to_B

        def prenesi_kot(sektor, zasuk, od, do):
            # Sektor se vrti okoli svojega vrha, medtem ko vrh drsi od »od« do »do«.
            zacetni = sektor.copy()
            return UpdateFromAlphaFunc(
                sektor,
                lambda m, t: m.become(zacetni.copy().rotate(zasuk * t, about_point=od).shift((do - od) * t)),
            )

        def utrip(oznaka, odsek_kota):
            # Oznaka kota se poveča in zmanjša, njegov odsek se za hip močneje obarva.
            return AnimationGroup(
                oznaka.animate(rate_func=there_and_back).scale(1.5),
                odsek_kota.animate(rate_func=there_and_back).set_fill(opacity=0.5),
            )

        def pojavi_z_utripom(oznaka, faktor=1.5):
            # Nova oznaka zraste iz nič čez polno velikost in se ustali (enako kot utrip).
            zacetna = oznaka.copy()

            def velikost(t):
                if t < 0.5:
                    return 0.01 + (faktor - 0.01) * smooth(t / 0.5)
                return faktor + (1 - faktor) * smooth((t - 0.5) / 0.5)

            return UpdateFromAlphaFunc(oznaka, lambda m, t: m.become(zacetna.copy().scale(velikost(t))))

        # Vsak kot ima svoj ton: isti ton pri spodnjem in zgornjem kotu pove, da gre za enak kot.
        TON_ALPHA = ton(2)
        TON_BETA = ton(4)

        ZATEMNJENO = 0.25

        # 3. Frame: fokus na premici p, p′ in r; primerjamo kot α z novokonstruiranim α.
        # Uvodno besedilo izgine v isti potezi, ko se q umakne v ozadje.
        self.play(
            FadeOut(naslov, uvod_1, vzporednica_txt),
            q.animate.set_opacity(ZATEMNJENO),
            gamma_dol.animate.set_opacity(0.0),
            gamma_lok.animate.set_stroke(opacity=0.0),
            beta_dol.animate.set_opacity(1.0),
            oznaka_p.animate.set_opacity(0.6),
            oznaka_pp.animate.set_opacity(0.6),
            run_time=0.8,
        )

        razlaga_alpha_1 = self.txt("Ker sta p in p′ vzporedni,\nsta izmenična kota\nob tej premici enaka.", t2c={"tej": UL_RED}).move_to(UP * 4.3)
        razlaga_alpha_2 = self.txt("Torej je zgornji kot\nenak spodnjemu.").move_to(DOWN * 3.25)
        # »Ob tej premici«: premica, ob kateri ležita izmenična kota, se obarva enako kot beseda »tej«
        # in ostane poudarjena, dokler se kot α ne prenese.
        self.play(
            FadeIn(razlaga_alpha_1),
            r_crta.animate.set_stroke(color=UL_RED, width=SREDNJA * 1.75),
            stranica_AB.animate.set_stroke(color=UL_RED),
            run_time=0.9,
        )
        self.zvok("kapljica", f=TON_ALPHA)  # spodnji α
        self.play(utrip(alpha_dol, alpha_odsek), run_time=0.7)
        self.wait(0.2)
        self.zvok("kapljica", f=TON_ALPHA)  # zgornji α: isti ton, ker je enak
        self.play(pojavi_z_utripom(alpha_vrh), FadeIn(razlaga_alpha_2), run_time=0.7)
        self.wait(1.6)  # čas za branje: izmenična kota
        self.zvok_risanja(1.5, gladko=True, seme=17)  # odsek α potuje (tih vuš)
        self.zvok("potrditev", zamik=1.45, glasnost=-4)  # odsek se lepo poklopi: »pling-pling«
        self.play(prenesi_kot(alpha_odsek, zasuk_alpha, A, B), run_time=1.5)
        self.wait(0.6)

        # 4. Frame: fokus na premici p, p′ in q; primerjamo kot β z novokonstruiranim β.
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            stranica_AB.animate.set_stroke(color=UL_DARK, opacity=ZATEMNJENO),
            r_crta.animate.set_stroke(color=UL_GRAY, width=SREDNJA, opacity=ZATEMNJENO),
            q.animate.set_opacity(1.0),
            alpha_dol.animate.set_opacity(ZATEMNJENO),
            alpha_lok.animate.set_stroke(opacity=ZATEMNJENO),
            alpha_vrh.animate.set_opacity(ZATEMNJENO),
            beta_dol.animate.set_opacity(1.0),
            gamma_dol.animate.set_opacity(1.0),
            gamma_lok.animate.set_stroke(opacity=1.0),
            FadeOut(razlaga_alpha_1, razlaga_alpha_2),
            run_time=1.2,
        )
        razlaga_gamma_1 = self.txt("Enako velja za drugi par\nkotov ob tej premici.", t2c={"tej": UL_BLUE}).move_to(UP * 4.3)
        self.play(
            FadeIn(razlaga_gamma_1),
            q_crta.animate.set_stroke(color=UL_BLUE, width=SREDNJA * 1.75),  # ostane poudarjena do prenosa β
            stranica_BC.animate.set_stroke(color=UL_BLUE),
            run_time=0.9,
        )
        self.zvok("kapljica", f=TON_BETA)  # spodnji β
        self.play(utrip(gamma_dol, gamma_odsek), run_time=0.7)
        self.wait(0.2)
        self.zvok("kapljica", f=TON_BETA)  # zgornji β: isti ton, ker je enak
        self.play(pojavi_z_utripom(gamma_vrh), run_time=0.7)
        self.wait(0.4)
        self.zvok_risanja(1.6, gladko=True, seme=18)  # odsek β potuje (tih vuš)
        self.zvok("potrditev", zamik=1.55, glasnost=-4)  # odsek se lepo poklopi: »pling-pling«
        self.play(prenesi_kot(gamma_odsek, zasuk_gamma, C, B), run_time=1.6)
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            r.animate.set_opacity(1.0),
            stranica_BC.animate.set_stroke(color=UL_DARK, opacity=1.0),
            q_crta.animate.set_stroke(color=UL_GRAY, width=SREDNJA, opacity=1.0),
            oznaka_p.animate.set_opacity(1.0),
            oznaka_pp.animate.set_opacity(1.0),
            alpha_dol.animate.set_opacity(1.0),
            alpha_lok.animate.set_stroke(opacity=1.0),
            alpha_vrh.animate.set_opacity(1.0),
            alpha_vrh_lok.animate.set_stroke(opacity=1.0),
            beta_dol.animate.set_opacity(1.0),
            gamma_dol.animate.set_opacity(1.0),
            gamma_lok.animate.set_stroke(opacity=1.0),
            gamma_vrh.animate.set_opacity(1.0),
            gamma_vrh_lok.animate.set_stroke(opacity=1.0),
            FadeOut(razlaga_gamma_1),
            run_time=1.2,
        )

        # 5. »Aha« trenutek: koti ob vrhu skupaj tvorijo ravni kot, števec prešteje do 180°.
        sklep_1 = self.txt("Ob oglišču α, γ in β skupaj\ntvorijo iztegnjeni kot.").move_to(UP * 4.3)

        # Vse razen vrha stopi v ozadje; iz vrha zraste ravna črta (ravni kot).
        zatemnjene_crte = VGroup(p, r, q)
        zatemnjene_oznake = VGroup(oznaka_p, oznaka_pp, alpha_dol, gamma_dol)
        zatemnjeni_loki = VGroup(alpha_lok, gamma_lok)
        dolzina_ravne = polmer_kota + 0.55
        ravna_crta = Line(B - smer_p * dolzina_ravne, B + smer_p * dolzina_ravne, color=UL_DARK, stroke_width=DEBELA + 2)

        # Koti ob vrhu od leve proti desni: α, γ (siv, pri B) in β (moder, prenesen iz C).
        razpon_alpha = (ang_B_to_A - ang_C_to_A) % TAU
        razpon_srednji = (ang_B_to_C - ang_B_to_A) % TAU
        razpon_desni = PI - razpon_alpha - razpon_srednji

        preteceni_kot = ValueTracker(0.0)  # v stopinjah, od leve strani ravne črte
        stevec_polozaj = B + DOWN * (polmer_kota + 0.85)
        VELIKOST_STEVCA = 88

        def stevec_za(vrednost):
            return self.mat(f"{int(round(vrednost))}°", size=VELIKOST_STEVCA).move_to(stevec_polozaj)

        stevec = stevec_za(0)
        stevec.add_updater(lambda m: m.become(stevec_za(preteceni_kot.get_value())))

        drsni_lok = always_redraw(lambda: Arc(
            arc_center=B,
            radius=polmer_kota,
            start_angle=ang_C_to_A,
            angle=max(preteceni_kot.get_value() * DEGREES, 1e-4),
            color=UL_DARK,
            stroke_width=TANKA,
        ))

        # Kazalec: polmer iz vrha B, ki se vrti skupaj z drsnim lokom in kaže trenutno stopinjo.
        def smer_kazalca():
            kot = ang_C_to_A + preteceni_kot.get_value() * DEGREES
            return np.array([np.cos(kot), np.sin(kot), 0.0])

        kazalec = always_redraw(lambda: Line(
            B, B + smer_kazalca() * (polmer_kota + 0.3), color=UL_RED, stroke_width=DEBELA,
        ).set_z_index(5))
        konica_kazalca = always_redraw(lambda: Dot(
            B + smer_kazalca() * polmer_kota, radius=0.1, color=UL_RED,
        ).set_z_index(6))

        # Kazalec se pojavi na levem kraku ravnega kota, šele nato začne krožiti.
        zacetni_kazalec = VGroup(
            Line(B, B + smer_kazalca() * (polmer_kota + 0.3), color=UL_RED, stroke_width=DEBELA).set_z_index(5),
            Dot(B + smer_kazalca() * polmer_kota, radius=0.1, color=UL_RED).set_z_index(6),
        )

        def napolni_ob_prehodu(sektor, zacetek, razpon, dodatek=0.25):
            # Sektor se obarva, ko čezenj potuje drsni lok.
            sektor.add_updater(lambda m: m.set_fill(
                opacity=0.18 + dodatek * np.clip((preteceni_kot.get_value() * DEGREES - zacetek) / razpon, 0, 1)
            ))

        self.zvok_risanja(0.9, gladko=True, seme=15)  # ravna črta zraste iz vrha
        self.play(
            zatemnjene_crte.animate.set_opacity(ZATEMNJENO),
            zatemnjene_oznake.animate.set_opacity(ZATEMNJENO),
            zatemnjeni_loki.animate.set_stroke(opacity=ZATEMNJENO),
            GrowFromCenter(ravna_crta),
            FadeIn(sklep_1),
            FadeIn(stevec),
            FadeIn(zacetni_kazalec),
            run_time=0.9,
        )
        # Mirujoči kazalec zamenjamo z vrtečim (na istem mestu), ki nato obide ravni kot.
        self.remove(zacetni_kazalec)
        self.add(kazalec, konica_kazalca)

        napolni_ob_prehodu(alpha_odsek, 0, razpon_alpha)
        napolni_ob_prehodu(beta_odsek, razpon_alpha, razpon_srednji, dodatek=0.1)  # siva naj ne postane umazana
        napolni_ob_prehodu(gamma_odsek, razpon_alpha + razpon_srednji, razpon_desni)
        self.add(drsni_lok)
        # Števec: tih »blip« na vsakih 5°, časovno po isti krivulji smooth kot kazalec,
        # zato se tiki zgostijo, ko kazalec pospeši, in razredčijo, ko se ustavlja.
        self.zvok("stevec", trajanje=2.4, koraki=36, glasnost=-8)
        self.play(preteceni_kot.animate.set_value(180), run_time=2.4, rate_func=smooth)
        for mobjekt in (alpha_odsek, beta_odsek, gamma_odsek, stevec, kazalec, konica_kazalca):
            mobjekt.clear_updaters()
        self.remove(drsni_lok)
        polkrog_obroba = Arc(arc_center=B, radius=polmer_kota, start_angle=ang_C_to_A, angle=PI, color=UL_DARK, stroke_width=TANKA)
        self.add(polkrog_obroba)

        # Kratek poudarek na končni vrednosti; kazalec, ki je obšel ravni kot, izgine.
        self.zvok("zvoncek")  # 180°!
        self.play(
            stevec.animate(rate_func=there_and_back).scale(1.18),
            FadeOut(kazalec, konica_kazalca),
            run_time=0.5,
        )
        self.wait(0.6)

        # 180° se kot celota premakne v formulo; α, β, γ priletijo iz skice; skica se vrne v polno moč.
        # Znaki formule (brez presledkov): α + β + γ = 1 8 0 °
        formula_trikotnik = self.mat(
            "α + β + γ = 180°", size=60, color=UL_DARK,
            t2c={"α": UL_RED, "β": UL_BLUE, "γ": UL_DARK, "180°": UL_RED},
        ).move_to(DOWN * 3.2)
        stevilo_v_formuli = VGroup(*formula_trikotnik[6:10])
        sklep_2 = self.txt("Vsota notranjih kotov\nv trikotniku je 180°.").move_to(UP * 4.3)
        # α, β in γ priletijo v formulo: trije poki ob pristanku.
        # Med letom ostane skica zatemnjena, spodnji oznaki α in β pa za hip izgineta,
        # da se leteče črke ne prekrivajo z njima; skica se okrepi šele, ko so črke na mestu.
        # Najprej se 180° premakne na svoje mesto v formuli (z znakom =), da ne stoji na poti črk.
        self.play(
            stevec.animate.scale_to_fit_height(stevilo_v_formuli.height).move_to(stevilo_v_formuli),
            FadeIn(formula_trikotnik[5]),
            alpha_dol.animate.set_opacity(0.0),
            gamma_dol.animate.set_opacity(0.0),
            FadeOut(ravna_crta),
            FadeOut(sklep_1),
            run_time=0.7,
        )
        # Nato črke letijo zaporedno (α, β, γ), da se njihove poti ne prekrivajo; pok ob vsakem pristanku.
        cas_leta, zamik_leta = 1.2, 0.35
        trajanje_crke = cas_leta / (1 + zamik_leta * 2)
        for i in range(3):
            self.zvok("pok", zamik=(i * zamik_leta + 0.9) * trajanje_crke, f1=1100 + 200 * i, glasnost=-4)
        self.zvok("vetrc", trajanje=1.2, seme=9, glasnost=-10, akcija=True)
        self.play(
            LaggedStart(
                TransformFromCopy(alpha_vrh, formula_trikotnik[0]),
                TransformFromCopy(gamma_vrh, formula_trikotnik[2]),
                TransformFromCopy(beta_dol, formula_trikotnik[4]),
                lag_ratio=zamik_leta,
            ),
            FadeIn(formula_trikotnik[1], formula_trikotnik[3]),
            run_time=cas_leta,
        )
        self.play(
            zatemnjene_crte.animate.set_opacity(1.0),
            zatemnjene_oznake.animate.set_opacity(1.0),
            zatemnjeni_loki.animate.set_stroke(opacity=1.0),
            FadeIn(sklep_2),
            run_time=0.7,
        )
        self.remove(stevec)
        self.add(stevilo_v_formuli)
        self.wait(2.6)  # čas za branje: glavni rezultat 180°

        # 6. »Poljuben« res pomeni vsak: zgornje oglišče drsi po p′, vsi koti se sproti prilagajajo,
        # trije koti ob vrhu pa ves čas sestavljajo iztegnjeni kot. Zgoraj se sproti izpisujejo meritve.
        polnila_vrha = [m.get_fill_opacity() for m in (alpha_odsek, beta_odsek, gamma_odsek)]

        def ziv_dokaz(Bt):
            a_AB, a_AC = smerni_kot(A, Bt), smerni_kot(A, C)
            a_BA, a_BC = smerni_kot(Bt, A), smerni_kot(Bt, C)
            a_CB, a_CA = smerni_kot(C, Bt), smerni_kot(C, A)
            levo, desno = smerni_kot(Bt, Bt - smer_p), smerni_kot(Bt, Bt + smer_p)
            oznaka = lambda crka, barva: self.mat(crka, size=VELIKOST_OZNAKE_KOTA, color=barva)
            return VGroup(
                Line(A, Bt, color=UL_DARK, stroke_width=DEBELA),
                Line(Bt, C, color=UL_DARK, stroke_width=DEBELA),
                lok(A, a_AC, a_AB, UL_RED),
                lok(C, a_CB, a_CA, UL_BLUE),
                oznaka("α", UL_RED).move_to(A + simetrala(A, Bt, C) * odmik_oznake),
                oznaka("β", UL_BLUE).move_to(C + simetrala(C, A, Bt) * odmik_oznake),
                odsek(Bt, levo, a_BA, UL_RED, polnila_vrha[0]),
                odsek(Bt, a_BA, a_BC, UL_DARK, polnila_vrha[1]),
                odsek(Bt, a_BC, desno, UL_BLUE, polnila_vrha[2]),
                lok(Bt, levo, a_BA, UL_RED),
                lok(Bt, a_BA, a_BC, UL_DARK),
                lok(Bt, a_BC, desno, UL_BLUE),
                Arc(arc_center=Bt, radius=polmer_kota, start_angle=levo, angle=PI, color=UL_DARK, stroke_width=TANKA),
                oznaka("α", UL_RED).move_to(Bt + simetrala(Bt, A, Bt - smer_p) * odmik_oznake),
                oznaka("γ", UL_DARK).move_to(Bt + simetrala(Bt, A, C) * odmik_oznake),
                oznaka("β", UL_BLUE).move_to(Bt + simetrala(Bt, C, Bt + smer_p) * odmik_oznake),
            )

        def notranji_kot(v, u, w):
            return np.degrees(abs((smerni_kot(v, u) - smerni_kot(v, w) + PI) % TAU - PI))

        def zaokrozi_ohrani_vsoto(vrednosti):
            # Metoda največjih ostankov: vsaka vrednost se zaokroži navzdol ali navzgor (odstopa < 1°),
            # izpisana vsota pa je enaka zaokroženi izmerjeni vsoti (brez 179° ali 181° zaradi zaokroževanja).
            cilj = int(round(sum(vrednosti)))
            spodaj = [int(np.floor(v)) for v in vrednosti]
            po_ostanku = sorted(range(len(vrednosti)), key=lambda i: vrednosti[i] - spodaj[i], reverse=True)
            for i in po_ostanku[:cilj - sum(spodaj)]:
                spodaj[i] += 1
            return spodaj

        def odcitek(Bt):
            # Vsi trije koti so izmerjeni neodvisno iz lege oglišč (noben ni izračunan iz izreka).
            a, g, b = zaokrozi_ohrani_vsoto([notranji_kot(A, Bt, C), notranji_kot(Bt, A, C), notranji_kot(C, A, Bt)])
            return self.mat(
                f"α = {a}°   γ = {g}°   β = {b}°", size=44, color=UL_DARK,
                t2c={"α": UL_RED, "β": UL_BLUE},
            ).move_to(UP * 3.35)

        ziv_B = ValueTracker(0.0)
        ziva_slika = always_redraw(lambda: ziv_dokaz(B + smer_p * ziv_B.get_value()))
        ziv_odcitek = always_redraw(lambda: odcitek(B + smer_p * ziv_B.get_value()))
        sklep_3 = self.txt("To velja za vsak trikotnik.").move_to(UP * 4.3)

        # Pomožni premici skozi stranici umaknemo, da je slika med premikanjem mirna.
        # Vzporednico p′ podaljšamo na obe strani, da odseka ob vrhu pri skrajnih legah oglišča
        # ne segata čez njena konca (p′ je v zgornji polovici, stran od gumbov Instagrama).
        pp_dalje = [B + smer_p * (x - B[0]) / smer_p[0] for x in (-4.15, 3.65)]
        premik_oznake_pp = pp_dalje[1] - pp.get_end()
        self.play(
            FadeOut(r_crta, q_crta, sklep_2),
            pp.animate.put_start_and_end_on(*pp_dalje),
            oznaka_pp.animate.shift(premik_oznake_pp),
            run_time=0.6,
        )
        # Mirujočo sliko zamenjamo z enako živo (isti položaj, ni vidnega skoka).
        self.remove(
            stranica_AB, stranica_BC, alpha_lok, gamma_lok, alpha_dol, gamma_dol,
            alpha_odsek, beta_odsek, gamma_odsek, alpha_vrh_lok, beta_lok, gamma_vrh_lok,
            polkrog_obroba, alpha_vrh, beta_dol, gamma_vrh,
        )
        self.add(ziva_slika)
        self.zvok("pok", f1=1100, glasnost=-8)
        self.play(FadeIn(sklep_3), FadeIn(ziv_odcitek), run_time=0.6)
        for i, (cilj, trajanje) in enumerate(((-2.6, 1.6), (2.0, 2.0), (0.0, 1.3))):
            self.zvok_risanja(trajanje, gladko=True, glasnost=-3, seme=30 + i)  # oglišče drsi po p′
            self.play(ziv_B.animate.set_value(cilj), run_time=trajanje)
        self.zvok("potrditev", glasnost=-4)  # vsota je vedno 180°
        self.play(formula_trikotnik.animate(rate_func=there_and_back).scale(1.12), run_time=0.6)
        self.wait(1.0)
        ziva_slika.clear_updaters()
        ziv_odcitek.clear_updaters()

        final_proof_group = VGroup(*[m for m in self.mobjects if isinstance(m, VMobject)])
        # 7. Prehod: isto idejo uporabimo pri večkotniku. Vprašanje se pojavi že med izginjanjem trikotnika.
        prehod = self.heading("KAJ PA VEČKOTNIK?")
        self.zvok("vetrc", trajanje=0.8, seme=10, glasnost=-6, akcija=True)
        self.zvok("pok", zamik=0.4, f1=900)
        self.play(FadeOut(final_proof_group), FadeIn(prehod), run_time=0.8)
        self.remove(*[m for m in self.mobjects if m is not prehod])
        podvprasanje = self.txt(
            "Tudi večkotnik lahko\nrazdelimo na trikotnike.\nPoglejmo si petkotnik.",
        ).move_to(UP * 4.05)
        petkotnik = RegularPolygon(
            n=5, radius=2.3, color=UL_DARK, stroke_width=DEBELA
        ).rotate(PI / 2).move_to(UP * 0.8)
        oglisca = petkotnik.get_vertices()
        diagonali = VGroup(
            Line(oglisca[0], oglisca[2], color=UL_DARK, stroke_width=SREDNJA),
            Line(oglisca[0], oglisca[3], color=UL_DARK, stroke_width=SREDNJA),
        )
        trikotniki = [(0, 1, 2), (0, 2, 3), (0, 3, 4)]
        stevilke = VGroup()
        for i, indeksi in enumerate(trikotniki, start=1):
            sredina = np.mean([oglisca[j] for j in indeksi], axis=0)
            stevilke.add(self.txt(str(i), size=40, color=UL_DARK, weight="MEDIUM").move_to(sredina))
        # Trikotniki v barvah kotov α, β, γ: petkotnik se vizualno naveže na trikotnik.
        barve_trikotnikov = [UL_RED, UL_BLUE, UL_DARK]
        ploskve_trikotnikov = VGroup(*[
            Polygon(
                *[oglisca[j] for j in indeksi],
                color=UL_DARK,
                stroke_width=0,
                fill_color=barve_trikotnikov[i],
                fill_opacity=0.18,
            )
            for i, indeksi in enumerate(trikotniki)
        ])
        kosi = VGroup(*[
            VGroup(ploskve_trikotnikov[i], stevilke[i])
            for i in range(len(trikotniki))
        ])
        # Zakaj ravno toliko trikotnikov: iz izbranega oglišča ni diagonale do njega samega in do
        # obeh sosedov, zato ostane 5 − 3 diagonal, ki dajo 5 − 2 trikotnikov (pozneje splošno n).
        opis_sosedi = self.txt("Do sosednjih oglišč\nni diagonale.").move_to(DOWN * 2.6)
        stevec_diagonal = self.txt("5 − 3 = 2 diagonali", t2c={"5 − 3": UL_RED}).move_to(DOWN * 2.4)
        stevec_trikotnikov = self.txt("5 − 2 = 3 trikotniki", t2c={"5 − 2": UL_RED}).move_to(DOWN * 3.15)
        izbrano_oglisce = Dot(oglisca[0], radius=0.14, color=UL_RED).set_z_index(3)
        sosednji_oglisci = VGroup(*[Dot(oglisca[k], radius=0.11, color=UL_GRAY).set_z_index(3) for k in (1, 4)])
        opis_koti = self.txt("Koti trikotnikov skupaj\nzapolnijo kote petkotnika.").move_to(DOWN * 2.6)
        utemeljitev_pet = self.txt("Vsak trikotnik\nprispeva 180°.").move_to(DOWN * 2.75)

        def notranji_odsek(v, u, w, **kwargs):
            # Kot pri oglišču v med smerema proti u in w (manjši od iztegnjenega).
            z, k = smerni_kot(v, u), smerni_kot(v, w)
            razpon = (k - z) % TAU
            if razpon > PI:
                z, razpon = k, TAU - razpon
            return z, razpon

        # V izbranem oglišču se stikajo trije ozki koti, zato so tam narisani z večjim polmerom.
        def polmer_kota_pet(v, osnovni):
            return osnovni * 1.6 if np.allclose(v, oglisca[0]) else osnovni

        def kot_trikotnika(v, u, w, barva):
            z, razpon = notranji_odsek(v, u, w)
            return Sector(radius=polmer_kota_pet(v, 0.5), start_angle=z, angle=razpon, stroke_width=0,
                          fill_color=barva, fill_opacity=0.5).move_arc_center_to(v)

        # Trije koti vsakega trikotnika v barvi trikotnika.
        koti_trikotnikov = VGroup(*[
            VGroup(*[
                kot_trikotnika(oglisca[t[k]], oglisca[t[(k + 1) % 3]], oglisca[t[(k + 2) % 3]], barve_trikotnikov[i])
                for k in range(3)
            ])
            for i, t in enumerate(trikotniki)
        ])
        # Loki notranjih kotov petkotnika: barvni koščki pod vsakim lokom natanko zapolnijo kot.
        loki_petkotnika = VGroup(*[
            Arc(arc_center=oglisca[m], radius=polmer_kota_pet(oglisca[m], 0.62), color=UL_DARK, stroke_width=TANKA,
                start_angle=notranji_odsek(oglisca[m], oglisca[m - 1], oglisca[(m + 1) % 5])[0],
                angle=notranji_odsek(oglisca[m], oglisca[m - 1], oglisca[(m + 1) % 5])[1])
            for m in range(5)
        ])

        def val_kapljic(st, cas, zamik_vala=0.6, glasnost=-2):
            # Mehka kapljica ob začetku vsakega dela vala LaggedStart; toni se vzpenjajo.
            trajanje_kosa = cas / (1 + zamik_vala * (st - 1))
            for i in range(st):
                self.zvok("kapljica", zamik=i * zamik_vala * trajanje_kosa + 0.08, f=ton(2 * i), glasnost=glasnost)

        # Petkotnik se nariše umirjeno; vsaka stranica dobi svoj mehak vuš.
        self.zvok_risanja_lika(5, 1.6, seme=6)
        self.play(FadeIn(podvprasanje), Create(petkotnik), run_time=1.6)
        self.wait(1.2)  # čas za branje uvodnega besedila

        # Izberemo oglišče; sosednji oglišči sta z njim povezani že s stranicama.
        self.zvok("kapljica", f=ton(2))
        self.play(GrowFromCenter(izbrano_oglisce), FadeOut(podvprasanje), run_time=0.5)
        sosednji_stranici = VGroup(*[Line(oglisca[0], oglisca[k]) for k in (1, 4)])
        sosednji_stranici.set_stroke(UL_GRAY, width=DEBELA * 2, opacity=0)
        self.zvok("pok", f1=900, glasnost=-8)
        self.play(
            FadeIn(sosednji_oglisci, scale=0.5), FadeIn(opis_sosedi),
            sosednji_stranici.animate(rate_func=there_and_back).set_stroke(opacity=0.8),
            run_time=0.8,
        )
        self.remove(sosednji_stranici)
        self.wait(1.6)  # čas za branje: do sosedov ni diagonale

        # Diagonali do preostalih oglišč se narišeta druga za drugo; sproti se pokaže štetje.
        self.play(FadeOut(opis_sosedi), run_time=0.4)
        for i, diagonala in enumerate(diagonali):
            self.zvok_risanja(0.8, gladko=True, seme=16 + 3 * i)
            animacije = [Create(diagonala)]
            if i == 0:
                animacije.append(FadeIn(stevec_diagonal))
            self.play(*animacije, run_time=0.8)
        self.wait(0.3)
        # Trikotniki se obarvajo v tekočem valu (vsak se začne, preden prejšnji konča).
        val_kapljic(len(trikotniki), 1.8)
        self.play(
            LaggedStart(*[
                AnimationGroup(FadeIn(ploskve_trikotnikov[i]), FadeIn(stevilke[i], scale=0.5))
                for i in range(len(trikotniki))
            ], lag_ratio=0.6),
            FadeIn(stevec_trikotnikov),
            # Pike oglišč so opravile svoje: izginejo, da ne zakrivajo kotov v izbranem oglišču.
            FadeOut(izbrano_oglisce, sosednji_oglisci),
            run_time=1.8,
        )
        self.wait(1.8)  # čas za branje: 5 − 3 diagonali, 5 − 2 trikotniki

        # Ključni korak: koti trikotnikov skupaj sestavljajo kote petkotnika.
        val_kapljic(len(trikotniki), 1.6)
        self.play(
            LaggedStart(*[FadeIn(k, scale=0.6) for k in koti_trikotnikov], lag_ratio=0.6),
            Succession(FadeOut(stevec_diagonal, stevec_trikotnikov, run_time=0.4), FadeIn(opis_koti, run_time=0.6)),
            run_time=1.6,
        )
        self.zvok_risanja(1.0, gladko=True, seme=19)  # loki kotov petkotnika
        self.play(Create(loki_petkotnika), run_time=1.0)
        self.wait(2.4)  # čas za branje: koti trikotnikov zapolnijo kote petkotnika

        # Trikotnike (z njihovimi koti) ločimo iz petkotnika: vsak je samostojen trikotnik s 180°.
        for i in range(len(trikotniki)):
            kosi[i].add(koti_trikotnikov[i])
        for ploskev in ploskve_trikotnikov:
            ploskev.set_stroke(UL_DARK, width=SREDNJA, opacity=1)
        smer_desno = normalize(np.array([
            -(oglisca[2] - oglisca[0])[1],
            (oglisca[2] - oglisca[0])[0],
            0,
        ]))
        sredina_desnega = np.mean([oglisca[j] for j in trikotniki[0]], axis=0)
        if np.dot(smer_desno, sredina_desnega - oglisca[0]) < 0:
            smer_desno *= -1

        smer_levo = normalize(np.array([
            -(oglisca[3] - oglisca[0])[1],
            (oglisca[3] - oglisca[0])[0],
            0,
        ]))
        sredina_levga = np.mean([oglisca[j] for j in trikotniki[2]], axis=0)
        if np.dot(smer_levo, sredina_levga - oglisca[0]) < 0:
            smer_levo *= -1

        odmik_kosov = 0.45
        self.zvok_risanja(1.5, gladko=True, seme=11)  # trikotniki se mehko razmaknejo
        self.play(
            kosi[0].animate.shift(smer_desno * odmik_kosov),
            kosi[2].animate.shift(smer_levo * odmik_kosov),
            FadeOut(petkotnik, diagonali, loki_petkotnika, opis_koti),
            run_time=1.5,
        )
        self.play(FadeIn(utemeljitev_pet), run_time=0.6)
        self.wait(0.8)

        # 9. Konkretni izračun za petkotnik.
        racun_pet = self.mat("3 · 180° = 540°", size=58).move_to(DOWN * 3.95)
        self.zvok("zvoncek", zamik=0.9, glasnost=-6)  # rezultat 540°, ko je zapis dokončan
        self.play(Write(racun_pet), run_time=1.2)
        self.wait(1.6)  # čas za branje: 3 · 180° = 540°

        # 10. Število trikotnikov sledi vzorcu n - 2.
        vrstice_y = [2.9, 1.8, 0.7, -0.4]
        stevila_stranic = ["3", "4", "5", "6"]
        poimenovanja_stranic = ["stranice", "stranice", "stranic", "stranic"]
        stevila_trikotnikov = ["1", "2", "3", "4"]
        poimenovanja_trikotnikov = ["trikotnik", "trikotnika", "trikotniki", "trikotniki"]

        n_nadomestek = self.txt("n", color=UL_RED)
        n_minus_2_nadomestek = self.txt("n − 2", color=UL_RED)
        st_stranic = [self.txt(s) for s in stevila_stranic]
        besede_stranic = [self.txt(s) for s in poimenovanja_stranic]
        puscice = [
            Arrow(LEFT * 0.36, RIGHT * 0.36, buff=0, color=UL_DARK, stroke_width=TANKA,
                  tip_length=0.16, max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=10)
            for _ in vrstice_y
        ]
        st_trikotnikov = [self.txt(s) for s in stevila_trikotnikov]
        besede_trikotnikov = [self.txt(s) for s in poimenovanja_trikotnikov]
        # Ob splošnem n rodilnik množine, enako kot »n stranic«.
        beseda_trikotnikov_n = self.txt("trikotnikov")

        # Stolpce razporedimo glede na dejanske širine, da je tabela na sredini.
        razmik = 0.18
        razmik_puscice = 0.3
        sirina_st_1 = max(m.width for m in st_stranic + [n_nadomestek])
        sirina_besede_1 = max(m.width for m in besede_stranic)
        sirina_puscice = puscice[0].width
        sirina_st_2 = max(m.width for m in st_trikotnikov + [n_minus_2_nadomestek])
        sirina_besede_2 = max(m.width for m in besede_trikotnikov + [beseda_trikotnikov_n])
        skupna_sirina = (
            sirina_st_1 + razmik + sirina_besede_1 + razmik_puscice + sirina_puscice
            + razmik_puscice + sirina_st_2 + razmik + sirina_besede_2
        )
        x_st_1 = -skupna_sirina / 2 + sirina_st_1
        x_beseda_1 = x_st_1 + razmik
        x_puscica = x_beseda_1 + sirina_besede_1 + razmik_puscice + sirina_puscice / 2
        x_st_2 = x_puscica + sirina_puscice / 2 + razmik_puscice + sirina_st_2
        x_beseda_2 = x_st_2 + razmik

        def postavi_desno(obj, x, y):
            obj.move_to([x - obj.width / 2, y, 0])

        def postavi_levo(obj, x, y):
            obj.move_to([x + obj.width / 2, y, 0])

        pregled_vrstice = []
        for i, y in enumerate(vrstice_y):
            postavi_desno(st_stranic[i], x_st_1, y)
            postavi_levo(besede_stranic[i], x_beseda_1, y)
            # Puščica na višini sredine malih črk (ne sredine celotne vrstice).
            puscice[i].move_to([x_puscica, besede_stranic[i].get_bottom()[1] + 0.12, 0])
            postavi_desno(st_trikotnikov[i], x_st_2, y)
            postavi_levo(besede_trikotnikov[i], x_beseda_2, y)
            pregled_vrstice.append(
                VGroup(st_stranic[i], besede_stranic[i], puscice[i], st_trikotnikov[i], besede_trikotnikov[i])
            )
        pregled = VGroup(*pregled_vrstice)
        # Univerza Sans nima znakov ∈ in ℕ; zapis »n = 3, 4, 5, …« pove isto.
        domena_n = self.txt("n = 3, 4, 5, …").move_to(DOWN * 1.8)
        # Razlog iz petkotnika (5 − 3 diagonali, 5 − 2 trikotniki), zapisan splošno.
        razlog_n = self.txt(
            "Iz enega oglišča gre\nn − 3 diagonal, ki dajo\nn − 2 trikotnikov.",
            t2c={"n − 3": UL_RED, "n − 2": UL_RED},
        ).move_to(DOWN * 3.1)
        self.zvok("vetrc", trajanje=0.5, seme=12, glasnost=-10, akcija=True)
        self.play(FadeOut(VGroup(prehod, kosi, utemeljitev_pet, racun_pet)), run_time=0.5)
        naslov_vzorec = self.heading("OPAZIMO VZOREC")
        self.zvok("pok", f1=900)
        self.play(FadeIn(naslov_vzorec), run_time=0.4)
        # Vrstice v ritmu: najprej levi del, nato puščica in odgovor, da gledalec lahko ugiba.
        for i_vrstice, vrstica in enumerate(pregled_vrstice):
            self.zvok("pok", f1=1000, glasnost=-8)
            self.play(FadeIn(vrstica[:2], shift=RIGHT * 0.15), run_time=0.25)
            self.zvok("ksilofon", f=ton(i_vrstice + 1))
            self.play(FadeIn(vrstica[2:], shift=RIGHT * 0.15), run_time=0.3)
            self.wait(0.3)  # čas za branje vrstice
        postavi_desno(n_nadomestek, x_st_1, vrstice_y[3])
        postavi_desno(n_minus_2_nadomestek, x_st_2, vrstice_y[3])
        # Poravnava po osnovni črti: spodnji rob kot pri števkah, ki ju zamenjata.
        n_nadomestek.align_to(st_stranic[3], DOWN)
        n_minus_2_nadomestek.align_to(st_trikotnikov[3], DOWN)
        postavi_levo(beseda_trikotnikov_n, x_beseda_2, vrstice_y[3])
        beseda_trikotnikov_n.align_to(besede_trikotnikov[3], DOWN)
        self.wait(0.3)
        # Stari števki najprej izgineta, šele nato se pojavita n in n − 2, da se ne prekrivajo.
        self.play(
            FadeOut(st_stranic[3], shift=UP * 0.25),
            FadeOut(st_trikotnikov[3], shift=UP * 0.25),
            FadeOut(besede_trikotnikov[3], shift=UP * 0.25),
            run_time=0.3,
        )
        self.zvok("iskrice")  # 6 → n, 4 → n − 2
        self.play(
            FadeIn(n_nadomestek, shift=UP * 0.25),
            FadeIn(n_minus_2_nadomestek, shift=UP * 0.25),
            FadeIn(beseda_trikotnikov_n, shift=UP * 0.25),
            run_time=0.35,
        )
        # Zamenjani števki odstranimo iz tabele, sicer bi se med končnim FadeOut za hip spet pokazali.
        pregled_vrstice[3].remove(st_stranic[3], st_trikotnikov[3], besede_trikotnikov[3])
        self.zvok("pok", f1=1300, glasnost=-8)
        self.play(FadeIn(domena_n), run_time=0.4)
        self.wait(1.0)
        self.zvok("potrditev", glasnost=-4)  # razlog za vzorec
        self.play(FadeIn(razlog_n, shift=UP * 0.15), run_time=0.6)
        self.wait(3.0)  # čas za branje: vzorec n → n − 2 in razlog

        # 11. Posplošitev in končno pravilo.
        self.play(FadeOut(VGroup(naslov_vzorec, pregled, n_nadomestek, n_minus_2_nadomestek, beseda_trikotnikov_n, domena_n, razlog_n)), run_time=0.5)
        naslov_pravilo = self.heading("SPLOŠNO PRAVILO")

        # Lik, ki raste: začne se s trikotnikom z začetka videa, nato mu postopoma zrastejo
        # nova oglišča (štirikotnik, petkotnik, šestkotnik), pod formulo pa se sproti menja izračun.
        def tocka(x, y):
            return np.array([x, y, 0.0])

        # Oglišča imajo imena, da lahko sledimo, katera so nova. Vrstni red je v smeri urinega kazalca.
        oglisca_rasti = {
            "A": A, "B": B, "C": C,
            "D": tocka(-0.35, -3.25), "E": tocka(-2.75, 0.55), "F": tocka(2.65, 0.85),
        }
        # (novo oglišče, soseda, med katerima zraste)
        koraki_rasti = [("D", "C", "A"), ("E", "A", "B"), ("F", "B", "C")]
        # Barve kotov: trikotnik ohrani barve z začetka (α rdeč, γ siv, β moder);
        # vsak nov kot dobi svojo barvo iz sekundarne palete UL, da se vidi, da so vsi koti različni.
        barve_rasti = {"A": UL_RED, "B": UL_DARK, "C": UL_BLUE, "D": UL_GREEN, "E": UL_TURQUOISE, "F": UL_PINK}
        POLMER_RASTI = 0.55
        PROSOJNOST_DIAGONAL = 0.35  # diagonale (meje trikotnikov) so svetlejše od stranic lika

        # Vsi liki so preslikani enako, zato trikotnik raste na mestu.
        merilo_rasti = 0.64
        sredisce_rasti = tocka(-0.25, -0.65)  # središče okvirja šestkotnika
        polozaj_rasti = UP * 3.015

        def preslikaj(t):
            return (t - sredisce_rasti) * merilo_rasti + polozaj_rasti

        # Trenutno stanje lika, ki ga posodablja animacija rasti.
        polozaji = {ime: preslikaj(t) for ime, t in oglisca_rasti.items()}
        vrstni_red = ["A", "B", "C"]
        vidnost_kota = {}       # ime oglišča -> 0..1 (novi koti se postopoma pokažejo)
        vidnost_diagonale = {}  # ime oddaljenega oglišča -> 0..1
        vidnost_okrasa = ValueTracker(0.0)
        polmer_okrasa = ValueTracker(POLMER_RASTI)
        polnilo_okrasa = ValueTracker(0.3)

        def tocke_lika():
            return [polozaji[ime] for ime in vrstni_red]

        def diagonale_iz_A():
            # Vse diagonale iz oglišča A razdelijo lik na n − 2 trikotnikov.
            return vrstni_red[2:len(vrstni_red) - 1]

        def zgradi_okras():
            tocke = tocke_lika()
            n = len(tocke)
            skupaj = vidnost_okrasa.get_value()
            okras = VGroup()
            for ime in diagonale_iz_A():
                okras.add(Line(
                    polozaji["A"], polozaji[ime], color=UL_DARK, stroke_width=SREDNJA,
                    stroke_opacity=PROSOJNOST_DIAGONAL * skupaj * vidnost_diagonale.get(ime, 1.0),
                ))
            for k, ime in enumerate(vrstni_red):
                vrh, naslednje, prejsnje = tocke[k], tocke[(k + 1) % n], tocke[k - 1]
                zacetek = smerni_kot(vrh, prejsnje)
                razpon = max((smerni_kot(vrh, naslednje) - zacetek) % TAU, 1e-3)
                f = skupaj * vidnost_kota.get(ime, 1.0)
                polmer = polmer_okrasa.get_value()
                okras.add(
                    Sector(radius=polmer, start_angle=zacetek, angle=razpon, stroke_width=0,
                           fill_color=barve_rasti[ime], fill_opacity=polnilo_okrasa.get_value() * f).move_arc_center_to(vrh),
                    Arc(arc_center=vrh, radius=polmer, start_angle=zacetek, angle=razpon,
                        color=barve_rasti[ime], stroke_width=TANKA, stroke_opacity=f),
                )
            return okras

        okras_rasti = always_redraw(zgradi_okras)
        rastoci_lik = Polygon(*tocke_lika(), color=UL_DARK, stroke_width=DEBELA).set_z_index(1)

        def zrasti(novo, sosed_1, sosed_2):
            # Novo oglišče se izvleče iz sredine stranice med sosedoma; njegov kot in nova diagonala
            # se pri tem postopoma pokažeta.
            cilj = polozaji[novo].copy()
            zacetek = (polozaji[sosed_1] + polozaji[sosed_2]) / 2
            stare_diagonale = set(diagonale_iz_A())
            vrstni_red.insert(vrstni_red.index(sosed_1) + 1, novo)
            nove_diagonale = set(diagonale_iz_A()) - stare_diagonale

            def posodobi(lik, alfa):
                a = smooth(alfa)
                polozaji[novo] = zacetek + (cilj - zacetek) * a
                vidnost_kota[novo] = a
                for ime in nove_diagonale:
                    vidnost_diagonale[ime] = a
                tocke = tocke_lika()
                lik.set_points_as_corners([*tocke, tocke[0]])

            posodobi(rastoci_lik, 0)
            return UpdateFromAlphaFunc(rastoci_lik, posodobi)

        formula_splosno = self.mat("S = (n − 2) · 180°", size=66).move_to(UP * 0.31)

        def izracun(n):
            vsota = f"{(n - 2) * 180}°"
            return self.mat(f"n = {n}  →  S = {vsota}", size=48, color=UL_DARK, t2c={vsota: UL_RED}).move_to(DOWN * 0.95)

        trenutni_izracun = izracun(3)

        # Legenda: tri enakovredne vrstice v lahki pisavi, manjše od formule.
        legenda = self.txt(
            "S = vsota notranjih kotov\nn = število stranic\nn − 2 = število trikotnikov",
            razmik=1.25,
        ).move_to(DOWN * 2.75)
        izziv = self.txt("Izziv: koliko je vsota\nkotov v 10-kotniku?", t2c={"Izziv:": UL_RED}).move_to(DOWN * 2.75)

        self.add(okras_rasti)
        self.zvok("pok", f1=900)
        self.zvok_risanja_lika(3, 1.2, seme=7)  # trikotnik na zadnjem kadru: tri stranice
        self.play(
            FadeIn(naslov_pravilo),
            Create(rastoci_lik),
            Write(formula_splosno),
            FadeIn(trenutni_izracun),
            FadeIn(legenda),  # pomen črk je viden takoj, ko se pojavi formula
            run_time=1.2,
        )
        for i in range(3):
            self.zvok("pok", zamik=0.1 * i, f1=1000 + 250 * i)
        self.play(vidnost_okrasa.animate.set_value(1.0), run_time=0.4)
        self.wait(0.6)

        for n, (novo, sosed_1, sosed_2) in enumerate(koraki_rasti, start=4):
            nov_izracun = izracun(n)
            self.zvok("ksilofon", f=ton(n - 1))  # vsako novo oglišče je višja nota
            self.zvok("pok", zamik=0.4, f1=1100 + 200 * (n - 4), glasnost=-4)
            self.play(
                zrasti(novo, sosed_1, sosed_2),
                # Izračun zamenjamo v dveh korakih, da se števki ne prekrivata.
                Succession(
                    FadeOut(trenutni_izracun, shift=UP * 0.2, run_time=0.2),
                    FadeIn(nov_izracun, shift=UP * 0.2, run_time=0.3),
                ),
                run_time=0.5,
            )
            trenutni_izracun = nov_izracun
            self.wait(0.4)

        self.wait(2.2)  # čas za branje: končno pravilo in legenda
        # Izziv za gledalca (spodbuda za komentarje).
        self.zvok("pok", f1=1200, glasnost=-8)
        self.play(FadeOut(legenda), run_time=0.4)
        self.play(FadeIn(izziv, shift=UP * 0.15), run_time=0.5)
        self.wait(3.0)  # čas za razmislek: (10 − 2) · 180° = 1440°

        # 12. Vrnitev v prvi kader: lik se skrči nazaj v trikotnik, ta se vrne na začetno mesto
        # in velikost, nato izgine. Zadnja sličica je tako enaka prvi in video na Instagramu
        # (ki teče v zanki) se brez skoka začne znova.
        def skrci(staro, sosed_1, sosed_2):
            # Obratno od zrasti: oglišče se vrne na sredino stranice, njegov kot in diagonala izgineta.
            zacetek = polozaji[staro].copy()
            cilj = (polozaji[sosed_1] + polozaji[sosed_2]) / 2
            ostala = [ime for ime in vrstni_red if ime != staro]
            izginjajoce = set(diagonale_iz_A()) - set(ostala[2:len(ostala) - 1])

            def posodobi(lik, alfa):
                a = smooth(alfa)
                polozaji[staro] = zacetek + (cilj - zacetek) * a
                vidnost_kota[staro] = 1 - a
                for ime in izginjajoce:
                    vidnost_diagonale[ime] = 1 - a
                tocke = tocke_lika()
                lik.set_points_as_corners([*tocke, tocke[0]])

            return UpdateFromAlphaFunc(rastoci_lik, posodobi)

        koraki_nazaj = [("F", "B", "C"), ("E", "A", "B"), ("D", "C", "A")]
        self.zvok("drsenje", f0=1200, f1=300, trajanje=1.2, glasnost=-8, akcija=True)  # »previjanje nazaj«
        for i, (staro, sosed_1, sosed_2) in enumerate(koraki_nazaj):
            self.zvok("ksilofon", f=ton(5 - i), glasnost=-3, akcija=True)  # note se spuščajo
            animacije = [skrci(staro, sosed_1, sosed_2)]
            if i == 0:
                animacije.append(FadeOut(formula_splosno, trenutni_izracun, izziv))
            self.play(*animacije, run_time=0.35)
            vrstni_red.remove(staro)
            vidnost_diagonale.clear()
            tocke = tocke_lika()
            rastoci_lik.set_points_as_corners([*tocke, tocke[0]])

        # Trikotnik se vrne na mesto in v velikost iz prvega kadra; naslov in uvod sta enaka kot na začetku.
        zacetni_polozaji = {ime: polozaji[ime].copy() for ime in ("A", "B", "C")}
        koncni_polozaji = {"A": A, "B": B, "C": C}

        def vrni_na_zacetek(lik, alfa):
            a = smooth(alfa)
            for ime in ("A", "B", "C"):
                polozaji[ime] = zacetni_polozaji[ime] + (koncni_polozaji[ime] - zacetni_polozaji[ime]) * a
            tocke = tocke_lika()
            lik.set_points_as_corners([*tocke, tocke[0]])

        naslov_zacetek = self.heading("VSOTA NOTRANJIH KOTOV\nV TRIKOTNIKU")
        uvod_zacetek = self.txt("Vsak trikotnik ima 180°.\nAmpak zakaj?", t2c={"Ampak zakaj?": UL_RED}).move_to(UP * 3.8)
        self.zvok("vetrc", trajanje=1.0, seme=14, glasnost=-6, akcija=True)
        self.zvok("pok", zamik=0.9, f1=900)
        self.play(
            UpdateFromAlphaFunc(rastoci_lik, vrni_na_zacetek),
            polmer_okrasa.animate.set_value(polmer_kota),
            polnilo_okrasa.animate.set_value(0.18),
            # Naslova se ne prekrivata: stari najprej izgine, nato se pokaže začetni.
            Succession(
                FadeOut(naslov_pravilo, run_time=0.35),
                FadeIn(naslov_zacetek, uvod_zacetek, run_time=0.65),
            ),
            run_time=1.0,
        )
        # Pojavijo se še oznake kotov: zadnja sličica je enaka prvi (naslov, vprašanje, trikotnik s koti).
        zacetna_skica = skica_trikotnika(A, B, C)
        self.play(FadeIn(zacetna_skica["alpha_dol"], zacetna_skica["beta_dol"], zacetna_skica["gamma_dol"]), run_time=0.5)
        # Rastoči lik (mnogokotnik z okrasom) zamenjamo z enakimi predmeti kot v prvi sličici
        # (tri stranice, odseki, loki), da se tudi stiki stranic v ogliščih ujemajo do piksla.
        self.remove(rastoci_lik, okras_rasti, *[zacetna_skica[k] for k in ("alpha_dol", "beta_dol", "gamma_dol")])
        self.add(*zacetna_skica.values())
        self.wait(0.5)

# Allows VS Code's "Run Python File" button to render a preview.
if __name__ == "__main__":
    with tempconfig({
        "quality": "high_quality",
        "preview": False,
        "pixel_width": 1080,
        "pixel_height": 1920,
        "frame_width": 9,
        "frame_height": 16,
        "frame_rate": 30,
    }):
        VsotaKotov().render()
