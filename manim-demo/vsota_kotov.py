from manim import *
import numpy as np


# Pokončni format za TikTok/Instagram.
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30

# Barvna zasnova po osnovnih elementih CGP UL: rdeča, sivi toni
# in ena sekundarna barva. Arial je nadomestna pisava, kadar Univerza Sans
# ni nameščena.
UL_RED = "#E03127"
UL_DARK = "#252525"
UL_GRAY = "#58595B"
UL_LIGHT = "#E6E7E8"
UL_BLUE = "#2878AC"
BG = "#FAFAF8"

config.background_color = BG


class VsotaKotov(Scene):
    def txt(self, text, size=30, color=UL_DARK, **kwargs):
        return Text(text, font="Arial", font_size=size, color=color, **kwargs)

    def heading(self, text, y=6.55):
        return self.txt(text, size=36, color=UL_RED, weight=BOLD).scale_to_fit_width(8.2).move_to(UP * y)

    def construct(self):
        # 1. Prvi frame: bolj grandiozen uvod z res poljubnim trikotnikom.
        naslov = self.heading("VSOTA NOTRANJIH KOTOV")

        # Nepravilen, vendar uravnotežen trikotnik brez pretirano ostrega vrha.
        A1 = np.array([-2.8, -1.5, 0])
        B1 = np.array([0.3, 2.5, 0])
        C1 = np.array([2.7, -1.3, 0])
        trikotnik_1 = Polygon(A1, B1, C1, color=UL_DARK, stroke_width=7)

        # Oznake ležijo na notranjih simetralah kotov, blizu posameznih oglišč.
        simetrala_A1 = normalize(normalize(B1 - A1) + normalize(C1 - A1))
        simetrala_B1 = normalize(normalize(A1 - B1) + normalize(C1 - B1))
        simetrala_C1 = normalize(normalize(A1 - C1) + normalize(B1 - C1))
        alpha_1 = MathTex(r"\alpha", color=UL_RED).scale(1.2).move_to(A1 + simetrala_A1 * 0.72)
        beta_1 = MathTex(r"\beta", color=UL_DARK).scale(1.2).move_to(B1 + simetrala_B1 * 0.72)
        gamma_1 = MathTex(r"\gamma", color=UL_BLUE).scale(1.2).move_to(C1 + simetrala_C1 * 0.72)

        self.play(FadeIn(naslov), Create(trikotnik_1), FadeIn(alpha_1, beta_1, gamma_1), run_time=1.6)
        self.wait(1.0)
        self.play(FadeOut(naslov, trikotnik_1, alpha_1, beta_1, gamma_1), run_time=1.0)
        self.wait(0.2)

        # 2. Drugi frame: trikotnik nastane iz štirih premic.
        p = Line([-3.8, -2.1, 0], [3.8, -2.1, 0], color=UL_BLUE, stroke_width=5)
        pp = Line([-3.8, 2.6, 0], [3.8, 2.6, 0], color=UL_BLUE, stroke_width=5)
        T = np.array([0.0, 2.6, 0])
        r = Line([-2.9, -2.1, 0], T, color=UL_DARK, stroke_width=5)
        q = Line([2.6, -2.1, 0], T, color=UL_DARK, stroke_width=5)

        A2 = np.array([-2.9, -2.1, 0])
        B2 = np.array([0.0, 2.6, 0])
        C2 = np.array([2.6, -2.1, 0])
        trikotnik_2 = Polygon(A2, B2, C2, color=UL_DARK, stroke_width=6)

        oznaka_p = self.txt("p", size=28, color=UL_BLUE).move_to([3.7, -1.7, 0])
        oznaka_pp = self.txt("p′", size=28, color=UL_BLUE).move_to([3.55, 2.95, 0])
        oznaka_r = self.txt("r", size=28, color=UL_DARK).move_to([-2.1, 0.9, 0])
        oznaka_q = self.txt("q", size=28, color=UL_DARK).move_to([1.65, 0.8, 0])

        alpha_dir = normalize((B2 - A2) + (C2 - A2))
        beta_dir = normalize((A2 - B2) + (C2 - B2))
        gamma_dir = normalize((A2 - C2) + (B2 - C2))

        alpha_dol = MathTex(r"\alpha", color=UL_RED).scale(1.05).move_to(A2 + alpha_dir * 0.9)
        beta_dol = MathTex(r"\beta", color=UL_DARK).scale(1.05).move_to(B2 + beta_dir * 0.9)
        gamma_dol = MathTex(r"\gamma", color=UL_BLUE).scale(1.05).move_to(C2 + gamma_dir * 0.9)

        alpha_vrh = MathTex(r"\alpha", color=UL_RED).scale(0.9).move_to([-1.2, 1.8, 0])
        beta_vrh = MathTex(r"\beta", color=UL_DARK).scale(0.9).move_to([0.18, 0.95, 0])
        gamma_vrh = MathTex(r"\gamma", color=UL_BLUE).scale(0.9).move_to([1.35, 1.8, 0])
        size_lok = 1.5


        alpha_lok = ArcBetweenPoints(
            start=A2 + normalize(C2 - A2) * size_lok,
            end=A2 + normalize(B2 - A2) * size_lok,
            radius=size_lok,
            color=UL_RED,
            stroke_width=4,
        )
        beta_lok = ArcBetweenPoints(
            start=B2 + normalize(A2 - B2) * size_lok,
            end=B2 + normalize(C2 - B2) * size_lok,
            radius=size_lok,
            color=UL_DARK,
            stroke_width=4,
        )
        gamma_lok = ArcBetweenPoints(
            start=C2 + normalize(B2 - C2) * size_lok,
            end=C2 + normalize(A2 - C2) * size_lok,
            radius=size_lok,
            color=UL_BLUE,
            stroke_width=4,
        )

        self.play(Create(p), Create(pp), Create(r), Create(q), FadeIn(oznaka_p, oznaka_pp, oznaka_r, oznaka_q), run_time=1.6)
        self.play(Create(trikotnik_2), FadeIn(alpha_dol, beta_dol, gamma_dol, alpha_lok, beta_lok, gamma_lok), run_time=1.1)
        self.wait(0.6)

        vprasanje = self.txt(
            "Koliko skupaj merijo koti\nv poljubnem trikotniku?",
            size=31,
            line_spacing=0.9,
        ).move_to(UP * 4.75)
        self.play(FadeIn(vprasanje), run_time=1.1)
        self.wait(1.8)

        # 3. Frame: fokus na premici p, p′ in r; primerjamo kot α z novokonstruiranim α.
        self.play(
            trikotnik_2.animate.set_opacity(0.10),
            q.animate.set_opacity(0.12),
            gamma_dol.animate.set_opacity(0.0),
            beta_dol.animate.set_opacity(1.0),
            #beta_vrh.animate.set_opacity(1.0),
            gamma_vrh.animate.set_opacity(0.0),
            oznaka_q.animate.set_opacity(0.15),
            oznaka_p.animate.set_opacity(0.6),
            oznaka_pp.animate.set_opacity(0.6),
            oznaka_r.animate.set_opacity(1.0),
            run_time=1.2,
        )

        razlaga_alpha = self.txt(
            "Ker je p ∥ p′, sta izmenična kota enaka.", size=24
        ).move_to(DOWN * 3.0)
        self.play(Indicate(alpha_dol, color=UL_RED), FadeIn(alpha_vrh), FadeIn(razlaga_alpha), run_time=1.2)
        self.wait(2.0)

        # 4. Frame: fokus na premici p, p′ in q; primerjamo kot γ z novokonstruiranim γ.
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            r.animate.set_opacity(0.12),
            oznaka_r.animate.set_opacity(0.12),
            q.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(1.0),
            trikotnik_2.animate.set_opacity(0.18),
            alpha_dol.animate.set_opacity(0.12),
            alpha_vrh.animate.set_opacity(0.12),
            beta_dol.animate.set_opacity(1.0),
            #beta_vrh.animate.set_opacity(1.0),
            gamma_dol.animate.set_opacity(1.0),
            gamma_vrh.animate.set_opacity(1.0),
            run_time=1.2,
        )
        self.wait(0.6)
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            r.animate.set_opacity(1.0),
            oznaka_r.animate.set_opacity(1.0),
            q.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(1.0),
            trikotnik_2.animate.set_opacity(0.18),
            alpha_dol.animate.set_opacity(1.0),
            alpha_vrh.animate.set_opacity(1.0),
            beta_dol.animate.set_opacity(1.0),
            gamma_dol.animate.set_opacity(1.0),
            gamma_vrh.animate.set_opacity(1.0),
            run_time=1.4,
        )

        razlaga_gamma = self.txt(
            "Enako velja za kota γ.", size=24
        ).move_to(DOWN * 3.5)
        self.play(Indicate(gamma_dol, color=UL_BLUE), FadeIn(gamma_vrh), FadeIn(razlaga_gamma), run_time=1.2)
        self.wait(2.0)

        # 5. Trije koti ob vrhu B ležijo na premici p.
        sklep = self.txt("Koti na premici sestavijo iztegnjeni kot.", size=24).move_to(DOWN * 4.0)
        formula_trikotnik = MathTex(
            r"\alpha+\beta+\gamma=180^\circ", color=UL_RED
        ).scale(1.05).move_to(DOWN * 5.0)
        self.play(
            FadeIn(sklep),
            FadeIn(beta_dol, beta_vrh),
            Write(formula_trikotnik),
            run_time=2.2,
        )



        dokazna_skupina = VGroup(
            trikotnik_2, alpha_dol, beta_dol, gamma_dol,
            alpha_lok, beta_lok, gamma_lok,
            p, pp, r, q, oznaka_p, oznaka_pp, oznaka_r, oznaka_q,
            alpha_vrh, beta_vrh, gamma_vrh, razlaga_alpha,
            razlaga_gamma, sklep, formula_trikotnik, vprasanje,
        )
        self.play(FadeOut(dokazna_skupina), run_time=0.7)
        self.wait(0.4)

        # 7. Prehod: isto idejo uporabimo pri večkotniku.
        prehod = self.heading("KAJ PA VEČKOTNIK?")
        podvprasanje = self.txt(
            "Ali lahko tudi njegove kote\nrazdelimo na trikotnike?",
            size=36,
            line_spacing=0.9,
            weight=BOLD,
            color=UL_DARK,
        ).move_to(UP * 2.35)

        self.play(
            FadeIn(prehod, scale=1.02),
            FadeIn(podvprasanje, scale=1.03),
            run_time=1.1,
        )
        self.wait(2.0)
        self.play(
            FadeOut(prehod, podvprasanje),
            run_time=0.9,
        )

        # 8. Petkotnik razdelimo na tri trikotnike.
        naslov_pet = self.heading("PETKOTNIK RAZDELIMO NA TRIKOTNIKE")
        petkotnik = RegularPolygon(
            n=5, radius=1.9, color=UL_DARK, stroke_width=6
        ).rotate(PI / 2).move_to(UP * 0.9)
        oglisca = petkotnik.get_vertices()
        diagonali = VGroup(
            Line(oglisca[0], oglisca[2], color=UL_BLUE, stroke_width=5),
            Line(oglisca[0], oglisca[3], color=UL_BLUE, stroke_width=5),
        )
        trikotniki = [(0, 1, 2), (0, 2, 3), (0, 3, 4)]
        stevilke = VGroup()
        for i, indeksi in enumerate(trikotniki, start=1):
            sredina = np.mean([oglisca[j] for j in indeksi], axis=0)
            stevilke.add(self.txt(str(i), size=32, color=UL_RED, weight=BOLD).move_to(sredina))
        opis_pet = self.txt("Diagonali ustvarita 3 trikotnike.", size=26).move_to(DOWN * 2.0)
        utemeljitev_pet = self.txt("Vsak prispeva 180°.", size=24, color=UL_GRAY).move_to(DOWN * 2.65)

        self.play(FadeIn(naslov_pet), Create(petkotnik), run_time=1.0)
        self.play(Create(diagonali), FadeIn(stevilke), run_time=1.0)
        self.play(FadeIn(opis_pet, utemeljitev_pet), run_time=0.4)
        self.wait(2.8)

        # 9. Konkretni izračun za petkotnik.
        racun_pet = MathTex(r"3\cdot180^\circ=540^\circ", color=UL_RED).scale(1.2)
        racun_pet.move_to(DOWN * 3.75)
        self.play(Write(racun_pet), run_time=0.8)
        self.wait(2.2)

        # 10. Število trikotnikov sledi vzorcu n - 2.
        pregled = VGroup(
            self.txt("3 stranice  →  1 trikotnik", size=27),
            self.txt("4 stranice  →  2 trikotnika", size=27),
            self.txt("5 stranic      →  3 trikotniki", size=27),
            self.txt("6 stranic      →  4 trikotniki", size=27),
        ).arrange(DOWN, buff=0.48).move_to(UP * 1.35)
        posplositev = MathTex(r"n\text{-kotnik}\;\longrightarrow\;n-2\text{ trikotnikov}", color=UL_BLUE).scale(0.8)
        posplositev.move_to(DOWN * 2.0)
        self.play(FadeOut(VGroup(naslov_pet, petkotnik, diagonali, stevilke, opis_pet,
                                 utemeljitev_pet, racun_pet)), run_time=0.8)
        naslov_vzorec = self.heading("OPAZIMO VZOREC")
        self.play(FadeIn(naslov_vzorec), FadeIn(pregled), Write(posplositev), run_time=1.0)
        self.wait(2.3)

        # 11. Posplošitev in končno pravilo.
        self.play(FadeOut(VGroup(naslov_vzorec, pregled, posplositev)), run_time=0.8)
        naslov_pravilo = self.heading("SPLOŠNO PRAVILO")
        formula_splosno = MathTex(r"S=(n-2)\cdot180^\circ", color=UL_RED).scale(1.35)
        formula_splosno.move_to(UP * 1.25)
        pomen_S = self.txt("S = vsota notranjih kotov", size=27).move_to(DOWN * 0.5)
        pomen_n = self.txt("n = število stranic", size=27, color=UL_GRAY).move_to(DOWN * 1.35)
        zakljucek = self.txt("n − 2 je število trikotnikov.", size=25, color=UL_BLUE).move_to(DOWN * 2.55)
        self.play(FadeIn(naslov_pravilo), Write(formula_splosno), run_time=1.0)
        self.play(FadeIn(pomen_S, pomen_n, zakljucek), run_time=0.6)
        self.wait(1.5)


# Allows VS Code's "Run Python File" button to render a preview.
if __name__ == "__main__":
    with tempconfig({
        "quality": "low_quality",
        "preview": True,
        "pixel_width": 540,
        "pixel_height": 960,
        "frame_width": 9,
        "frame_height": 16,
        "frame_rate": 30,
    }):
        VsotaKotov().render()
