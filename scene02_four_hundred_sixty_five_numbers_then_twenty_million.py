from manim import *
from teachme_manim import BeatClock
import numpy as np

YELLOW = "#F4D345"
BLUE = "#58C4DD"
GREY_B = "#CCCCCC"
RED = "#FC6255"
GREEN = "#83C167"
GOLD = "#F0AC5F"
WHITE = "#FFFFFF"

BEATS = [5.65, 6.93, 7.83, 6.53, 6.35, 5.43, 7.03, 6.5, 5.75, 8.65, 8.08, 9.03, 4.68]


def make_grid(n, side, spacing, center, stroke_w, fill_op, color):
    buff = spacing - side
    cells = VGroup(*[
        Square(side_length=side, stroke_color=color, stroke_width=stroke_w,
               fill_color=color, fill_opacity=fill_op)
        for _ in range(n * n)
    ])
    cells.arrange_in_grid(rows=n, cols=n, buff=buff)
    cells.move_to(center)
    return cells


def make_portfolio_grid():
    side = 0.44
    spacing = 0.66
    buff = spacing - side
    squares = VGroup(*[
        Square(side_length=side, stroke_color=BLUE, stroke_width=2,
               fill_color=BLUE, fill_opacity=0.12)
        for _ in range(30)
    ])
    squares.arrange_in_grid(rows=5, cols=6, buff=buff)
    yellow_square = squares[-1]
    yellow_square.set_stroke(color=YELLOW, width=3)
    yellow_square.set_fill(color=YELLOW, opacity=0.30)
    squares.scale(0.55)
    squares.move_to([-4.30, 0.40, 0])
    return squares, yellow_square


def hatch_cell(cell, color, n=3):
    s = cell.width
    c = cell.get_center()
    lines = VGroup()
    for off in np.linspace(-0.28, 0.28, n) * s:
        p1 = c + np.array([-0.42 * s, -0.42 * s + off, 0])
        p2 = c + np.array([0.42 * s, 0.42 * s + off, 0])
        lines.add(Line(p1, p2, color=color, stroke_width=1.5))
    return lines


