from manim import *
from teachme_manim import BeatClock
import numpy as np

WHITE = "#FFFFFF"
RED = "#FC6255"
GOLD = "#F0AC5F"
BLUE = "#58C4DD"
YELLOW = "#F4D345"
GREY_B = "#CCCCCC"

BEATS = [8.88, 11.08, 7.22, 13.63, 10.02, 6.19, 15.93, 14.12, 19.1]


def true_vol(h):
    return 0.20 * np.sqrt(1.0 + h ** 2 - 1.2 * h)


class TeachScene(Scene):
    def construct(self):
        np.random.seed(3)
        self.camera.background_color = "#0e1015"
        clock = BeatClock(self, BEATS)

        # ---------- Beat 0: the optimizer is an adversary ----------
        title = Text("The optimizer is an adversary", font_size=44, color=WHITE)
        title.move_to(np.array([0.0, 3.1, 0.0]))
        clock.play(Write(title), run_time=1.2)

        half = 1.4
        step = 2.8 / 20.0
        cx, cy = 0.0, 0.2
        grid_lines = VGroup()
        for i in range(1, 20):
            gx = -half + i * step
            grid_lines.add(
                Line(
                    np.array([cx + gx, cy - half, 0.0]),
                    np.array([cx + gx, cy + half, 0.0]),
                    color=GREY_B, stroke_width=1,
                )
            )
            gy = -half + i * step
            grid_lines.add(
                Line(
                    np.array([cx - half, cy + gy, 0.0]),
                    np.array([cx + half, cy + gy, 0.0]),
                    color=GREY_B, stroke_width=1,
                )
            )
        grid_lines.set_stroke(opacity=0.22)
        square = Square(side_length=2.8, stroke_color=WHITE, stroke_width=2, fill_opacity=0.0)
        square.move_to(np.array([cx, cy, 0.0]))
        sigma_square = VGroup(grid_lines, square)
        clock.play(FadeIn(sigma_square), run_time=1.0)

        sweep = Rectangle(width=0.35, height=2.8, fill_color=RED, fill_opacity=0.35, stroke_opacity=0.0)
        sweep.move_to(np.array([cx - half, cy, 0.0]))
        clock.play(FadeIn(sweep), run_time=0.3)
        clock.play(sweep.animate.move_to(np.array([cx + half, cy, 0.0])), run_time=2.0, rate_func=linear)

        interior_dot = Dot(point=np.array([0.35, 0.55, 0.0]), radius=0.10, color=RED)
        clock.play(FadeOut(sweep), FadeIn(interior_dot), run_time=0.4)

        hunt_text = Text("it hunts the cheapest direction", font_size=30, color=RED)
        hunt_text.move_to(np.array([0.0, -1.8, 0.0]))
        clock.play(FadeIn(hunt_text), run_time=0.6)
        clock.wait(1.5)
        clock.end_beat(0)

        # ---------- Beat 1: the true-volatility curve ----------
        clock.play(
            FadeOut(sigma_square), FadeOut(interior_dot), FadeOut(hunt_text), run_time=1.0
        )

        corner_title = Text("The optimizer is an adversary", font_size=30, color=WHITE)
        corner_title.move_to(np.array([-3.9, 3.25, 0.0]))
        clock.play(ReplacementTransform(title, corner_title), run_time=0.8)

        axes = Axes(
            x_range=[0.0, 1.2, 0.2],
            y_range=[0.12, 0.21, 0.01],
            x_length=7.4,
            y_length=5.2,
            axis_config={"color": GREY_B, "stroke_width": 2},
            tips=False,
        )
        axes.move_to(np.array([0.1, -0.3, 0.0]))
        clock.play(Create(axes), run_time=1.5)

        x_label = Text("hedge ratio h", font_size=28, color=WHITE)
        x_label.move_to(np.array([0.1, -3.25, 0.0]))
        y_label = Text("volatility", font_size=28, color=WHITE).rotate(PI / 2)
        y_label.move_to(np.array([-4.5, -0.3, 0.0]))
        clock.play(FadeIn(x_label), FadeIn(y_label), run_time=0.8)

        formula = MathTex(
            r"\sigma^2 = 0.04\,(1 + h^2 - 2h\rho), \quad \rho = 0.60",
            color=WHITE,
        ).scale(0.85)
        formula.move_to(np.array([1.4, 2.7, 0.0]))
        if formula.width > 9.4:
            formula.scale_to_fit_width(9.4)
            formula.move_to(np.array([1.4, 2.7, 0.0]))
        clock.play(Write(formula), run_time=1.5)

        curve = axes.plot(true_vol, x_range=[0.0, 1.2], color=WHITE, stroke_width=4)
        clock.play(Create(curve), run_time=2.0)

        true_label = Text("true", font_size=28, color=WHITE)
        true_label.move_to(axes.coords_to_point(1.05, true_vol(1.05)) + np.array([0.0, 0.35, 0.0]))
        clock.play(FadeIn(true_label), run_time=0.5)
        clock.end_beat(1)

        # ---------- Beat 2: the minimum, 16.0% at h = 0.60 ----------
        min_point = axes.coords_to_point(0.6, 0.16)
        min_dot = Dot(point=min_point, radius=0.09, color=WHITE)
        clock.play(FadeIn(min_dot), run_time=0.5)

        min_line = DashedLine(min_point, axes.coords_to_point(0.6, 0.12), color=GREY_B, stroke_width=2)
        clock.play(Create(min_line), run_time=0.7)

        min_label = MathTex(r"16.0\%", font_size=28, color=WHITE)
        min_label.next_to(min_dot, DOWN, buff=0.15)
        clock.play(FadeIn(min_label), run_time=0.5)
        clock.wait(2.0)
        clock.end_beat(2)

        # ---------- Beat 3: optimistic estimate 0.75 ----------
        red_point = axes.coords_to_point(0.75, 0.132)
        red_dot = Dot(point=red_point, radius=0.10, color=RED)
        red_label = MathTex(r"13.2\%", font_size=28, color=RED).next_to(red_dot, RIGHT, buff=0.15)
        clock.play(FadeIn(red_dot), FadeIn(red_label), run_time=0.8)

        white75_point = axes.coords_to_point(0.75, true_vol(0.75))
        white75_dot = Dot(point=white75_point, radius=0.09, color=WHITE)
        white75_label = MathTex(r"16.3\%", font_size=28, color=WHITE).next_to(white75_dot, UP, buff=0.15)
        clock.play(FadeIn(white75_dot), FadeIn(white75_label), run_time=0.8)

        arrow75 = DoubleArrow(red_point, white75_point, color=RED, stroke_width=4, buff=0.15)
        bias75_label = Text("bias 1.23", font_size=28, color=RED).next_to(arrow75, RIGHT, buff=0.2)
        clock.play(Create(arrow75), FadeIn(bias75_label), run_time=0.8)

        estimate75 = Text("estimate 0.75", font_size=26, color=RED)
        estimate75.move_to(np.array([2.4, -2.85, 0.0]))
        clock.play(FadeIn(estimate75), run_time=0.6)
        clock.wait(2.0)
        clock.end_beat(3)

        # ---------- Beat 4: pessimistic estimate 0.45 ----------
        gold_point = axes.coords_to_point(0.45, 0.179)
        gold_dot = Dot(point=gold_point, radius=0.10, color=GOLD)
        gold_label = MathTex(r"17.9\%", font_size=28, color=GOLD).next_to(gold_dot, LEFT, buff=0.15)
        clock.play(FadeIn(gold_dot), FadeIn(gold_label), run_time=0.8)

        white45_point = axes.coords_to_point(0.45, true_vol(0.45))
        white45_dot = Dot(point=white45_point, radius=0.09, color=WHITE)
        white45_label = MathTex(r"16.3\%", font_size=28, color=WHITE).next_to(white45_dot, DOWN, buff=0.15)
        clock.play(FadeIn(white45_dot), FadeIn(white45_label), run_time=0.8)

        arrow45 = DoubleArrow(gold_point, white45_point, color=GOLD, stroke_width=4, buff=0.15)
        bias45_label = Text("bias 0.91", font_size=28, color=GOLD).next_to(arrow45, LEFT, buff=0.2)
        clock.play(Create(arrow45), FadeIn(bias45_label), run_time=0.8)

        estimate45 = Text("estimate 0.45", font_size=26, color=GOLD)
        estimate45.move_to(np.array([-0.7, -2.85, 0.0]))
        clock.play(FadeIn(estimate45), run_time=0.6)
        clock.wait(2.0)
        clock.end_beat(4)

        # ---------- Beat 5: same true risk, different forecast ----------
        level_line = DashedLine(white75_point, white45_point, color=WHITE, stroke_width=3)
        clock.play(Create(level_line), run_time=1.2)

        fade_group = VGroup(
            axes, x_label, y_label, formula, curve, true_label,
            min_dot, min_line, min_label,
            red_dot, red_label, arrow75, bias75_label, estimate75,
            gold_dot, gold_label, arrow45, bias45_label, estimate45,
        )
        clock.play(FadeOut(fade_group), run_time=1.2)

        same_text = Text("same true risk, different forecast", font_size=32, color=WHITE)
        same_text.move_to(np.array([0.0, -1.6, 0.0]))
        clock.play(FadeIn(same_text), run_time=0.6)
        clock.wait(2.5)
        clock.end_beat(5)

        # ---------- Beat 6: selection turns error into bias ----------
        clock.play(
            FadeOut(level_line), FadeOut(white75_dot), FadeOut(white75_label),
            FadeOut(white45_dot), FadeOut(white45_label), FadeOut(same_text),
            run_time=1.2,
        )

        number_line = NumberLine(x_range=[-2.4, 2.4, 1.0], length=4.8, color=WHITE, rotation=PI / 2)
        number_line.move_to(np.array([-4.0, 0.0, 0.0]))
        nl_label = Text("predicted risk", font_size=28, color=WHITE).rotate(PI / 2)
        nl_label.move_to(np.array([-5.2, 0.0, 0.0]))
        clock.play(Create(number_line), FadeIn(nl_label), run_time=1.0)

        red_xs = [-2.8, -1.9, -1.0, -0.1, 0.9, 1.8, 2.9]
        red_ys = [-1.9, -1.4, -2.0, -0.5, -1.6, -1.0, -0.3]
        gold_xs = [-2.3, -1.4, -0.5, 0.5, 1.4, 2.3, 3.3]
        gold_ys = [1.8, 1.3, 2.1, 0.5, 1.6, 0.9, 0.3]
        red_dots = VGroup(*[Dot(np.array([x, y, 0.0]), radius=0.09, color=RED) for x, y in zip(red_xs, red_ys)])
        gold_dots = VGroup(*[Dot(np.array([x, y, 0.0]), radius=0.09, color=GOLD) for x, y in zip(gold_xs, gold_ys)])
        clock.play(
            LaggedStart(*[FadeIn(d) for d in list(red_dots) + list(gold_dots)], lag_ratio=0.06),
            run_time=1.5,
        )

        clock.play(
            *[d.animate.move_to(np.array([-3.4, d.get_center()[1], 0.0])) for d in red_dots],
            gold_dots.animate.set_opacity(0.25),
            run_time=2.0,
        )

        takes_text = Text("the optimizer takes these", font_size=28, color=RED)
        takes_text.move_to(np.array([0.4, -3.0, 0.0]))
        clock.play(FadeIn(takes_text), run_time=0.6)
        clock.wait(1.5)

        symmetric_text = Text("symmetric error becomes one-sided bias", font_size=30, color=WHITE)
        symmetric_text.move_to(np.array([0.4, 2.8, 0.0]))
        clock.play(FadeIn(symmetric_text), run_time=0.6)
        clock.wait(2.0)
        clock.end_beat(6)

        # ---------- Beat 7: the Shepard correction ----------
        clock.play(
            FadeOut(number_line), FadeOut(nl_label), FadeOut(red_dots), FadeOut(gold_dots),
            FadeOut(takes_text), FadeOut(symmetric_text), run_time=1.2,
        )

        shepard = MathTex(
            r"\sigma_{\text{true}} \approx \frac{\sigma_{\text{predicted}}}{1 - K / N_{\text{eff}}}",
            color=WHITE,
        ).scale(1.4)
        shepard.move_to(np.array([0.0, 1.6, 0.0]))
        shepard.set_color_by_tex("K", BLUE)
        shepard.set_color_by_tex(r"N_{\text{eff}}", YELLOW)
        clock.play(Write(shepard), run_time=1.8)

        info_text = Text("parameters over information", font_size=28, color=GREY_B)
        info_text.move_to(np.array([0.0, 0.5, 0.0]))
        clock.play(FadeIn(info_text), run_time=0.6)
        clock.wait(1.0)

        arithmetic = MathTex(r"\frac{1}{1 - 20/243} = 1.090", color=WHITE).scale(1.0)
        arithmetic.move_to(np.array([-2.4, -1.0, 0.0]))
        clock.play(Write(arithmetic), run_time=1.4)

        measured = Text("measured 1.088", font_size=32, color=WHITE)
        measured.move_to(np.array([2.6, -1.0, 0.0]))
        clock.play(Write(measured), run_time=1.0)

        floor_text = Text("at K = 40 the floor is 1.20", font_size=28, color=BLUE)
        floor_text.move_to(np.array([0.0, -2.2, 0.0]))
        clock.play(FadeIn(floor_text), run_time=0.6)
        clock.wait(2.5)
        clock.end_beat(7)

        # ---------- Beat 8: the correction lives at the reporting layer ----------
        clock.play(
            FadeOut(shepard), FadeOut(info_text), FadeOut(arithmetic),
            FadeOut(measured), FadeOut(floor_text), run_time=1.2,
        )

        box1 = Rectangle(width=3.0, height=1.4, stroke_color=WHITE, stroke_width=2)
        box1.move_to(np.array([-3.6, 0.6, 0.0]))
        box2 = Rectangle(width=3.0, height=1.4, stroke_color=WHITE, stroke_width=2)
        box2.move_to(np.array([0.0, 0.6, 0.0]))
        box3 = Rectangle(width=3.0, height=1.4, stroke_color=WHITE, stroke_width=2)
        box3.move_to(np.array([3.6, 0.6, 0.0]))
        arrow_a = Arrow(box1.get_right(), box2.get_left(), color=WHITE, buff=0.05, stroke_width=4)
        arrow_b = Arrow(box2.get_right(), box3.get_left(), color=WHITE, buff=0.05, stroke_width=4)
        pipeline = VGroup(box1, box2, box3, arrow_a, arrow_b)
        clock.play(LaggedStart(*[Create(m) for m in pipeline], lag_ratio=0.2), run_time=2.0)

        label1 = Text("the matrix", font_size=28, color=WHITE).move_to(box1.get_center())
        label2 = Text("reporting layer", font_size=28, color=WHITE).move_to(box2.get_center())
        label3 = Text("the caller", font_size=28, color=WHITE).move_to(box3.get_center())
        clock.play(FadeIn(label1), FadeIn(label2), FadeIn(label3), run_time=0.6)

        under1 = Text("unbiased for chosen-in-advance", font_size=26, color=GREY_B)
        under1.move_to(np.array([-3.6, -0.7, 0.0]))
        under2 = MathTex(r"\div\,(1 - K/N_{\text{eff}})", font_size=28, color=RED)
        under2.move_to(np.array([0.0, -0.7, 0.0]))
        under3 = Text("declares: optimized", font_size=26, color=RED)
        under3.move_to(np.array([3.6, -0.7, 0.0]))
        clock.play(FadeIn(under1), FadeIn(under2), FadeIn(under3), run_time=0.8)
        clock.wait(1.5)

        closing_text = Text("the correction lives where the selection happened", font_size=30, color=WHITE)
        closing_text.move_to(np.array([0.0, -2.4, 0.0]))
        clock.play(FadeIn(closing_text), run_time=1.4)
        clock.wait(2.5)

        clock.play(
            FadeOut(VGroup(pipeline, label1, label2, label3, under1, under2, under3, closing_text, corner_title)),
            run_time=1.0,
        )
        clock.end_beat(8)
