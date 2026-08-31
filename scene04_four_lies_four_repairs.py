import numpy as np
from manim import *
from teachme_manim import BeatClock

GOLD = "#F0AC5F"
GREEN = "#83C167"
BLUE = "#58C4DD"
YELLOW = "#F4D345"
RED = "#FC6255"
GREY_B = "#CCCCCC"

BEATS = [12.01, 12.46, 13.58, 9.34, 12.05, 12.22, 15.6, 16.67, 19.85, 3.62]


class TeachScene(Scene):
    def construct(self):
        self.camera.background_color = "#0e1015"
        np.random.seed(3)
        clock = BeatClock(self, BEATS)

        # ---------- Beat 1 (index 0): title, four dots ----------
        title = Text("Four lies, four repairs", font_size=44, color=WHITE).move_to([0, 3.1, 0])
        clock.play(Write(title), run_time=1.2)

        dots = VGroup(*[Dot(point=[x, 0, 0], radius=0.08, color=GREY_B) for x in (-2.4, -0.8, 0.8, 2.4)])
        clock.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.3), run_time=1.0)
        clock.wait(2.0)
        clock.play(FadeOut(dots), run_time=1.0)

        title_small = Text("Four lies, four repairs", font_size=38, color=WHITE).move_to([-4.3, 3.3, 0])
        clock.play(ReplacementTransform(title, title_small), run_time=1.2)
        title = title_small

        # pre-fade a faint preview of the Beat 2 axes so the screen never goes
        # fully blank while it waits for the momentum chart to arrive
        axes1 = Axes(
            x_range=[0, 60, 20],
            y_range=[-3, 3, 1],
            x_length=7.0,
            y_length=2.6,
            axis_config={"color": WHITE, "include_tip": False, "stroke_width": 2},
        ).move_to([0, 1.0, 0])
        axes1.set_stroke(opacity=0.25)
        clock.play(FadeIn(axes1), run_time=1.5)
        clock.wait(4.0)
        clock.end_beat(0)

        # ---------- Beat 2 (index 1): the annualizing lie ----------
        run_lens = np.random.randint(5, 10, size=20)
        signs = []
        s = 1
        for rl in run_lens:
            signs += [s] * int(rl)
            s *= -1
        signs = np.array(signs[:60])
        mags = np.random.uniform(0.6, 2.2, 60)
        rets = signs * mags
        mom_pts = [axes1.c2p(x, y) for x, y in enumerate(rets)]
        mom_line = VMobject(stroke_color=BLUE, stroke_width=3)
        mom_line.set_points_as_corners(mom_pts)
        mom_label = Text("momentum, daily", font_size=28, color=BLUE).move_to([0, 2.7, 0])

        clock.play(axes1.animate.set_stroke(opacity=1), run_time=0.6)
        clock.play(Create(mom_line), FadeIn(mom_label), run_time=1.5)

        times_eq = MathTex(
            r"\times 252 \;\Rightarrow\; \text{days are independent}", font_size=30, color=RED
        ).move_to([0, -1.0, 0])
        clock.play(Write(times_eq), run_time=1.2)

        realized_text = Text("realized 1.40x the forecast", font_size=30, color=RED).move_to([0, -1.9, 0])
        clock.play(FadeIn(realized_text), run_time=0.8)
        clock.wait(1.5)
        clock.end_beat(1)

        # ---------- Beat 3 (index 2): Newey-West repair ----------
        clock.play(FadeOut(VGroup(mom_line, axes1, times_eq, mom_label)), run_time=1.0)
        clock.play(realized_text.animate.move_to([0, -0.9, 0]), run_time=1.0)

        nw_formula = MathTex(
            r"\text{var}_{\text{adj}} = \text{var} + 2\sum_{l=1}^{5}\left(1 - \frac{l}{6}\right)\gamma_l",
            color=WHITE,
        ).scale(0.95).move_to([0, 2.1, 0])
        clock.play(Write(nw_formula), run_time=1.8)

        bar_xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        bar_heights = [1.25, 1.00, 0.75, 0.50, 0.25]
        bars = VGroup()
        bar_labels = VGroup()
        for i, (x, h) in enumerate(zip(bar_xs, bar_heights)):
            bar = Rectangle(width=0.5, height=h, fill_color=GOLD, fill_opacity=0.85, stroke_width=0)
            bar.move_to([x, 0.2 + h / 2, 0])
            bars.add(bar)
            lbl = Text(str(i + 1), font_size=24, color=GREY_B).move_to([x, -0.15, 0])
            bar_labels.add(lbl)
        clock.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.2), FadeIn(bar_labels), run_time=1.5)

        psd_text = Text("variances only, so V C V stays PSD", font_size=28, color=GREEN).move_to([0, -0.9, 0])
        clock.play(ReplacementTransform(realized_text, psd_text), run_time=1.0)
        clock.wait(5.6)

        ledger1_name = Text("Newey-West", font_size=28, color=WHITE).move_to([-3.2, -1.7, 0])
        ledger1_val = Text("1.40x", font_size=28, color=RED).move_to([2.4, -1.7, 0])
        ledger1 = VGroup(ledger1_name, ledger1_val)
        clock.play(
            FadeOut(VGroup(nw_formula, bars, bar_labels)),
            ReplacementTransform(psd_text, ledger1),
            run_time=1.5,
        )
        clock.end_beat(2)

        # ---------- Beat 4 (index 3): the responsiveness lag ----------
        axes2 = Axes(
            x_range=[0, 100, 25],
            y_range=[0, 30, 10],
            x_length=7.4,
            y_length=2.4,
            axis_config={"color": WHITE, "include_tip": False, "stroke_width": 2},
        ).move_to([0, 1.6, 0])

        step = VMobject(stroke_color=WHITE, stroke_width=3)
        step.set_points_as_corners([axes2.c2p(0, 12), axes2.c2p(40, 12), axes2.c2p(40, 26), axes2.c2p(100, 26)])

        halflife = 15
        ewma_xs = np.linspace(40, 100, 60)
        ewma_ys = 26 - 14 * np.power(2.0, -(ewma_xs - 40) / halflife)
        ewma_pts = [axes2.c2p(0, 12), axes2.c2p(40, 12)] + [axes2.c2p(x, y) for x, y in zip(ewma_xs, ewma_ys)]
        ewma = VMobject(stroke_color=GOLD, stroke_width=3)
        ewma.set_points_smoothly(ewma_pts)

        clock.play(Create(axes2), run_time=0.8)
        clock.play(Create(step), run_time=1.5)
        clock.play(Create(ewma), run_time=1.5)

        x_jump = axes2.c2p(40, 0)[0]
        x_half = axes2.c2p(40 + halflife, 0)[0]
        lag_arrow = DoubleArrow(
            [x_jump, 1.4, 0], [x_half, 1.4, 0], color=YELLOW, buff=0, stroke_width=3, tip_length=0.15
        )
        lag_label = Text("one half-life late", font_size=28, color=YELLOW).move_to([1.0, 0.0, 0])
        clock.play(Create(lag_arrow), FadeIn(lag_label), run_time=1.2)
        clock.wait(1.5)
        clock.end_beat(3)

        # ---------- Beat 5 (index 4): forty coincidences ----------
        clock.play(FadeOut(VGroup(axes2, step, ewma, lag_arrow, lag_label)), run_time=1.0)

        n_bars = 40
        ratio_xs = np.linspace(-(n_bars - 1) * 0.16 / 2, (n_bars - 1) * 0.16 / 2, n_bars)
        ratio_heights = 1.5 + np.random.uniform(-0.25, 0.25, n_bars)
        ratio_bars = VGroup()
        for x, h in zip(ratio_xs, ratio_heights):
            b = Rectangle(width=0.13, height=h, fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
            b.move_to([x, 0.4 + h / 2, 0])
            ratio_bars.add(b)

        baseline = Line([ratio_xs[0] - 0.3, 0.4, 0], [ratio_xs[-1] + 0.3, 0.4, 0], color=WHITE, stroke_width=2)
        forecast_y = 0.4 + 1.0
        forecast_line = DashedLine(
            [ratio_xs[0] - 0.3, forecast_y, 0], [ratio_xs[-1] + 0.3, forecast_y, 0], color=WHITE, stroke_width=2
        )
        forecast_label = Text("forecast", font_size=26, color=WHITE).move_to([4.4, forecast_y, 0])

        clock.play(Create(baseline), run_time=0.5)
        clock.play(LaggedStart(*[Create(b) for b in ratio_bars], lag_ratio=0.05), run_time=2.0)
        clock.play(Create(forecast_line), FadeIn(forecast_label), run_time=0.8)

        message_text = Text("not 40 coincidences, one message", font_size=30, color=GOLD).move_to([0, -0.9, 0])
        clock.play(FadeIn(message_text), run_time=1.0)
        clock.wait(2.0)
        clock.end_beat(4)

        # ---------- Beat 6 (index 5): the regime multiplier ----------
        bt_formula = MathTex(
            r"B_t^2 = \text{mean}_k\left(\frac{f_{kt}}{\sigma_{kt}}\right)^2, \quad "
            r"\lambda_F = \sqrt{\text{EWMA}[B^2]}",
            color=GOLD,
        ).scale(0.75).move_to([0, 2.3, 0])
        clock.play(ReplacementTransform(ratio_bars, bt_formula), run_time=1.8)
        clock.play(FadeOut(VGroup(message_text, baseline, forecast_line, forecast_label)), run_time=0.8)

        axes3 = Axes(
            x_range=[0, 24, 6],
            y_range=[0.6, 1.4, 0.2],
            x_length=6.8,
            y_length=2.2,
            axis_config={"color": WHITE, "include_tip": False, "stroke_width": 2},
        ).move_to([0, 0.8, 0])
        x_axis_label3 = Text("2008-09", font_size=26, color=GREY_B).next_to(axes3, DOWN, buff=0.2)

        red_xs = np.linspace(0, 24, 40)
        red_ys = np.where(red_xs < 12, 1.0 + 0.3 * (red_xs / 12), 1.3 - 0.6 * ((red_xs - 12) / 12))
        red_pts = [axes3.c2p(x, y) for x, y in zip(red_xs, red_ys)]
        red_line = VMobject(stroke_color=RED, stroke_width=3)
        red_line.set_points_smoothly(red_pts)
        red_label = Text("unadjusted", font_size=26, color=RED).move_to([4.8, 1.5, 0])

        white_xs = np.linspace(0, 24, 40)
        white_ys = 1.0 + 0.02 * np.sin(white_xs)
        white_pts = [axes3.c2p(x, y) for x, y in zip(white_xs, white_ys)]
        white_line = VMobject(stroke_color=WHITE, stroke_width=3)
        white_line.set_points_smoothly(white_pts)
        white_label = Text("adjusted", font_size=26, color=WHITE).move_to([4.8, 0.6, 0])

        clock.play(Create(axes3), FadeIn(x_axis_label3), run_time=0.8)
        clock.play(Create(red_line), FadeIn(red_label), run_time=1.5)
        clock.play(Create(white_line), FadeIn(white_label), run_time=1.2)
        clock.wait(4.4)

        ledger2_name = Text("Regime multiplier", font_size=28, color=WHITE).move_to([-3.2, -2.2, 0])
        ledger2_val = Text("1.3 / 0.7 becomes 1.0", font_size=28, color=GOLD).move_to([2.4, -2.2, 0])
        ledger2 = VGroup(ledger2_name, ledger2_val)
        clock.play(
            FadeOut(VGroup(axes3, x_axis_label3, red_line, red_label, white_line, white_label, bt_formula)),
            FadeIn(ledger2),
            run_time=1.5,
        )
        clock.end_beat(5)

        # ---------- Beat 7 (index 6): the correlation blend ----------
        n_eig = 40
        eig_xs = np.linspace(-(n_eig - 1) * 0.16 / 2, (n_eig - 1) * 0.16 / 2, n_eig)
        decay = 1.8 * np.exp(-np.arange(n_eig) / 6.0) + 0.05
        eig_bars = VGroup()
        for i, (x, h) in enumerate(zip(eig_xs, decay)):
            color = GREEN if i < 30 else RED
            opacity = 0.8 if i < 30 else 0.9
            b = Rectangle(width=0.13, height=h, fill_color=color, fill_opacity=opacity, stroke_width=0)
            b.move_to([x, 0.1 + h / 2, 0])
            eig_bars.add(b)
        clock.play(LaggedStart(*[Create(b) for b in eig_bars], lag_ratio=0.05), run_time=2.0)

        question_text = Text("these directions never move?", font_size=28, color=RED).move_to([2.6, -0.6, 0])
        clock.play(FadeIn(question_text), run_time=0.6)
        clock.wait(1.2)

        pca_formula = MathTex(
            r"C \leftarrow 0.8\, C_{\text{sample}} + 0.2\, C_{\text{PCA}}(10)", color=GREEN
        ).scale(0.8).move_to([0, 2.6, 0])
        clock.play(Write(pca_formula), run_time=1.5)

        floor_h = 0.4
        grow_anims = []
        for i, b in enumerate(eig_bars):
            if i >= 30:
                new_b = b.copy().set_fill(GREEN, opacity=0.8)
                new_b.stretch_to_fit_height(floor_h, about_edge=DOWN)
                grow_anims.append(Transform(b, new_b))
        clock.play(*grow_anims, run_time=1.5)
        clock.play(FadeOut(question_text), run_time=0.6)
        clock.wait(6.5)

        ledger3_name = Text("Correlation blend", font_size=28, color=WHITE).move_to([-3.2, -2.7, 0])
        ledger3_val = Text("1.36 becomes 1.29", font_size=28, color=GREEN).move_to([2.4, -2.7, 0])
        ledger3 = VGroup(ledger3_name, ledger3_val)
        clock.play(
            FadeOut(VGroup(eig_bars, pca_formula)),
            FadeIn(ledger3),
            run_time=1.5,
        )
        clock.end_beat(6)

        # ---------- Beat 8 (index 7): the alternative that did not survive ----------
        number_line = NumberLine(
            x_range=[0.7, 1.4, 0.1], length=8.4, include_numbers=True, font_size=24, color=WHITE
        ).move_to([0, 0.2, 0])

        one_x = number_line.n2p(1.0)[0]
        dashed_vert = DashedLine([one_x, -0.4, 0], [one_x, 2.4, 0], color=WHITE, stroke_width=2)

        band_left = number_line.n2p(0.88)[0]
        band_right = number_line.n2p(1.12)[0]
        band = Rectangle(
            width=band_right - band_left, height=2.8, fill_color=GREY_B, fill_opacity=0.12, stroke_width=0
        ).move_to([(band_left + band_right) / 2, 1.0, 0])

        clock.play(FadeIn(band), Create(number_line), Create(dashed_vert), run_time=1.5)

        d_minvar = Dot(point=[number_line.n2p(1.36)[0], 2.0, 0], radius=0.09, color=RED)
        d_style = Dot(point=[number_line.n2p(1.16)[0], 1.5, 0], radius=0.09, color=RED)
        d_random = Dot(point=[number_line.n2p(0.93)[0], 1.0, 0], radius=0.09, color=WHITE)
        d_equal = Dot(point=[number_line.n2p(0.98)[0], 0.6, 0], radius=0.09, color=WHITE)

        l_minvar = Text("min-var", font_size=26, color=RED).move_to([-5.5, 2.0, 0])
        l_style = Text("style", font_size=26, color=RED).move_to([-5.5, 1.5, 0])
        l_random = Text("random", font_size=26, color=WHITE).move_to([-5.5, 1.0, 0])
        l_equal = Text("equal", font_size=26, color=WHITE).move_to([-5.5, 0.6, 0])

        dots_group = VGroup(d_minvar, d_style, d_random, d_equal)
        labels_group = VGroup(l_minvar, l_style, l_random, l_equal)
        clock.play(FadeIn(dots_group), FadeIn(labels_group), run_time=1.0)
        clock.wait(1.0)

        targets = [0.98, 0.92, 0.75, 0.77]
        new_colors = [WHITE, WHITE, RED, RED]
        anims = []
        for dot, val, col in zip(dots_group, targets, new_colors):
            new_x = number_line.n2p(val)[0]
            anims.append(dot.animate.move_to([new_x, dot.get_y(), 0]).set_color(col))
        clock.play(*anims, run_time=2.0)

        switched_off_text = Text("switched off, result published", font_size=28, color=RED).move_to([0, -1.0, 0])
        clock.play(FadeIn(switched_off_text), run_time=1.0)
        clock.wait(9.0)

        clock.play(
            FadeOut(VGroup(number_line, band, dashed_vert, dots_group, labels_group, switched_off_text)),
            run_time=1.0,
        )
        clock.end_beat(7)

        # ---------- Beat 9 (index 8): specific-risk shrinkage ----------
        axes4 = Axes(
            x_range=[0, 400, 100],
            y_range=[0, 1.0, 0.25],
            x_length=6.6,
            y_length=2.4,
            axis_config={"color": WHITE, "include_tip": False, "stroke_width": 2},
        ).move_to([0, 1.2, 0])
        x_label4 = Text("days of history", font_size=26, color=WHITE).next_to(axes4, DOWN, buff=0.25)
        y_label4 = Text("weight on own record", font_size=26, color=WHITE).rotate(90 * DEGREES).next_to(
            axes4, LEFT, buff=0.3
        )

        weight_curve = axes4.plot(lambda t: t / (t + 126), x_range=[0, 400], color=GREY_B, stroke_width=4)

        clock.play(Create(axes4), FadeIn(x_label4), FadeIn(y_label4), run_time=1.2)
        clock.play(Create(weight_curve), run_time=1.5)

        marks = [(0, "0.00"), (63, "0.33"), (126, "0.50"), (252, "0.67")]
        mark_dots = VGroup()
        mark_labels = VGroup()
        for T, lbl in marks:
            w = T / (T + 126)
            pt = axes4.c2p(T, w)
            d = Dot(point=pt, radius=0.07, color=WHITE)
            t = Text(lbl, font_size=24, color=WHITE).next_to(d, UP, buff=0.12)
            mark_dots.add(d)
            mark_labels.add(t)
        clock.play(FadeIn(mark_dots), FadeIn(mark_labels), run_time=0.8)

        w_formula = MathTex(r"w_i = \frac{T_i}{T_i + 126}", color=GREY_B).scale(0.95).move_to([4.6, 1.8, 0])
        clock.play(Write(w_formula), run_time=1.2)
        clock.wait(2.0)

        clock.play(
            FadeOut(VGroup(axes4, x_label4, y_label4, weight_curve, mark_dots, mark_labels, w_formula)),
            run_time=1.0,
        )

        decile_xs = np.linspace(-3.6, 3.6, 10)
        decile_ys = np.linspace(1.4, 0.2, 10)
        decile_dots = VGroup(*[Dot(point=[x, y, 0], radius=0.09, color=GREY_B) for x, y in zip(decile_xs, decile_ys)])
        clock.play(LaggedStart(*[FadeIn(d) for d in decile_dots], lag_ratio=0.15), run_time=1.2)

        target_line = DashedLine([-4.0, 0.8, 0], [4.0, 0.8, 0], color=WHITE, stroke_width=2)
        target_label = Text("1.00", font_size=26, color=WHITE).move_to([4.4, 0.8, 0])
        clock.play(Create(target_line), FadeIn(target_label), run_time=0.8)

        clock.play(*[d.animate.move_to([d.get_x(), 0.8, 0]) for d in decile_dots], run_time=1.5)
        clock.wait(7.0)

        ledger4_name = Text("Specific shrinkage", font_size=28, color=WHITE).move_to([-3.2, -3.2, 0])
        ledger4_val = Text("1.08 / 0.92 becomes 1.00", font_size=28, color=GREY_B).move_to([2.4, -3.2, 0])
        ledger4 = VGroup(ledger4_name, ledger4_val)
        clock.play(
            FadeOut(VGroup(decile_dots, target_line, target_label)),
            FadeIn(ledger4),
            run_time=1.5,
        )
        clock.end_beat(8)

        # ---------- Beat 10 (index 9): the finished ledger ----------
        full_ledger = VGroup(ledger1, ledger2, ledger3, ledger4)
        clock.play(full_ledger.animate.move_to([0, 0.2, 0]).scale(1.15), run_time=1.2)
        clock.wait(1.2)
        clock.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        clock.end_beat(9)
