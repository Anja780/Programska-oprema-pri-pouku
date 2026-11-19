from manim import *
from manimpango import register_font
import numpy as np
from pathlib import Path


# Pokončni format za TikTok/Instagram.
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30

# Pisave Univerza Sans so vključene v projekt in registrirane za ta izris.
PROJEKT = Path(__file__).parent
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
UL_BLUE = "#2878AC"  # sinjemodra: edina sekundarna barva, samo za kot β
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


class VsotaKotov(Scene):
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

    def dashed_segment(self, start, end, color=UL_GRAY, stroke_width=SREDNJA, dash_length=0.18, gap_length=0.12):
        start = np.array(start, dtype=float)
        end = np.array(end, dtype=float)
        vec = end - start
        total = np.linalg.norm(vec)
        if total < 1e-8:
            return VGroup()
        direction = vec / total
        segments = []
        travelled = 0.0
        while travelled + dash_length < total - 1e-8:
            seg_start = start + direction * travelled
            seg_end = start + direction * (travelled + dash_length)
            segments.append(Line(seg_start, seg_end, color=color, stroke_width=stroke_width))
            travelled += dash_length + gap_length
        if travelled < total:
            seg_start = start + direction * travelled
            seg_end = end
            segments.append(Line(seg_start, seg_end, color=color, stroke_width=stroke_width))
        return VGroup(*segments)

    def construct(self):
        # 1. Prvi frame: poljuben trikotnik, na katerem nato izpeljemo še dokaz.
        naslov = self.heading("VSOTA NOTRANJIH KOTOV\nV TRIKOTNIKU")

        # Nepravilen trikotnik z rahlo nagnjeno osnovnico. Desni del ostane levo od
        # stolpca gumbov Instagrama (x < 3,25 v spodnji polovici zaslona).
        A = np.array([-3.25, -2.45, 0])
        B = np.array([0.1, 1.95, 0])
        C = np.array([2.75, -1.8, 0])
        stranica_AB = Line(A, B, color=UL_DARK, stroke_width=DEBELA)
        stranica_BC = Line(B, C, color=UL_DARK, stroke_width=DEBELA)
        stranica_CA = Line(C, A, color=UL_DARK, stroke_width=DEBELA)

        # Trikotnik se nadaljuje v kratke črtkane vodilne črte v sivi 40 %.
        dolzina_raztega = 0.42
        odmik_od_oglisc = 0.16
        smer_AB = normalize(B - A)
        smer_BC = normalize(C - B)
        smer_CA = normalize(A - C)
        beta_extension_from_B = self.dashed_segment(B - smer_BC * (odmik_od_oglisc + dolzina_raztega), B - smer_BC * odmik_od_oglisc)
        gamma_extension_from_C = self.dashed_segment(C + smer_BC * odmik_od_oglisc, C + smer_BC * (odmik_od_oglisc + dolzina_raztega))
        gamma_right_extension = self.dashed_segment(C - smer_CA * (odmik_od_oglisc + dolzina_raztega), C - smer_CA * odmik_od_oglisc)
        left_base = self.dashed_segment(A - smer_AB * (odmik_od_oglisc + dolzina_raztega), A - smer_AB * odmik_od_oglisc)
        right_base = self.dashed_segment(B + smer_AB * odmik_od_oglisc, B + smer_AB * (odmik_od_oglisc + dolzina_raztega))
        left_side = self.dashed_segment(A + smer_CA * odmik_od_oglisc, A + smer_CA * (odmik_od_oglisc + dolzina_raztega))
        dashed_guides_1 = VGroup(left_base, right_base, left_side, gamma_right_extension, beta_extension_from_B, gamma_extension_from_C)

        polmer_kota = 1.25
        odmik_oznake = 0.8
        VELIKOST_OZNAKE_KOTA = 40

        # Oznake ležijo na notranjih simetralah kotov, blizu posameznih oglišč.
        def simetrala(vrh, krak_1, krak_2):
            return normalize(normalize(krak_1 - vrh) + normalize(krak_2 - vrh))

        alpha_dol = self.mat("α", size=VELIKOST_OZNAKE_KOTA, color=UL_RED).move_to(A + simetrala(A, B, C) * odmik_oznake)
        # Oznaki sta zamenjani: kot pri B (siv, zgoraj) je γ, kot pri C (moder, spodaj desno) je β.
        # Imena spremenljivk beta_* / gamma_* še vedno označujejo kot pri B oz. C.
        beta_dol = self.mat("γ", size=VELIKOST_OZNAKE_KOTA, color=UL_DARK).move_to(B + simetrala(B, A, C) * odmik_oznake)
        gamma_dol = self.mat("β", size=VELIKOST_OZNAKE_KOTA, color=UL_BLUE).move_to(C + simetrala(C, A, B) * odmik_oznake)

        # Besedilo zgoraj (pod naslovom) in spodaj, nad območjem opisa na Instagramu.
        uvod_1 = self.txt("Oglejmo si\npoljuben trikotnik.").move_to(UP * 3.8)
        uvod_2 = self.txt("V trikotniku so trije\nnotranji koti: α, β in γ.").move_to(DOWN * 3.25)
        vzporednica_txt = self.txt("Skozi zgornje oglišče\nnarišemo vzporednico p′\nk osnovnici.").move_to(DOWN * 3.42)

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

        def odsek(vrh, zacetni_kot, koncni_kot, barva):
            return Sector(
                radius=polmer_kota,
                start_angle=zacetni_kot,
                angle=(koncni_kot - zacetni_kot) % TAU,
                color=barva,
                fill_opacity=0.18,
                stroke_width=0,
            ).move_arc_center_to(vrh)

        ang_A_to_B = smerni_kot(A, B)
        ang_A_to_C = smerni_kot(A, C)
        ang_B_to_A = smerni_kot(B, A)
        ang_B_to_C = smerni_kot(B, C)
        ang_C_to_A = smerni_kot(C, A)
        ang_C_to_B = smerni_kot(C, B)

        alpha_lok = lok(A, ang_A_to_C, ang_A_to_B, UL_RED)
        alpha_odsek = odsek(A, ang_A_to_C, ang_A_to_B, UL_RED)
        beta_lok = lok(B, ang_B_to_A, ang_B_to_C, UL_DARK)
        beta_odsek = odsek(B, ang_B_to_A, ang_B_to_C, UL_DARK)
        gamma_lok = lok(C, ang_C_to_B, ang_C_to_A, UL_BLUE)
        gamma_odsek = odsek(C, ang_C_to_B, ang_C_to_A, UL_BLUE)

        # Trikotnik s črtkanimi podaljški se izriše v treh sekundah. Vsaka premica je ena
        # neprekinjena poteza z enakomerno hitrostjo: črtkani del, stranica, črtkani del.
        # Presledki (med črticami in ob ogliščih) so časovno upoštevani, kot da pero potuje čeznje.
        poteze = [
            [left_base, stranica_AB, right_base],
            [beta_extension_from_B, stranica_BC, gamma_extension_from_C],
            [gamma_right_extension, stranica_CA, left_side],
        ]

        def koraki_poteze(deli):
            # Seznam (črta ali None za presledek, dolžina) v vrstnem redu risanja.
            crte = []
            for del_poteze in deli:
                crte.extend(del_poteze if isinstance(del_poteze, VGroup) else [del_poteze])
            koraki = []
            for i, crta in enumerate(crte):
                if i > 0:
                    koraki.append((None, np.linalg.norm(crta.get_start() - crte[i - 1].get_end())))
                koraki.append((crta, crta.get_length()))
            return koraki

        cas_risanja = 3.0
        vsi_koraki = [koraki_poteze(deli) for deli in poteze]
        hitrost = sum(dolzina for koraki in vsi_koraki for _, dolzina in koraki) / cas_risanja
        risanje = Succession(*[
            Create(crta, rate_func=linear, run_time=dolzina / hitrost)
            if crta is not None else Wait(run_time=dolzina / hitrost)
            for koraki in vsi_koraki
            for crta, dolzina in koraki
        ])
        # Naslov je viden že v prvi sličici (predogled na Instagramu ni prazen).
        self.add(naslov, uvod_1)
        self.play(risanje)
        self.play(
            FadeIn(alpha_lok, beta_lok, gamma_lok, alpha_odsek, beta_odsek, gamma_odsek, alpha_dol, beta_dol, gamma_dol),
            FadeIn(uvod_2),
            run_time=0.8,
        )
        self.wait(0.8)

        # 2. Stranice istega trikotnika podaljšamo v premice r, q in p ter osnovnici dodamo vzporednico p′.
        # Premice so pomožne (tanjše); stranice trikotnika ostanejo debele, da je trikotnik ves čas viden.
        podaljsek = 0.5
        smer_p = normalize(C - A)
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
        oznaka_r = self.txt("r", size=OZNAKE).move_to((A + B) / 2 + normala_navzven(smer_AB, A) * 0.5)
        oznaka_q = self.txt("q", size=OZNAKE).move_to((B + C) / 2 + normala_navzven(smer_BC, C) * 0.5)

        self.add(r_crta, q_crta, p_crta)
        self.play(
            r_crta.animate.put_start_and_end_on(*r_konca),
            q_crta.animate.put_start_and_end_on(*q_konca),
            p_crta.animate.put_start_and_end_on(p_konca[1], p_konca[0]),
            FadeOut(dashed_guides_1),
            FadeOut(uvod_2),
            run_time=1.4,
        )
        # Premica skupaj s pripadajočo stranico (za zatemnjevanje in prikaz).
        r = VGroup(r_crta, stranica_AB)
        q = VGroup(q_crta, stranica_BC)
        p = VGroup(p_crta, stranica_CA)
        self.play(FadeIn(oznaka_p, oznaka_r, oznaka_q), run_time=0.4)
        self.play(FadeIn(vzporednica_txt), Create(pp), FadeIn(oznaka_pp), run_time=1.2)
        self.wait(0.7)

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

        ZATEMNJENO = 0.25

        # 3. Frame: fokus na premici p, p′ in r; primerjamo kot α z novokonstruiranim α.
        # Uvodno besedilo izgine v isti potezi, ko se q umakne v ozadje.
        self.play(
            FadeOut(naslov, uvod_1, vzporednica_txt),
            q.animate.set_opacity(ZATEMNJENO),
            gamma_dol.animate.set_opacity(0.0),
            gamma_lok.animate.set_stroke(opacity=0.0),
            beta_dol.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(ZATEMNJENO),
            oznaka_p.animate.set_opacity(0.6),
            oznaka_pp.animate.set_opacity(0.6),
            oznaka_r.animate.set_opacity(1.0),
            run_time=0.8,
        )

        razlaga_alpha_1 = self.txt("Ker sta p in p′ vzporedni,\nsta izmenična kota\nob premici r enaka.").move_to(UP * 4.3)
        razlaga_alpha_2 = self.txt("Torej je zgornji kot\nenak spodnjemu.").move_to(DOWN * 3.25)
        self.play(Indicate(alpha_vrh, color=UL_RED), FadeIn(alpha_vrh), FadeIn(razlaga_alpha_1, razlaga_alpha_2), run_time=1.2)
        self.wait(1.6)
        self.play(prenesi_kot(alpha_odsek, zasuk_alpha, A, B), run_time=1.5)
        self.wait(0.6)

        # 4. Frame: fokus na premici p, p′ in q; primerjamo kot β z novokonstruiranim β.
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            r.animate.set_opacity(ZATEMNJENO),
            oznaka_r.animate.set_opacity(ZATEMNJENO),
            q.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(1.0),
            alpha_dol.animate.set_opacity(ZATEMNJENO),
            alpha_lok.animate.set_stroke(opacity=ZATEMNJENO),
            alpha_vrh.animate.set_opacity(ZATEMNJENO),
            beta_dol.animate.set_opacity(1.0),
            gamma_dol.animate.set_opacity(1.0),
            gamma_lok.animate.set_stroke(opacity=1.0),
            FadeOut(razlaga_alpha_1, razlaga_alpha_2),
            run_time=1.2,
        )
        razlaga_gamma_1 = self.txt("Enako velja tudi\nza drugi par kotov.").move_to(UP * 4.3)
        self.play(
            prenesi_kot(gamma_odsek, zasuk_gamma, C, B),
            FadeIn(gamma_vrh),
            FadeIn(razlaga_gamma_1),
            run_time=2.2,
        )
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            r.animate.set_opacity(1.0),
            oznaka_r.animate.set_opacity(1.0),
            q.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(1.0),
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
        zatemnjene_oznake = VGroup(oznaka_p, oznaka_pp, oznaka_r, oznaka_q, alpha_dol, gamma_dol)
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
        self.play(preteceni_kot.animate.set_value(180), run_time=2.4, rate_func=smooth)
        for mobjekt in (alpha_odsek, beta_odsek, gamma_odsek, stevec, kazalec, konica_kazalca):
            mobjekt.clear_updaters()
        self.remove(drsni_lok)
        polkrog_obroba = Arc(arc_center=B, radius=polmer_kota, start_angle=ang_C_to_A, angle=PI, color=UL_DARK, stroke_width=TANKA)
        self.add(polkrog_obroba)

        # Kratek poudarek na končni vrednosti; kazalec, ki je obšel ravni kot, izgine.
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
        self.play(
            stevec.animate.scale_to_fit_height(stevilo_v_formuli.height).move_to(stevilo_v_formuli),
            TransformFromCopy(alpha_vrh, formula_trikotnik[0]),
            TransformFromCopy(gamma_vrh, formula_trikotnik[2]),
            TransformFromCopy(beta_dol, formula_trikotnik[4]),
            FadeIn(formula_trikotnik[1], formula_trikotnik[3], formula_trikotnik[5]),
            zatemnjene_crte.animate.set_opacity(1.0),
            zatemnjene_oznake.animate.set_opacity(1.0),
            zatemnjeni_loki.animate.set_stroke(opacity=1.0),
            FadeOut(ravna_crta),
            Succession(FadeOut(sklep_1, run_time=0.5), FadeIn(sklep_2, run_time=0.8)),
            run_time=1.3,
        )
        self.remove(stevec)
        self.add(stevilo_v_formuli)
        self.wait(1.8)

        final_proof_group = VGroup(
            alpha_dol, beta_dol, gamma_dol,
            alpha_lok, alpha_odsek, beta_lok, beta_odsek, gamma_lok, gamma_odsek,
            alpha_vrh, alpha_vrh_lok, gamma_vrh, gamma_vrh_lok,
            p, pp, r, q,
            oznaka_p, oznaka_pp, oznaka_r, oznaka_q,
            polkrog_obroba,
            sklep_2, formula_trikotnik,
        )
        # 7. Prehod: isto idejo uporabimo pri večkotniku. Vprašanje se pojavi že med izginjanjem trikotnika.
        prehod = self.heading("KAJ PA VEČKOTNIK?")
        self.play(FadeOut(final_proof_group), FadeIn(prehod), run_time=0.8)
        self.remove(*[m for m in self.mobjects if m is not prehod])
        podvprasanje = self.txt(
            "Konveksni večkotnik lahko\nrazdelimo na trikotnike.\nPoglejmo si petkotnik.",
        ).move_to(UP * 4.0)
        petkotnik = RegularPolygon(
            n=5, radius=2.3, color=UL_DARK, stroke_width=DEBELA
        ).rotate(PI / 2).move_to(UP * 0.65)
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
        opis_pet = self.txt("Diagonali iz enega oglišča\nustvarita 3 trikotnike.").move_to(DOWN * 2.35)
        utemeljitev_pet = self.txt("Vsak prispeva 180°.", size=OZNAKE, weight="LIGHT").move_to(DOWN * 3.35)

        self.play(FadeIn(podvprasanje), Create(petkotnik), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(kosi), Create(diagonali), run_time=1.0)
        self.wait(1.5)  # čas za branje uvodnega besedila ob že razdeljenem petkotniku
        self.play(FadeOut(podvprasanje), FadeIn(opis_pet, utemeljitev_pet), run_time=0.6)
        self.wait(1.4)

        # Trikotnike ločimo iz petkotnika in jih pokažemo kot tri samostojne kose.
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
        self.play(
            kosi[0].animate.shift(smer_desno * odmik_kosov),
            kosi[2].animate.shift(smer_levo * odmik_kosov),
            FadeOut(petkotnik, diagonali, opis_pet, utemeljitev_pet),
            run_time=1.2,
        )

        # 9. Konkretni izračun za petkotnik.
        racun_pet = self.mat("3 · 180° = 540°", size=58).move_to(DOWN * 2.9)
        self.play(Write(racun_pet), run_time=0.8)
        self.wait(0.8)

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

        # Stolpce razporedimo glede na dejanske širine, da je tabela na sredini.
        razmik = 0.18
        razmik_puscice = 0.3
        sirina_st_1 = max(m.width for m in st_stranic + [n_nadomestek])
        sirina_besede_1 = max(m.width for m in besede_stranic)
        sirina_puscice = puscice[0].width
        sirina_st_2 = max(m.width for m in st_trikotnikov + [n_minus_2_nadomestek])
        sirina_besede_2 = max(m.width for m in besede_trikotnikov)
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
        domena_n = self.txt("n = 3, 4, 5, …", size=OZNAKE, weight="LIGHT").move_to(DOWN * 1.8)
        self.play(FadeOut(VGroup(prehod, kosi, racun_pet)), run_time=0.5)
        naslov_vzorec = self.heading("OPAZIMO VZOREC")
        self.play(FadeIn(naslov_vzorec), run_time=0.4)
        # Vrstice v ritmu: najprej levi del, nato puščica in odgovor, da gledalec lahko ugiba.
        for vrstica in pregled_vrstice:
            self.play(FadeIn(vrstica[:2], shift=RIGHT * 0.15), run_time=0.25)
            self.play(FadeIn(vrstica[2:], shift=RIGHT * 0.15), run_time=0.3)
        postavi_desno(n_nadomestek, x_st_1, vrstice_y[3])
        postavi_desno(n_minus_2_nadomestek, x_st_2, vrstice_y[3])
        # Poravnava po osnovni črti: spodnji rob kot pri števkah, ki ju zamenjata.
        n_nadomestek.align_to(st_stranic[3], DOWN)
        n_minus_2_nadomestek.align_to(st_trikotnikov[3], DOWN)
        self.wait(0.3)
        # Stari števki najprej izgineta, šele nato se pojavita n in n − 2, da se ne prekrivajo.
        self.play(
            FadeOut(st_stranic[3], shift=UP * 0.25),
            FadeOut(st_trikotnikov[3], shift=UP * 0.25),
            run_time=0.3,
        )
        self.play(
            FadeIn(n_nadomestek, shift=UP * 0.25),
            FadeIn(n_minus_2_nadomestek, shift=UP * 0.25),
            run_time=0.35,
        )
        # Zamenjani števki odstranimo iz tabele, sicer bi se med končnim FadeOut za hip spet pokazali.
        pregled_vrstice[3].remove(st_stranic[3], st_trikotnikov[3])
        self.play(FadeIn(domena_n), run_time=0.4)
        self.wait(1.6)

        # 11. Posplošitev in končno pravilo.
        self.play(FadeOut(VGroup(naslov_vzorec, pregled, n_nadomestek, n_minus_2_nadomestek, domena_n)), run_time=0.5)
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
        # nova oglišča dobijo barvo, ki se razlikuje od obeh sosedov.
        barve_rasti = {"A": UL_RED, "B": UL_DARK, "C": UL_BLUE, "D": UL_DARK, "E": UL_BLUE, "F": UL_RED}
        POLMER_RASTI = 0.55
        PROSOJNOST_DIAGONAL = 0.35  # diagonale (meje trikotnikov) so svetlejše od stranic lika

        # Vsi liki so preslikani enako, zato trikotnik raste na mestu.
        merilo_rasti = 0.6
        sredisce_rasti = tocka(-0.25, -0.65)  # središče okvirja šestkotnika
        polozaj_rasti = UP * 3.3

        def preslikaj(t):
            return (t - sredisce_rasti) * merilo_rasti + polozaj_rasti

        # Trenutno stanje lika, ki ga posodablja animacija rasti.
        polozaji = {ime: preslikaj(t) for ime, t in oglisca_rasti.items()}
        vrstni_red = ["A", "B", "C"]
        vidnost_kota = {}       # ime oglišča -> 0..1 (novi koti se postopoma pokažejo)
        vidnost_diagonale = {}  # ime oddaljenega oglišča -> 0..1
        vidnost_okrasa = ValueTracker(0.0)

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
                okras.add(
                    Sector(radius=POLMER_RASTI, start_angle=zacetek, angle=razpon, stroke_width=0,
                           fill_color=barve_rasti[ime], fill_opacity=0.3 * f).move_arc_center_to(vrh),
                    Arc(arc_center=vrh, radius=POLMER_RASTI, start_angle=zacetek, angle=razpon,
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

        formula_splosno = self.mat("S = (n − 2) · 180°", size=66).move_to(UP * 0.75)

        def izracun(n):
            vsota = f"{(n - 2) * 180}°"
            return self.mat(f"n = {n}  →  S = {vsota}", size=48, color=UL_DARK, t2c={vsota: UL_RED}).move_to(DOWN * 0.4)

        trenutni_izracun = izracun(3)

        # Legenda: tri enakovredne vrstice v lahki pisavi, manjše od formule.
        legenda = self.txt(
            "S = vsota notranjih kotov\nn = število stranic\nn − 2 = število trikotnikov",
            size=OZNAKE,
            razmik=1.25,
            weight="LIGHT",
        ).move_to(DOWN * 2.05)

        self.add(okras_rasti)
        self.play(
            FadeIn(naslov_pravilo),
            Create(rastoci_lik),
            Write(formula_splosno),
            FadeIn(trenutni_izracun),
            run_time=1.2,
        )
        self.play(vidnost_okrasa.animate.set_value(1.0), run_time=0.4)
        self.wait(0.6)

        for n, (novo, sosed_1, sosed_2) in enumerate(koraki_rasti, start=4):
            nov_izracun = izracun(n)
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

        self.play(FadeIn(legenda), run_time=0.6)
        self.wait(2.0)

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
