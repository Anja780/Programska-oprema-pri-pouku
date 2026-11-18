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
FONT_DIR = Path(__file__).parent / "Univerza Sans TTF 0"
for font_file in FONT_DIR.glob("*.ttf"):
    register_font(str(font_file))

# Barvna zasnova po barvni shemi UL: rdeča, antracit in ena sekundarna barva.
UL_RED = "#E03127"
UL_DARK = "#58595B"
UL_GRAY = "#58595B"
UL_LIGHT = "#E6E7E8"
UL_BLUE = "#2878AC"
BG = "#F4F3ED"

config.background_color = BG


class VsotaKotov(Scene):
    def txt(self, text, size=30, color=UL_DARK, **kwargs):
        text_mobject = Text(text, font="Univerza Sans", font_size=size, color=color, **kwargs)
        max_width = config.frame_width - 0.8
        if text_mobject.width > max_width:
            text_mobject.scale_to_fit_width(max_width)
        return text_mobject

    def heading(self, text, y=6.55):
        return self.txt(text, size=36, color=UL_RED, weight=BOLD).scale_to_fit_width(8.2).move_to(UP * y)

    def build_parallel_guides(self, base_y=-2.1, top_y=2.9):
        p = Line([-3.8, base_y, 0], [3.8, base_y, 0], color=UL_BLUE, stroke_width=5)
        pp = Line([-3.8, top_y, 0], [3.8, top_y, 0], color=UL_BLUE, stroke_width=5)
        return p, pp

    def line_intersection(self, line1, line2):
        p1 = np.array(line1.get_start())
        p2 = np.array(line1.get_end())
        p3 = np.array(line2.get_start())
        p4 = np.array(line2.get_end())

        den = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
        if abs(den) < 1e-8:
            return None

        x = ((p1[0] * p2[1] - p1[1] * p2[0]) * (p3[0] - p4[0]) - (p1[0] - p2[0]) * (p3[0] * p4[1] - p3[1] * p4[0])) / den
        y = ((p1[0] * p2[1] - p1[1] * p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] * p4[1] - p3[1] * p4[0])) / den
        return np.array([x, y, 0.0])

    def build_triangle_from_lines(self, p, pp, r, q):
        A2 = self.line_intersection(p, r)
        C2 = self.line_intersection(p, q)
        B2 = self.line_intersection(r, q)
        return A2, B2, C2, r, q

    def dashed_segment(self, start, end, color=UL_DARK, stroke_width=4.0, dash_length=0.18, gap_length=0.12):
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
        # 1. Prvi frame: bolj grandiozen uvod z res poljubnim trikotnikom.
        naslov = self.heading("Vsota notranjih kotov v trikotniku")

        # Nepravilen, vendar uravnotežen trikotnik brez pretirano ostrega vrha.
        A1 = np.array([-2.8, -1.5, 0])
        B1 = np.array([0.3, 2.5, 0])
        C1 = np.array([2.7, -1.3, 0])
        stranica_AB = Line(A1, B1, color=UL_DARK, stroke_width=7)
        stranica_BC = Line(B1, C1, color=UL_DARK, stroke_width=7)
        stranica_CA = Line(C1, A1, color=UL_DARK, stroke_width=7)
        trikotnik_1 = VGroup(stranica_AB, stranica_BC, stranica_CA)

        # Trikotnik se nadaljuje v krajše, bolj vidne črtkane vodilne črte, kot na referenci.
        dolzina_raztega = 0.8
        odmik_od_oglisc = 0.16
        smer_AB = normalize(B1 - A1)
        smer_BC = normalize(C1 - B1)
        smer_CA = normalize(A1 - C1)
        beta_extension_from_B = self.dashed_segment(B1 - smer_BC * (odmik_od_oglisc + dolzina_raztega), B1 - smer_BC * odmik_od_oglisc, color=UL_DARK, stroke_width=4.0, dash_length=0.18, gap_length=0.12)
        gamma_extension_from_C = self.dashed_segment(C1 + smer_BC * odmik_od_oglisc, C1 + smer_BC * (odmik_od_oglisc + dolzina_raztega), color=UL_DARK, stroke_width=4.0, dash_length=0.18, gap_length=0.12)
        gamma_right_extension = self.dashed_segment(C1 - smer_CA * (odmik_od_oglisc + dolzina_raztega), C1 - smer_CA * odmik_od_oglisc, color=UL_DARK, stroke_width=4.0, dash_length=0.18, gap_length=0.12)
        left_base = self.dashed_segment(A1 - smer_AB * (odmik_od_oglisc + dolzina_raztega), A1 - smer_AB * odmik_od_oglisc, color=UL_DARK, stroke_width=4.0, dash_length=0.18, gap_length=0.12)
        right_base = self.dashed_segment(B1 + smer_AB * odmik_od_oglisc, B1 + smer_AB * (odmik_od_oglisc + dolzina_raztega), color=UL_DARK, stroke_width=4.0, dash_length=0.18, gap_length=0.12)
        left_side = self.dashed_segment(A1 + smer_CA * odmik_od_oglisc, A1 + smer_CA * (odmik_od_oglisc + dolzina_raztega), color=UL_DARK, stroke_width=4.0, dash_length=0.18, gap_length=0.12)
        dashed_guides_1 = VGroup(left_base, right_base, left_side, gamma_right_extension, beta_extension_from_B, gamma_extension_from_C)

        # Oznake ležijo na notranjih simetralah kotov, blizu posameznih oglišč.
        simetrala_A1 = normalize(normalize(B1 - A1) + normalize(C1 - A1))
        simetrala_B1 = normalize(normalize(A1 - B1) + normalize(C1 - B1))
        simetrala_C1 = normalize(normalize(A1 - C1) + normalize(B1 - C1))
        alpha_1 = MathTex(r"\alpha", color=UL_RED).scale(1.2).move_to(A1 + simetrala_A1 * 0.72)
        beta_1 = MathTex(r"\beta", color=UL_DARK).scale(1.2).move_to(B1 + simetrala_B1 * 0.72)
        gamma_1 = MathTex(r"\gamma", color=UL_BLUE).scale(1.2).move_to(C1 + simetrala_C1 * 0.72)
        uvod_1 = self.txt("Oglejmo si poljuben trikotnik.", size=28, color=UL_DARK).move_to(UP * 4.8)
        uvod_2 = self.txt("V trikotniku so trije notranji koti: α, β in γ.", size=26, color=UL_DARK).move_to(UP * 3.9)

        ang_A1_to_B = np.arctan2(B1[1] - A1[1], B1[0] - A1[0])
        ang_A1_to_C = np.arctan2(C1[1] - A1[1], C1[0] - A1[0])
        ang_B1_to_A = np.arctan2(A1[1] - B1[1], A1[0] - B1[0])
        ang_B1_to_C = np.arctan2(C1[1] - B1[1], C1[0] - B1[0])
        ang_C1_to_A = np.arctan2(A1[1] - C1[1], A1[0] - C1[0])
        ang_C1_to_B = np.arctan2(B1[1] - C1[1], B1[0] - C1[0])

        alpha_1_lok = Arc(
            arc_center=A1,
            start_angle=ang_A1_to_C,
            angle=(ang_A1_to_B - ang_A1_to_C) % (2 * np.pi),
            color=UL_RED,
            radius=1.15,
            stroke_width=2.0,
        )
        alpha_1_odsek = Sector(
            radius=1.15,
            start_angle=ang_A1_to_C,
            angle=(ang_A1_to_B - ang_A1_to_C) % (2 * np.pi),
            color=UL_RED,
            fill_opacity=0.18,
            stroke_width=0,
        ).move_arc_center_to(A1)
        beta_1_lok = Arc(
            arc_center=B1,
            start_angle=ang_B1_to_A,
            angle=(ang_B1_to_C - ang_B1_to_A) % (2 * np.pi),
            color=UL_DARK,
            radius=1.15,
            stroke_width=2.0,
        )
        beta_1_odsek = Sector(
            radius=1.15,
            start_angle=ang_B1_to_A,
            angle=(ang_B1_to_C - ang_B1_to_A) % (2 * np.pi),
            color=UL_DARK,
            fill_opacity=0.18,
            stroke_width=0,
        ).move_arc_center_to(B1)
        gamma_1_lok = Arc(
            arc_center=C1,
            start_angle=ang_C1_to_B,
            angle=(ang_C1_to_A - ang_C1_to_B) % (2 * np.pi),
            color=UL_BLUE,
            radius=1.15,
            stroke_width=2.0,
        )
        gamma_1_odsek = Sector(
            radius=1.15,
            start_angle=ang_C1_to_B,
            angle=(ang_C1_to_A - ang_C1_to_B) % (2 * np.pi),
            color=UL_BLUE,
            fill_opacity=0.18,
            stroke_width=0,
        ).move_arc_center_to(C1)

        self.play(FadeIn(naslov, uvod_1, uvod_2), run_time=0.8)
        self.play(Create(left_base), run_time=0.35)
        self.play(Create(stranica_AB), run_time=0.55)
        self.play(Create(right_base), run_time=0.35)
        self.play(Create(beta_extension_from_B), run_time=0.35)
        self.play(Create(stranica_BC), run_time=0.55)
        self.play(Create(gamma_extension_from_C), run_time=0.35)
        self.play(Create(gamma_right_extension), run_time=0.35)
        self.play(Create(stranica_CA), run_time=0.55)
        self.play(Create(left_side), run_time=0.35)
        self.play(FadeIn(alpha_1_lok, beta_1_lok, gamma_1_lok, alpha_1_odsek, beta_1_odsek, gamma_1_odsek, alpha_1, beta_1, gamma_1), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(naslov, trikotnik_1, dashed_guides_1, alpha_1_lok, beta_1_lok, gamma_1_lok, alpha_1_odsek, beta_1_odsek, gamma_1_odsek, alpha_1, beta_1, gamma_1, uvod_1, uvod_2), run_time=1.6)
        self.wait(0.4)

        # 2. Drugi frame: trikotnik nastane iz štirih premic.
        p = Line([-3.8, -2.1, 0], [3.8, -2.1, 0], color=UL_BLUE, stroke_width=5)
        # p′ mora spet potekati skozi isti vrh, kjer se sekata r in q.
        r = Line([-3.8, -2.5, 0], [1.6, 3.5, 0], color=UL_DARK, stroke_width=5)
        q = Line([4.0, -2.7, 0], [0.5, 3.3, 0], color=UL_DARK, stroke_width=5)
        A2, B2, C2, r, q = self.build_triangle_from_lines(p, Line([-3.8, 0, 0], [3.8, 0, 0], color=UL_BLUE, stroke_width=5), r, q)
        pp = Line([-3.8, B2[1], 0], [3.8, B2[1], 0], color=UL_BLUE, stroke_width=5)

        # Oznake so tik ob ustreznih premicah, na zunanji strani trikotnika.
        oznaka_p = self.txt("p", size=28, color=UL_BLUE).move_to([3.35, -2.48, 0])
        oznaka_pp = self.txt("p′", size=28, color=UL_BLUE).move_to([3.35, 3.28, 0])

        r_vec = np.array(r.get_end()) - np.array(r.get_start())
        q_vec = np.array(q.get_end()) - np.array(q.get_start())
        r_normal = np.array([-r_vec[1], r_vec[0], 0.0])
        q_normal = np.array([-q_vec[1], q_vec[0], 0.0])
        r_normal = r_normal / np.linalg.norm(r_normal)
        q_normal = q_normal / np.linalg.norm(q_normal)

        # q naj bo desno od premice q; r ostane na "zgornji" strani svoje premice.
        q_label_offset = q_normal * 0.9 if q_normal[0] > 0 else -q_normal * 0.9
        oznaka_r = self.txt("r", size=28, color=UL_DARK).move_to((np.array(r.get_start()) + np.array(r.get_end())) / 2 + r_normal * 0.55)
        oznaka_q = self.txt("q", size=28, color=UL_DARK).move_to((np.array(q.get_start()) + np.array(q.get_end())) / 2 + q_label_offset)

        alpha_dir = normalize((B2 - A2) + (C2 - A2))
        beta_dir = normalize((A2 - B2) + (C2 - B2))
        gamma_dir = normalize((A2 - C2) + (B2 - C2))

        alpha_dol = MathTex(r"\alpha", color=UL_RED).scale(1.05).move_to(A2 + alpha_dir * 0.9)
        beta_dol = MathTex(r"\beta", color=UL_DARK).scale(1.05).move_to(B2 + beta_dir * 0.9)
        gamma_dol = MathTex(r"\gamma", color=UL_BLUE).scale(1.05).move_to(C2 + gamma_dir * 0.9)

        alpha_vrh = MathTex(r"\alpha", color=UL_RED).scale(1.05).move_to(
            B2 + normalize((A2 - B2) + (np.array([-3.8, pp.get_start()[1], 0]) - B2)) * 0.9
        )
        gamma_vrh = MathTex(r"\gamma", color=UL_BLUE).scale(1.05).move_to(
            B2 + normalize((C2 - B2) + (np.array([3.8, pp.get_start()[1], 0]) - B2)) * 0.9
        )
        size_lok = 1.5


        ang_A_to_B = np.arctan2(B2[1] - A2[1], B2[0] - A2[0])
        ang_A_to_C = np.arctan2(C2[1] - A2[1], C2[0] - A2[0])
        ang_B_to_A = np.arctan2(A2[1] - B2[1], A2[0] - B2[0])
        ang_B_to_C = np.arctan2(C2[1] - B2[1], C2[0] - B2[0])
        ang_C_to_A = np.arctan2(A2[1] - C2[1], A2[0] - C2[0])
        ang_C_to_B = np.arctan2(B2[1] - C2[1], B2[0] - C2[0])

        alpha_lok = Arc(
            arc_center=A2,
            start_angle=ang_A_to_C,
            angle=(ang_A_to_B - ang_A_to_C) % (2 * np.pi),
            color=UL_RED,
            radius=size_lok,
            stroke_width=1.5,
        )
        alpha_odsek = Sector(
            radius=size_lok,
            start_angle=ang_A_to_C,
            angle=(ang_A_to_B - ang_A_to_C) % (2 * np.pi),
            color=UL_RED,
            fill_opacity=0.3,
            stroke_width=0,
        ).move_arc_center_to(A2)
        beta_lok = Arc(
            arc_center=B2,
            radius=size_lok,
            start_angle=ang_B_to_A,
            angle=(ang_B_to_C - ang_B_to_A) % (2 * np.pi),
            color=UL_DARK,
            stroke_width=1.5,
        )
        beta_odsek = Sector(
            radius=size_lok,
            start_angle=ang_B_to_A,
            angle=(ang_B_to_C - ang_B_to_A) % (2 * np.pi),
            color=UL_DARK,
            fill_opacity=0.3,
            stroke_width=0,
        ).move_arc_center_to(B2)
        gamma_lok = Arc(
            arc_center=C2,
            radius=size_lok,
            start_angle=ang_C_to_B,
            angle=(ang_C_to_A - ang_C_to_B) % (2 * np.pi),
            color=UL_BLUE,
            stroke_width=1.5,
        )
        gamma_odsek = Sector(
            radius=size_lok,
            start_angle=ang_C_to_B,
            angle=(ang_C_to_A - ang_C_to_B) % (2 * np.pi),
            color=UL_BLUE,
            fill_opacity=0.3,
            stroke_width=0,
        ).move_arc_center_to(C2)
        alpha_vrh_dir = np.array([-3.8, pp.get_start()[1], 0])
        gamma_vrh_dir = np.array([3.8, pp.get_start()[1], 0])
        ang_B_to_alpha_vrh = np.arctan2(alpha_vrh_dir[1] - B2[1], alpha_vrh_dir[0] - B2[0])
        ang_B_to_gamma_vrh = np.arctan2(gamma_vrh_dir[1] - B2[1], gamma_vrh_dir[0] - B2[0])
        zasuk_alpha = ang_B_to_alpha_vrh - ang_A_to_C
        zasuk_gamma = ang_B_to_C - ang_C_to_B
        alpha_vrh_lok = Arc(
            arc_center=B2,
            radius=size_lok,
            start_angle=ang_B_to_alpha_vrh,
            angle=(ang_B_to_A - ang_B_to_alpha_vrh) % (2 * np.pi),
            color=UL_RED,
            stroke_width=1.5,
        ).set_opacity(0)
        gamma_vrh_lok = Arc(
            arc_center=B2,
            radius=size_lok,
            start_angle=ang_B_to_C,
            angle=(ang_B_to_gamma_vrh - ang_B_to_C) % (2 * np.pi),
            color=UL_BLUE,
            stroke_width=1.5,
        ).set_opacity(0)

        skica = VGroup(
            p, pp, r, q,
            oznaka_p, oznaka_pp, oznaka_r, oznaka_q,
            alpha_dol, beta_dol, gamma_dol,
            alpha_lok, beta_lok, gamma_lok,
            alpha_odsek, beta_odsek, gamma_odsek,
            alpha_vrh, gamma_vrh, alpha_vrh_lok, gamma_vrh_lok,
        )
        skica_center = skica.get_center()
        skica_scale = 0.82
        skica_position = ORIGIN + DOWN * 0.2
        skica.scale(skica_scale).move_to(skica_position)

        # Animacije kotov morajo uporabljati koordinate po enakem skaliranju
        # in premiku kot skica; A2, B2 in C2 so še vedno v prvotnem koordinatnem sistemu.
        def skica_point(point):
            return skica_position + skica_scale * (point - skica_center)

        A2_prikaz = skica_point(A2)
        B2_prikaz = skica_point(B2)
        C2_prikaz = skica_point(C2)

        konstrukcija_1 = self.txt("Narišimo dve vzporedni premici p in p′.", size=24, color=UL_DARK).move_to(UP * 4.8)
        konstrukcija_2 = self.txt("Sekajmo ju z dvema premicama r in q.", size=24, color=UL_DARK).move_to(UP * 4.1)
        self.play(Create(p), Create(pp), Create(r), Create(q), FadeIn(oznaka_p, oznaka_pp, oznaka_r, oznaka_q), FadeIn(konstrukcija_1, konstrukcija_2), run_time=1.9)
        self.play(FadeIn(alpha_dol, beta_dol, gamma_dol, alpha_lok, beta_lok, gamma_lok), run_time=1.3)
        self.wait(1.0)
        self.play(FadeIn(alpha_odsek, beta_odsek, gamma_odsek), run_time=1.0)
        self.play(FadeOut(konstrukcija_1, konstrukcija_2), run_time=0.8)

        # 3. Frame: fokus na premici p, p′ in r; primerjamo kot α z novokonstruiranim α.
        self.play(
            q.animate.set_opacity(0.12),
            gamma_dol.animate.set_opacity(0.0),
            gamma_lok.animate.set_opacity(0.0),
            beta_dol.animate.set_opacity(1.0),
            #beta_lok.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(0.15),
            oznaka_p.animate.set_opacity(0.6),
            oznaka_pp.animate.set_opacity(0.6),
            oznaka_r.animate.set_opacity(1.0),
            run_time=0.8,
        )

        razlaga_alpha_1 = self.txt(
            "Ker sta p in p′ vzporedni, sta izmenična kota enaka.", size=24
        ).move_to(UP * 4.75)
        razlaga_alpha_2 = self.txt(
            "Torej je zgornji kot enak spodnjemu.", size=24
        ).move_to(UP * 3.75)
        self.play(Indicate(alpha_vrh, color=UL_RED), FadeIn(alpha_vrh), FadeIn(razlaga_alpha_1, razlaga_alpha_2), run_time=1.5)
        self.wait(1.8)
        self.play(
            Rotate(alpha_odsek, angle=zasuk_alpha, about_point=A2_prikaz),
            run_time=1.2,
        )
        self.play(
            alpha_odsek.animate.shift(B2_prikaz - A2_prikaz),
            FadeIn(alpha_vrh_lok),
            run_time=1.2,
        )
        self.wait(1.8)

        # 4. Frame: fokus na premici p, p′ in q; primerjamo kot γ z novokonstruiranim γ.
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            r.animate.set_opacity(0.12),
            oznaka_r.animate.set_opacity(0.12),
            q.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(1.0),
            alpha_dol.animate.set_opacity(0.12),
            alpha_lok.animate.set_opacity(0.12),
            alpha_vrh.animate.set_opacity(0.12),
            beta_dol.animate.set_opacity(1.0),
            #beta_lok.animate.set_opacity(1.0),
            gamma_dol.animate.set_opacity(1.0),
            gamma_lok.animate.set_opacity(0.5),
            run_time=1.2,
        )
        self.wait(0.6)
        razlaga_gamma_1 = self.txt(
            "Enako velja tudi za drugi par kotov.", size=24
        ).move_to(UP * 4.75)
        self.play(FadeOut(razlaga_alpha_1, razlaga_alpha_2), run_time=0.7)
        self.play(Indicate(gamma_dol, color=UL_BLUE), FadeIn(gamma_vrh), FadeIn(razlaga_gamma_1), run_time=1.5)
        self.play(
            Rotate(gamma_odsek, angle=zasuk_gamma, about_point=C2_prikaz),
            run_time=1.2,
        )
        self.play(
            gamma_odsek.animate.shift(B2_prikaz - C2_prikaz),
            FadeIn(gamma_vrh_lok),
            run_time=1.2,
        )
        self.play(
            p.animate.set_opacity(1.0),
            pp.animate.set_opacity(1.0),
            r.animate.set_opacity(1.0),
            oznaka_r.animate.set_opacity(1.0),
            q.animate.set_opacity(1.0),
            oznaka_q.animate.set_opacity(1.0),
            alpha_dol.animate.set_opacity(1.0),
            alpha_lok.animate.set_opacity(0.5),
            alpha_vrh.animate.set_opacity(1.0),
            alpha_vrh_lok.animate.set_opacity(1.0),
            beta_dol.animate.set_opacity(1.0),
            #beta_lok.animate.set_opacity(1.0),
            gamma_dol.animate.set_opacity(1.0),
            gamma_lok.animate.set_opacity(0.5),
            gamma_vrh.animate.set_opacity(1.0),
            gamma_vrh_lok.animate.set_opacity(1.0),
            run_time=1.4,
        )
        self.play(FadeOut(razlaga_gamma_1), run_time=0.7)

        sklep_1 = self.txt("Če se koti zložijo skupaj, dobimo ravni kot.", size=24, color=UL_DARK).move_to(UP * 5.0)
        formula_trikotnik = MathTex(
            r"\alpha+\beta+\gamma=180^\circ", color=UL_RED
        ).scale(1.05).move_to(DOWN * 3.9)
        sklep_2 = self.txt("Vsota notranjih kotov v trikotniku je 180°.", size=28, color=UL_DARK).move_to(DOWN * 5.1)
        self.play(
            alpha_lok.animate.set_opacity(1.0),
            beta_lok.animate.set_opacity(1.0),
            gamma_lok.animate.set_opacity(1.0),
            FadeIn(sklep_1),
            Write(formula_trikotnik),
            FadeIn(sklep_2),
            run_time=3.0,
        )
        self.wait(1.7)

        final_proof_group = VGroup(
            alpha_dol, beta_dol, gamma_dol,
            alpha_lok, alpha_odsek, beta_lok, beta_odsek, gamma_lok, gamma_odsek,
            alpha_vrh, alpha_vrh_lok, gamma_vrh, gamma_vrh_lok,
            p, pp, r, q,
            oznaka_p, oznaka_pp, oznaka_r, oznaka_q,
            sklep_1, sklep_2, formula_trikotnik,
        )
        self.play(FadeOut(final_proof_group), run_time=1.2)
        self.wait(0.5)
        self.clear()

        # 7. Prehod: isto idejo uporabimo pri večkotniku.
        prehod = self.heading("KAJ PA VEČKOTNIK?")
        naslov_pet = self.heading("PETKOTNIK RAZDELIMO NA TRIKOTNIKE")
        podvprasanje = self.txt(
            "Konveksni večkotnik lahko\nrazdelimo na trikotnike.\nPoglejmo si petkotnik.",
            size=28,
            line_spacing=0.9,
            weight=BOLD,
            color=UL_DARK,
        ).move_to(UP * 3.65)
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
        barve_trikotnikov = [UL_RED, UL_BLUE, UL_LIGHT]
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
        opis_pet = self.txt("Diagonali ustvarita 3 trikotnike.", size=26).move_to(DOWN * 2.0)
        utemeljitev_pet = self.txt("Vsak prispeva 180°.", size=24, color=UL_GRAY).move_to(DOWN * 2.65)

        self.play(
            FadeIn(prehod),
            FadeIn(podvprasanje),
            Create(petkotnik),
            run_time=1.5,
        )
        self.wait(0.35)
        self.play(
            FadeIn(kosi),
            Create(diagonali),
            run_time=1.1,
        )
        self.play(
            ReplacementTransform(prehod, naslov_pet),
            FadeOut(podvprasanje),
            run_time=0.8,
        )
        self.play(FadeIn(opis_pet, utemeljitev_pet), run_time=0.4)
        self.wait(2.4)

        # Trikotnike ločimo iz petkotnika in jih pokažemo kot tri samostojne kose.
        for ploskev in ploskve_trikotnikov:
            ploskev.set_stroke(UL_DARK, width=5, opacity=1)
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

        odmik_kosov = 0.38
        self.play(
            kosi[0].animate.shift(smer_desno * odmik_kosov),
            kosi[2].animate.shift(smer_levo * odmik_kosov),
            FadeOut(petkotnik, diagonali, opis_pet, utemeljitev_pet),
            run_time=1.5,
        )
        self.wait(0.8)

        # 9. Konkretni izračun za petkotnik.
        racun_pet = MathTex(r"3\cdot180^\circ=540^\circ", color=UL_RED).scale(1.2)
        racun_pet.move_to(DOWN * 4.2)
        self.play(Write(racun_pet), run_time=0.8)
        self.wait(0.8)

        # 10. Število trikotnikov sledi vzorcu n - 2.
        vrstice_y = [2.5, 1.7, 0.9, 0.1]
        leva_sidra = []
        desna_sidra = []
        pregled_vrstice = []
        stevila_stranic = ["3", "4", "5", "6"]
        poimenovanja_stranic = ["stranice", "stranice", "stranic", "stranic"]
        stevila_trikotnikov = ["1", "2", "3", "4"]
        poimenovanja_trikotnikov = ["trikotnik", "trikotnika", "trikotniki", "trikotniki"]

        def postavi_desno(obj, x, y):
            obj.move_to([x - obj.width / 2, y, 0])

        def postavi_levo(obj, x, y):
            obj.move_to([x + obj.width / 2, y, 0])

        for i, y in enumerate(vrstice_y):
            st_stranic = self.txt(stevila_stranic[i], size=29)
            beseda_stranic = self.txt(poimenovanja_stranic[i], size=29)
            puscica = MathTex(r"\longrightarrow", color=UL_BLUE).scale(0.78)
            st_trikotnikov = self.txt(stevila_trikotnikov[i], size=29)
            beseda_trikotnikov = self.txt(poimenovanja_trikotnikov[i], size=29)
            postavi_desno(st_stranic, -2.35, y)
            postavi_levo(beseda_stranic, -2.18, y)
            puscica.move_to([0.0, y, 0])
            postavi_desno(st_trikotnikov, 1.35, y)
            postavi_levo(beseda_trikotnikov, 1.53, y)
            leva_sidra.append(st_stranic)
            desna_sidra.append(st_trikotnikov)
            pregled_vrstice.append(
                VGroup(st_stranic, beseda_stranic, puscica, st_trikotnikov, beseda_trikotnikov)
            )
        pregled = VGroup(*pregled_vrstice)
        domena_n = MathTex(r"n\in\mathbb{N},\quad n\ge3", color=UL_GRAY).scale(0.76).move_to(DOWN * 1.15)
        self.play(FadeOut(VGroup(naslov_pet, kosi, racun_pet)), run_time=0.8)
        naslov_vzorec = self.heading("OPAZIMO VZOREC")
        self.play(FadeIn(naslov_vzorec), FadeIn(pregled), run_time=1.0)
        n_nadomestek = self.txt("n", size=29, color=UL_RED)
        n_nadomestek.move_to([-2.35 - n_nadomestek.width / 2, vrstice_y[3], 0])
        n_minus_2_nadomestek = self.txt("n − 2", size=29, color=UL_RED)
        n_minus_2_nadomestek.move_to([1.35 - n_minus_2_nadomestek.width / 2, vrstice_y[3], 0])
        self.play(
            Transform(leva_sidra[3], n_nadomestek),
            Transform(desna_sidra[3], n_minus_2_nadomestek),
            run_time=0.9,
        )
        self.play(FadeIn(domena_n), run_time=0.4)
        self.wait(2.7)

        # 11. Posplošitev in končno pravilo.
        self.play(FadeOut(VGroup(naslov_vzorec, pregled, domena_n)), run_time=0.8)
        naslov_pravilo = self.heading("SPLOŠNO PRAVILO")
        formula_splosno = MathTex(r"S=(n-2)\cdot180^\circ", color=UL_RED).scale(1.35)
        formula_splosno.move_to(UP * 1.25)
        pomen_S = self.txt("S = vsota notranjih kotov", size=27).move_to(DOWN * 0.5)
        pomen_n = self.txt("n = število stranic", size=27, color=UL_GRAY).move_to(DOWN * 1.35)
        zakljucek = self.txt("n − 2 je število trikotnikov.", size=25, color=UL_BLUE).move_to(DOWN * 2.55)
        self.play(FadeIn(naslov_pravilo), Write(formula_splosno), run_time=1.0)
        self.play(FadeIn(pomen_S, pomen_n, zakljucek), run_time=0.6)
        self.wait(0.9)

        # Samostojen zaključni kader z uradnim logotipom UL FMF.
        self.play(FadeOut(VGroup(naslov_pravilo, formula_splosno, pomen_S, pomen_n, zakljucek)), run_time=0.4)
        logo_path = Path(__file__).parent / "media" / "images" / "UL_FMF_logoHOR-RGB_barv.png"
        logo_fmf = ImageMobject(str(logo_path)).scale_to_fit_width(7.2).move_to(ORIGIN)
        self.play(FadeIn(logo_fmf), run_time=0.4)
        self.wait(1.4666667)


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
