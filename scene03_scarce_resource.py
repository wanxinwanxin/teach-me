import numpy as np
from manim import *
from teachme_manim import BeatClock

GOLD = "#F0AC5F"
GREEN = "#83C167"
BLUE = "#58C4DD"
YELLOW = "#F4D345"
RED = "#FC6255"
GREY_B = "#CCCCCC"

BEATS = [9.37, 9.22, 11.57, 8.76, 8.25, 20.39, 13.03, 9.53, 14.06, 8.97]


class TeachScene(Scene):
    def construct(self):
        self.camera.background_color = "#0e1015"
        np.random.seed(3)
        clock = BeatClock(self, BEATS)

        # ---------- Beat 0: title, axes, 84-day curve, half-life equation ----------
        title = Text("The scarce resource", font_size=44, color=WHITE).move_to([0, 3.1, 0])
        clock.play(Write(title), run_time=1.0)

        axes = Axes(
            x_range=[0, 400, 100],
            y_range=[0, 1.05, 0.25],
            x_length=8.4,
            y_length=4.0,
            axis_config={"color": WHITE, "include_tip": False, "stroke_width": 2},
        ).move_to([0.2, -0.4, 0])

        x_label = Text("days ago", font_size=28, color=WHITE).move_to([0.2, -2.7, 0])
        y_label = Text("weight", font_size=28, color=WHITE).rotate(90 * DEGREES).move_to([-4.5, -0.4, 0])

        clock.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.5)

        curve_84 = axes.plot(lambda x: 2 ** (-x / 84), x_range=[0, 400], color=GOLD)
        label_84 = Text("84-day half-life", font_size=28, color=GOLD).move_to([1.0, 1.0, 0])
        clock.play(Create(curve_84), run_time=1.5)
        clock.play(FadeIn(label_84), run_time=0.5)

        lambda_eq = MathTex(r"\lambda = 2^{-1/h}", font_size=34, color=WHITE).move_to([3.4, 2.3, 0])
        clock.play(Write(lambda_eq), run_time=0.8)
        clock.wait(1.0)
        clock.end_beat(0)

        # ---------- Beat 1: 252-day curve, N_eff equation, 242 / 727 ----------
        curve_252 = axes.plot(lambda x: 2 ** (-x / 252), x_range=[0, 400], color=GREEN)
        label_252 = Text("252-day half-life", font_size=28, color=GREEN).move_to([2.4, 0.2, 0])
        clock.play(Create(curve_252), run_time=1.5)
        clock.play(FadeIn(label_252), run_time=0.5)

        neff_eq = MathTex(r"N_{\text{eff}} = \frac{1+\lambda}{1-\lambda}", font_size=34, color=WHITE).move_to(
            [3.4, 2.3, 0]
        )
        clock.play(ReplacementTransform(lambda_eq, neff_eq), run_time=1.2)

        text_242 = Text("242", font_size=34, color=GOLD).move_to([5.4, 1.0, 0])
        text_727 = Text("727", font_size=34, color=GREEN).move_to([5.4, 0.2, 0])
        clock.play(FadeIn(text_242), FadeIn(text_727), run_time=0.6)
        clock.wait(1.5)
        clock.end_beat(1)

        # ---------- Beat 2: a decade of history changes nothing ----------
        p1 = axes.c2p(252, 0)
        p2 = axes.c2p(400, 1.05)
        history_rect = Polygon(
            p1,
            np.array([p2[0], p1[1], 0]),
            p2,
            np.array([p1[0], p2[1], 0]),
            fill_color=GREY_B,
            fill_opacity=0.22,
            stroke_width=0,
        )
        clock.play(FadeIn(history_rect), run_time=1.0)

        decade_text = Text("a decade more history changes nothing", font_size=28, color=GREY_B).move_to(
            [0, -3.3, 0]
        )
        clock.play(FadeIn(decade_text), run_time=0.6)
        clock.wait(2.5)
        clock.end_beat(2)

        # ---------- Beat 3: clear the plot, build F = V C V ----------
        cleanup = VGroup(
            axes,
            x_label,
            y_label,
            curve_84,
            curve_252,
            label_84,
            label_252,
            text_242,
            text_727,
            history_rect,
            decade_text,
        )
        clock.play(FadeOut(cleanup), run_time=1.2)

        title_small = Text("The scarce resource", font_size=30, color=WHITE).move_to([-4.7, 3.25, 0])
        clock.play(ReplacementTransform(title, title_small), run_time=1.0)
        title = title_small

        clock.play(neff_eq.animate.move_to([4.6, 3.1, 0]).scale(28 / 34), run_time=0.8)

        fvcv = MathTex("F", "=", "V", "C", "V").scale(1.5).move_to([0, 2.1, 0])
        fvcv_colors = {0: BLUE, 2: GOLD, 3: GREEN, 4: GOLD}
        for idx, col in fvcv_colors.items():
            fvcv[idx].set_color(col)
            fvcv[idx].set_stroke(color=col, width=0)

        clock.play(Write(VGroup(fvcv[0], fvcv[1])), run_time=0.6)
        clock.play(Write(fvcv[2]), run_time=0.6)
        clock.play(Write(fvcv[3]), run_time=0.6)
        clock.play(Write(fvcv[4]), run_time=0.6)
        clock.end_beat(3)

        # ---------- Beat 4: the 40x40 matrix, split into variances and correlations ----------
        cell = 3.4 / 20
        left, right, top, bottom = -1.7, 1.7, 1.0, -2.4

        square = Square(side_length=3.4, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to([0, -0.7, 0])
        grid_lines = VGroup()
        for i in range(1, 20):
            y = top - i * cell
            grid_lines.add(Line([left, y, 0], [right, y, 0], stroke_color=GREY_B, stroke_width=1, stroke_opacity=0.2))
        for i in range(1, 20):
            x = left + i * cell
            grid_lines.add(Line([x, top, 0], [x, bottom, 0], stroke_color=GREY_B, stroke_width=1, stroke_opacity=0.2))

        clock.play(Create(square), Create(grid_lines), run_time=0.8)

        diag_squares = VGroup()
        for k in range(20):
            cx = left + cell * (k + 0.5)
            cy = top - cell * (k + 0.5)
            diag_squares.add(
                Square(side_length=cell, fill_color=GOLD, fill_opacity=0.85, stroke_width=0).move_to([cx, cy, 0])
            )
        label_var = Text("40 variances", font_size=28, color=GOLD).move_to([-3.6, 0.6, 0])
        clock.play(FadeIn(diag_squares), run_time=1.0)
        clock.play(FadeIn(label_var), run_time=0.4)
        clock.wait(0.3)

        triangle_group = VGroup()
        for r in range(19):
            x0 = left + cell * (r + 1)
            x1 = right
            y0 = top - cell * (r + 1)
            y1 = top - cell * r
            width = x1 - x0
            rect = Rectangle(width=width, height=cell, fill_color=GREEN, fill_opacity=0.35, stroke_width=0).move_to(
                [(x0 + x1) / 2, (y0 + y1) / 2, 0]
            )
            triangle_group.add(rect)
        label_corr = Text("780 correlations", font_size=28, color=GREEN).move_to([3.6, 0.6, 0])
        clock.play(FadeIn(triangle_group), run_time=1.3)
        clock.play(FadeIn(label_corr), run_time=0.4)
        clock.wait(0.3)

        text_ratio = Text("20 to 1", font_size=32, color=WHITE).move_to([0, -2.9, 0])
        clock.play(FadeIn(text_ratio), run_time=0.5)
        clock.wait(3.0)
        clock.end_beat(4)

        # ---------- Beat 5: split into volatility clock and correlation clock ----------
        clock.wait(0.6)
        clock.play(FadeOut(VGroup(label_var, label_corr, text_ratio)), run_time=0.8)

        calm1 = np.random.normal(0, 0.05, 15)
        violent = np.random.normal(0, 0.45, 12)
        calm2 = np.random.normal(0, 0.05, 15)
        vol_vals = np.clip(np.concatenate([calm1, violent, calm2]), -0.75, 0.75)
        xs1 = np.linspace(-2.2, 2.2, len(vol_vals))
        points1 = [np.array([-3.2 + x, -0.6 + y, 0]) for x, y in zip(xs1, vol_vals)]
        vol_line = VMobject(stroke_color=GOLD, stroke_width=3, fill_opacity=0, stroke_opacity=1)
        vol_line.set_points_as_corners(points1)

        t = np.linspace(0, 1, 90)
        smooth_vals = np.clip(0.35 * np.sin(2 * np.pi * t) + 0.15 * t, -0.75, 0.75)
        xs2 = np.linspace(-2.2, 2.2, 90)
        points2 = [np.array([3.2 + x, -0.6 + y, 0]) for x, y in zip(xs2, smooth_vals)]
        smooth_line = VMobject(stroke_color=GREEN, stroke_width=3, fill_opacity=0, stroke_opacity=1)
        smooth_line.set_points_as_corners(points2)

        # Hold the finished matrix, then fade it out entirely before fading in
        # the two panels — a direct ReplacementTransform between a ~400-piece
        # grid and two simple line plots produces unreadable scribble frames.
        matrix_group = VGroup(square, grid_lines, diag_squares, triangle_group)
        clock.play(FadeOut(matrix_group), run_time=1.0)

        label_left_bottom = Text("clusters, moves fast", font_size=28, color=GOLD).move_to([-3.2, -2.3, 0])
        label_left_top = Text("84 days", font_size=30, color=GOLD).move_to([-3.2, 1.0, 0])
        label_right_bottom = Text("drifts slowly", font_size=28, color=GREEN).move_to([3.2, -2.3, 0])
        label_right_top = Text("252 days", font_size=30, color=GREEN).move_to([3.2, 1.0, 0])
        panels_group = VGroup(
            vol_line, smooth_line, label_left_bottom, label_left_top, label_right_bottom, label_right_top
        )
        clock.play(FadeIn(panels_group), run_time=1.2)
        clock.wait(2.0)

        psd_eq = MathTex(
            r"V \succ 0,\; C \succeq 0 \;\Rightarrow\; VCV \succeq 0", font_size=30, color=WHITE
        ).move_to([0, -3.1, 0])
        clock.play(FadeIn(psd_eq), run_time=1.2)
        clock.wait(1.5)
        clock.end_beat(5)

        # ---------- Beat 6: the weekly model's bar chart ----------
        clock.play(
            FadeOut(
                VGroup(
                    vol_line,
                    smooth_line,
                    label_left_bottom,
                    label_left_top,
                    label_right_bottom,
                    label_right_top,
                    psd_eq,
                    neff_eq,
                )
            ),
            run_time=1.2,
        )
        clock.play(fvcv.animate.move_to([4.8, 3.1, 0]).scale(30 / 72), run_time=0.6)

        # correlations stay GREEN throughout the video (same concept as C in F=VCV)
        corr_bar = Rectangle(width=6.4, height=0.7, fill_color=GREEN, fill_opacity=0.8, stroke_width=0).move_to(
            [-4.4 + 6.4 / 2, 1.1, 0]
        )
        clock.play(GrowFromEdge(corr_bar, LEFT), run_time=1.0)
        corr_label = Text("780 correlations", font_size=30, color=GREEN).next_to(
            np.array([6.0, 1.1, 0]), LEFT, buff=0.0
        )
        clock.play(FadeIn(corr_label), run_time=0.4)

        yellow_bar = Rectangle(width=0.62, height=0.7, fill_color=YELLOW, fill_opacity=1.0, stroke_width=0).move_to(
            [-4.4 + 0.62 / 2, -0.4, 0]
        )
        clock.play(GrowFromEdge(yellow_bar, LEFT), run_time=1.0)
        label_obs = Text("75 observations", font_size=30, color=YELLOW).move_to([-2.0, -0.4, 0])
        clock.play(FadeIn(label_obs), run_time=0.4)

        weekly_text = Text("weekly, 26-week half-life", font_size=28, color=GREY_B).move_to([0, 2.3, 0])
        clock.play(FadeIn(weekly_text), run_time=0.5)
        clock.wait(2.5)
        clock.end_beat(6)

        # ---------- Beat 7: exposures frozen Friday ----------
        frozen_text = Text(
            "exposures frozen Friday, five regressions a week", font_size=28, color=WHITE
        ).move_to([0, -2.0, 0])
        clock.play(FadeIn(frozen_text), run_time=1.0)
        clock.wait(1.5)
        clock.end_beat(7)

        # ---------- Beat 8: 75 becomes 727, bias and slope heal ----------
        label_obs_new = Text("727 observations", font_size=30, color=YELLOW).next_to(
            np.array([6.0, -0.4, 0]), LEFT, buff=0.0
        )
        clock.play(
            yellow_bar.animate.stretch_to_fit_width(6.0, about_edge=LEFT),
            ReplacementTransform(label_obs, label_obs_new),
            run_time=2.0,
        )
        clock.wait(1.0)

        # weekly_text ('weekly, 26-week half-life') stays on screen until the
        # final FadeOut at the end of the scene, per the storyboard.
        clock.play(
            FadeOut(VGroup(corr_bar, yellow_bar, corr_label, label_obs_new, frozen_text)), run_time=0.8
        )

        bias_label = Text("min-variance bias", font_size=28, color=GREY_B).move_to([0, 1.5, 0])
        clock.play(FadeIn(bias_label), run_time=0.4)
        bias_eq = MathTex("1.36", r"\longrightarrow", "1.088", color=WHITE).scale(1.1).move_to([0, 0.6, 0])
        bias_eq[0].set_color(RED)
        clock.play(Write(bias_eq), run_time=1.2)

        slope_label = Text("forecast slope", font_size=28, color=GREY_B).move_to([0, -0.3, 0])
        clock.play(FadeIn(slope_label), run_time=0.4)
        slope_eq = MathTex("0.81", r"\longrightarrow", "1.02", color=WHITE).scale(1.1).move_to([0, -1.0, 0])
        slope_eq[0].set_color(RED)
        clock.play(Write(slope_eq), run_time=1.2)
        clock.wait(2.0)
        clock.end_beat(8)

        # ---------- Beat 9: sampling rate beats every matrix adjustment ----------
        clock.play(FadeOut(VGroup(bias_label, bias_eq, slope_label, slope_eq)), run_time=0.8)

        adj_bar = Rectangle(width=1.0, height=0.6, fill_color=GREY_B, fill_opacity=1.0, stroke_width=0).move_to(
            [-3.0 + 1.0 / 2, 0.8, 0]
        )
        clock.play(GrowFromEdge(adj_bar, LEFT), run_time=0.8)
        adj_label = Text("best matrix adjustment: 0.07", font_size=28, color=GREY_B).move_to([1.4, 0.8, 0])
        clock.play(FadeIn(adj_label), run_time=0.4)

        sample_bar = Rectangle(width=3.86, height=0.6, fill_color=YELLOW, fill_opacity=1.0, stroke_width=0).move_to(
            [-3.0 + 3.86 / 2, -0.6, 0]
        )
        clock.play(GrowFromEdge(sample_bar, LEFT), run_time=0.8)
        sample_label = Text("sampling rate: 0.27", font_size=28, color=YELLOW).move_to([2.4, -0.6, 0])
        clock.play(FadeIn(sample_label), run_time=0.4)
        clock.wait(2.5)

        clock.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        clock.end_beat(9)