class TeachScene(Scene):
    def construct(self):
        np.random.seed(3)
        self.camera.background_color = "#0e1015"
        clock = BeatClock(self, BEATS)

        # ---------- Beat 0: measure the stocks instead ----------
        title = Text("Measure the stocks instead", font_size=44, color=WHITE)
        title.move_to([0, 3.10, 0])
        clock.play(FadeIn(title), run_time=1.2)

        portfolio_grid, yellow_square = make_portfolio_grid()
        clock.play(FadeIn(portfolio_grid), run_time=1.0)

        clock.wait(1.5)
        clock.end_beat(0)

        # ---------- Beat 1: the covariance matrix formula and object ----------
        formula = MathTex(r"\sigma_p", r"=\sqrt{", r"w^T ", r"\Sigma ", r"w", r"}",
                           font_size=48)
        formula[0].set_color(WHITE)
        formula[1].set_color(WHITE)
        formula[2].set_color(YELLOW)
        formula[3].set_color(BLUE)
        formula[4].set_color(YELLOW)
        formula[5].set_color(WHITE)
        formula.move_to([1.40, 1.90, 0])

        clock.play(Write(formula[0]), run_time=0.3)
        clock.wait(0.4)
        clock.play(Write(formula[1]), run_time=0.3)
        clock.wait(0.4)
        clock.play(Write(formula[2]), run_time=0.3)
        clock.wait(0.4)
        clock.play(Write(formula[3]), run_time=0.3)
        clock.wait(0.4)
        clock.play(Write(formula[4]), run_time=0.3)
        self.add(formula[5])

        matrix_cells = make_grid(12, 0.22, 0.24, [1.40, -1.15, 0],
                                  stroke_w=1, fill_op=0.10, color=BLUE)
        clock.play(
            LaggedStart(*[FadeIn(c) for c in matrix_cells], lag_ratio=0.01),
            run_time=1.5,
        )

        arrow = CurvedArrow(yellow_square.get_right(), np.array([-0.20, -1.15, 0]),
                             angle=-0.6, color=GREY_B, stroke_width=3)
        clock.play(Create(arrow), run_time=0.8)

        clock.end_beat(1)

        # ---------- Beat 2: 465 distinct numbers ----------
        n = 12
        upper_cells = [matrix_cells[r * n + c] for r in range(n) for c in range(n) if c >= r]
        lower_cells = [matrix_cells[r * n + c] for r in range(n) for c in range(n) if c < r]
        upper_group = VGroup(*upper_cells)
        lower_group = VGroup(*lower_cells)

        clock.play(
            upper_group.animate.set_fill(opacity=0.45),
            lower_group.animate.set_fill(opacity=0.05),
            run_time=1.2,
        )

        count_label = Text("465 distinct numbers", font_size=34, color=BLUE)
        count_label.move_to([1.40, -3.05, 0])
        clock.play(FadeIn(count_label), run_time=0.8)

        clock.wait(2.0)
        clock.end_beat(2)

        # ---------- Beat 3: 465 parameters vs 3,120 observations ----------
        clock.play(FadeOut(portfolio_grid), FadeOut(arrow), run_time=0.6)

        bar_top = Rectangle(width=1.05, height=0.55, fill_color=BLUE, fill_opacity=0.9,
                             stroke_width=0)
        bar_top.move_to([-4.6 + 1.05 / 2, 0.55, 0])
        label_top = Text("465 parameters", font_size=30, color=WHITE)
        label_top.move_to([-3.30 + label_top.width / 2, 0.55, 0])

        bar_bottom = Rectangle(width=7.10, height=0.55, fill_color=GREEN, fill_opacity=0.9,
                                stroke_width=0)
        bar_bottom.move_to([-4.6 + 7.10 / 2, -0.55, 0])
        label_bottom = Text("3,120 observations", font_size=30, color=WHITE)
        label_bottom.move_to([2.60, -0.05, 0])

        clock.play(GrowFromEdge(bar_top, LEFT), FadeIn(label_top), run_time=0.6)
        clock.play(GrowFromEdge(bar_bottom, LEFT), FadeIn(label_bottom), run_time=0.6)

        check = Text("✓", color=GREEN)
        check.scale_to_fit_height(0.7)
        check.move_to([5.10, 0.0, 0])
        clock.play(FadeIn(check), run_time=0.5)

        clock.wait(2.0)
        clock.end_beat(3)

        # ---------- Beat 4: the six-week-old name has no history ----------
        clock.play(
            FadeOut(bar_top), FadeOut(bar_bottom), FadeOut(label_top),
            FadeOut(label_bottom), FadeOut(check), FadeOut(count_label),
            run_time=0.6,
        )

        clock.play(matrix_cells.animate.move_to([0, -0.20, 0]).scale(1.35), run_time=1.0)

        centers = [c.get_center() for c in matrix_cells]
        min_y = min(ctr[1] for ctr in centers)
        max_x = max(ctr[0] for ctr in centers)
        last_row = [c for c, ctr in zip(matrix_cells, centers) if abs(ctr[1] - min_y) < 1e-2]
        last_col = [c for c, ctr in zip(matrix_cells, centers) if abs(ctr[0] - max_x) < 1e-2]
        combined = last_row + last_col
        seen = set()
        unique_cells = []
        for c in combined:
            if id(c) not in seen:
                seen.add(id(c))
                unique_cells.append(c)
        highlight_group = VGroup(*unique_cells)
        remaining_cells = [c for c in matrix_cells if id(c) not in seen]
        remaining_group = VGroup(*remaining_cells)

        hatch_group = VGroup(*[hatch_cell(c, RED) for c in unique_cells])

        clock.play(
            highlight_group.animate.set_stroke(RED, width=2).set_fill(opacity=0.0),
            Create(hatch_group),
            run_time=1.3,
        )

        six_obs_text = Text("6 observations", font_size=34, color=RED)
        six_obs_text.move_to([0, 2.50, 0])
        clock.play(FadeIn(six_obs_text), run_time=0.8)

        arrow_start_y = formula.get_bottom()[1] - 0.15
        six_obs_arrow = Arrow([0, arrow_start_y, 0], [2.05, 0.95, 0], color=RED, stroke_width=4)
        clock.play(Create(six_obs_arrow), run_time=0.5)

        clock.wait(1.8)
        clock.end_beat(4)

        # ---------- Beat 5: stop, or drop 1/30 of the money ----------
        new_title = Text("stop, or drop 1/30 of the money", font_size=40, color=RED)
        new_title.move_to([0, 3.10, 0])
        clock.play(ReplacementTransform(title, new_title), run_time=1.2)

        clock.play(FadeOut(highlight_group), FadeOut(hatch_group), run_time=1.0)

        clock.wait(2.5)
        clock.end_beat(5)

        # ---------- Beat 6: a single number, no attribution ----------
        restored_title = Text("Measure the stocks instead", font_size=32, color=WHITE)
        restored_title.move_to([0, 3.10, 0])
        clock.play(
            FadeOut(six_obs_text), FadeOut(six_obs_arrow),
            ReplacementTransform(new_title, restored_title),
            run_time=0.8,
        )

        big_text = Text("15.1%", font_size=72, color=WHITE)
        big_text.move_to([0, 0.30, 0])
        clock.play(ReplacementTransform(remaining_group, big_text), run_time=1.5)

        bet_text = Text("which shared bet?", font_size=34, color=RED)
        bet_text.move_to([0, -1.60, 0])
        clock.play(FadeIn(bet_text), run_time=0.8)

        clock.wait(2.0)
        clock.end_beat(6)

        # ---------- Beat 7: now the whole market ----------
        clock.play(FadeOut(big_text), FadeOut(bet_text), FadeOut(formula), run_time=0.6)

        market_title = Text("Now the whole market", font_size=40, color=WHITE)
        market_title.move_to([0, 3.10, 0])
        clock.play(ReplacementTransform(restored_title, market_title), run_time=1.0)

        dense_grid = make_grid(60, 0.055, 0.058, [0, -0.20, 0],
                                stroke_w=0.4, fill_op=0.18, color=BLUE)
        clock.play(FadeIn(dense_grid), run_time=1.5)

        names_label = Text("6,307 names", font_size=34, color=BLUE)
        names_label.move_to([0, -3.10, 0])
        clock.play(FadeIn(names_label), run_time=0.8)

        clock.wait(1.0)
        clock.end_beat(7)

        # ---------- Beat 8: 19,892,278 numbers to estimate ----------
        counter_tracker = ValueTracker(465)
        counter = always_redraw(lambda: DecimalNumber(
            counter_tracker.get_value(), num_decimal_places=0, group_with_commas=True,
            font_size=60, color=WHITE,
        ).move_to([0, 2.10, 0]))
        clock.play(FadeIn(counter), run_time=0.2)

        clock.play(counter_tracker.animate.set_value(19892278), run_time=3.0, rate_func=linear)

        clock.wait(2.4)
        clock.end_beat(8)

        # ---------- Beat 9: 0.1 observations per parameter ----------
        self.remove(counter)
        final_counter = DecimalNumber(19892278, num_decimal_places=0, group_with_commas=True,
                                       font_size=60, color=WHITE)
        final_counter.move_to([0, 2.10, 0])
        self.add(final_counter)

        clock.play(
            FadeOut(dense_grid), FadeOut(names_label), FadeOut(final_counter),
            run_time=0.8,
        )

        bar_params = Rectangle(width=10.6, height=0.60, fill_color=RED, fill_opacity=0.9,
                                stroke_width=0)
        bar_params.move_to([-5.4 + 10.6 / 2, 0.55, 0])
        label_params = Text("19,892,278 parameters", font_size=30, color=WHITE)
        label_params.move_to([0.0, 1.35, 0])

        bar_obs = Rectangle(width=1.06, height=0.60, fill_color=GREEN, fill_opacity=0.9,
                             stroke_width=0)
        bar_obs.move_to([-5.4 + 1.06 / 2, -0.75, 0])
        label_obs = Text("1,977,862 observations", font_size=30, color=WHITE)
        label_obs.move_to([0.0, -1.55, 0])
        if label_obs.get_right()[0] > 6.2:
            label_obs.move_to([-5.4 + label_obs.width / 2, -1.55, 0])

        clock.play(GrowFromEdge(bar_params, LEFT), FadeIn(label_params), run_time=0.75)
        clock.play(GrowFromEdge(bar_obs, LEFT), FadeIn(label_obs), run_time=0.75)

        ratio_text = Text("0.1 observations per parameter", font_size=38, color=RED)
        ratio_text.move_to([0, -2.80, 0])
        clock.play(FadeIn(ratio_text), run_time=1.0)

        clock.wait(2.0)
        clock.end_beat(9)

        # ---------- Beat 10: more years do not rescue this ----------
        clock.play(
            FadeOut(bar_params), FadeOut(bar_obs), FadeOut(label_params), FadeOut(label_obs),
            FadeOut(ratio_text),
            run_time=0.7,
        )

        axis_line = Line([-5.4, -1.80, 0], [5.4, -1.80, 0], color=GREY_B, stroke_width=3)
        ticks = VGroup(*[
            Line([x, -1.85, 0], [x, -1.75, 0], color=GREY_B, stroke_width=2)
            for x in (-5.4, 0.0, 5.4)
        ])
        year_labels = VGroup(*[
            Text(t, font_size=26, color=GREY_B).move_to([x, -2.10, 0])
            for t, x in [("2006", -5.4), ("2016", 0.0), ("2026", 5.4)]
        ])
        clock.play(Create(axis_line), Create(ticks), FadeIn(year_labels), run_time=0.8)

        xs = np.linspace(-5.4, 5.4, 60)
        t_frac = (xs + 5.4) / 10.8
        ys_n = -1.30 + 1.90 * (t_frac ** 1.4)
        ys_n2 = -1.25 + 4.15 * (t_frac ** 3.0)
        blue_curve = VMobject(color=BLUE, stroke_width=4)
        blue_curve.set_points_smoothly([[x, y, 0] for x, y in zip(xs, ys_n)])
        red_curve = VMobject(color=RED, stroke_width=4)
        red_curve.set_points_smoothly([[x, y, 0] for x, y in zip(xs, ys_n2)])
        clock.play(
            LaggedStart(Create(blue_curve), Create(red_curve), lag_ratio=0.2),
            run_time=2.4,
        )

        obs_label = Text("observations", font_size=28, color=BLUE)
        obs_label.move_to([4.20, 0.95, 0])
        param_label = Text("parameters", font_size=28, color=RED)
        param_label.move_to([4.20, 3.20, 0])
        clock.play(FadeIn(obs_label), FadeIn(param_label), run_time=0.6)

        clock.wait(2.0)
        clock.end_beat(10)

        # ---------- Beat 11: the matrix says zero risk ----------
        clock.play(
            FadeOut(blue_curve), FadeOut(red_curve), FadeOut(axis_line), FadeOut(ticks),
            FadeOut(year_labels), FadeOut(obs_label), FadeOut(param_label),
            run_time=0.7,
        )

        flat_line = Line([-4.0, 0.0, 0], [4.0, 0.0, 0], color=GREY_B, stroke_width=3)
        gold_dot = Dot(point=[0, 0.10, 0], radius=0.14, color=GOLD)
        clock.play(Create(flat_line), FadeIn(gold_dot), run_time=0.8)

        zero_text = Text("the matrix says: zero risk", font_size=36, color=RED)
        zero_text.move_to([0, 1.20, 0])
        clock.play(FadeIn(zero_text), run_time=1.0)

        clock.play(Indicate(gold_dot, scale_factor=1.3), run_time=0.4)
        clock.play(gold_dot.animate.shift(UP * 1.2), run_time=0.27)
        clock.play(gold_dot.animate.shift(DOWN * 2.4), run_time=0.27)
        clock.play(gold_dot.animate.shift(UP * 1.2), run_time=0.26)

        clock.wait(1.5)
        clock.end_beat(11)

        # ---------- Beat 12: the wall ----------
        if self.mobjects:
            clock.play(FadeOut(*self.mobjects), run_time=0.8)
        else:
            clock.wait(0.8)

        wall_rect = Rectangle(width=9.0, height=3.6, fill_color=RED, fill_opacity=0.15,
                               stroke_color=RED, stroke_width=4)
        wall_rect.move_to([0, -0.20, 0])
        wall_text = Text("price a risk you cannot measure", font_size=40, color=WHITE)
        wall_text.move_to([0, -0.20, 0])
        wall_group = VGroup(wall_rect, wall_text)

        clock.play(GrowFromEdge(wall_rect, DOWN), run_time=1.5)
        clock.play(FadeIn(wall_text), run_time=1.2)

        clock.wait(1.0)
        clock.end_beat(12)
