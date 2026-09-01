from manim import *
from teachme_manim import BeatClock
import numpy as np

YELLOW = "#F4D345"
BLUE = "#58C4DD"
GREY_B = "#CCCCCC"
RED = "#FC6255"
GREEN = "#83C167"
WHITE = "#FFFFFF"

BEATS = [5.7, 3.95, 7.15, 5.38, 5.98, 5.23, 7.73, 8.23, 6.68, 9.18, 6.2, 7.25,
         9.65, 7.28, 7.53, 11.33, 5.63]


def chip(label, pos):
    box = RoundedRectangle(corner_radius=0.1, width=2.2, height=0.62,
                            stroke_color=BLUE, stroke_width=2,
                            fill_color=BLUE, fill_opacity=0.12)
    box.move_to(pos)
    text = Text(label, font_size=28, color=WHITE)
    text.move_to(pos)
    return VGroup(box, text)


def circle_label(label, pos):
    circ = Circle(radius=0.55, stroke_color=BLUE, stroke_width=3,
                  fill_color=BLUE, fill_opacity=0.15)
    circ.move_to(pos)
    text = Text(label, font_size=22, color=WHITE)
    if text.width > 0.92:
        text.scale_to_fit_width(0.92)
    text.move_to(pos)
    return VGroup(circ, text)


class TeachScene(Scene):
    def construct(self):
        np.random.seed(3)
        self.camera.background_color = "#0e1015"
        clock = BeatClock(self, BEATS)

        # ---------- Beat 0: crack and clear the wall ----------
        wall = Rectangle(width=9.0, height=3.6, fill_color=RED, fill_opacity=0.15,
                          stroke_color=RED, stroke_width=4)
        wall.move_to([0, -0.20, 0])
        wall_text = Text("price a risk you cannot measure", font_size=40, color=WHITE)
        wall_text.move_to([0, -0.20, 0])
        self.add(wall, wall_text)

        crack = VMobject(stroke_color=WHITE, stroke_width=5)
        crack.set_points_as_corners([
            [0.0, 1.60, 0.0], [0.18, 1.05, 0.0], [-0.12, 0.55, 0.0],
            [0.15, 0.05, 0.0], [-0.10, -0.55, 0.0], [0.12, -1.10, 0.0],
            [0.0, -2.00, 0.0],
        ])
        clock.play(Create(crack), run_time=0.8)

        left_half = Rectangle(width=4.5, height=3.6, fill_color=RED, fill_opacity=0.15,
                               stroke_color=RED, stroke_width=4)
        left_half.move_to([-2.25, -0.20, 0])
        right_half = Rectangle(width=4.5, height=3.6, fill_color=RED, fill_opacity=0.15,
                                stroke_color=RED, stroke_width=4)
        right_half.move_to([2.25, -0.20, 0])
        self.remove(wall)
        self.add(left_half, right_half)

        clock.play(
            left_half.animate.move_to([-8.0, -0.20, 0]).set_opacity(0),
            right_half.animate.move_to([8.0, -0.20, 0]).set_opacity(0),
            FadeOut(wall_text),
            FadeOut(crack),
            run_time=1.5,
        )
        self.remove(left_half, right_half)
        clock.end_beat(0)

        # ---------- Beat 1: title ----------
        title = Text("Which characteristics move together", font_size=42, color=WHITE)
        title.move_to([0, 3.10, 0])
        clock.play(Write(title), run_time=1.2)
        clock.wait(2.0)
        clock.end_beat(1)

        # ---------- Beat 2: two utilities share a description, not a wire ----------
        circle_a = circle_label("utility A", [-3.60, 1.30, 0])
        circle_b = circle_label("utility B", [-3.60, -1.30, 0])
        clock.play(FadeIn(circle_a), FadeIn(circle_b), run_time=0.8)

        grey_line = Line([-3.60, 0.75, 0], [-3.60, -0.75, 0], color=GREY_B, stroke_width=4)
        clock.play(Create(grey_line), run_time=0.6)

        red_strike = Line([-3.85, 0.25, 0], [-3.35, -0.25, 0], color=RED, stroke_width=5)
        clock.play(Create(red_strike), FadeOut(grey_line), run_time=0.8)

        chip1 = chip("large", [1.80, 1.40, 0])
        chip2 = chip("low beta", [1.80, 0.00, 0])
        chip3 = chip("high leverage", [1.80, -1.40, 0])
        clock.play(
            LaggedStart(FadeIn(chip1), FadeIn(chip2), FadeIn(chip3), lag_ratio=0.4),
            run_time=1.2,
        )

        starts = [[-3.05, 1.30, 0], [-3.05, -1.30, 0]]
        ends = [[0.70, 1.40, 0], [0.70, 0.00, 0], [0.70, -1.40, 0]]
        links = VGroup(*[Line(s, e, color=BLUE, stroke_width=2) for s in starts for e in ends])
        clock.play(Create(links), run_time=1.5)

        clock.wait(2.0)
        clock.end_beat(2)

        # ---------- Beat 3: shared description ----------
        shared_label = Text("shared description", font_size=32, color=BLUE)
        shared_label.move_to([1.80, 2.45, 0])
        clock.play(Write(shared_label), run_time=0.8)
        clock.wait(3.0)
        clock.end_beat(3)

        # ---------- Beat 4: read off filings and prices, never estimated ----------
        clock.play(
            FadeOut(circle_a), FadeOut(circle_b), FadeOut(links), FadeOut(red_strike),
            FadeOut(shared_label),
            run_time=0.7,
        )

        clock.play(
            chip1.animate.move_to([-3.60, 1.30, 0]).scale(0.8),
            chip2.animate.move_to([-3.60, 0.55, 0]).scale(0.8),
            chip3.animate.move_to([-3.60, -0.20, 0]).scale(0.8),
            run_time=1.0,
        )

        doc_rect = Rectangle(width=1.1, height=1.4, stroke_color=GREY_B, stroke_width=2)
        doc_rect.move_to([2.40, 0.90, 0])
        doc_lines = VGroup(*[
            Line([-0.35, y, 0], [0.35, y, 0], color=GREY_B, stroke_width=2)
            for y in [0.35, 0.0, -0.35]
        ])
        doc_lines.move_to(doc_rect.get_center())
        doc_label = Text("filings", font_size=28, color=GREY_B)
        doc_label.move_to([2.40, -0.05, 0])

        price_rect = Rectangle(width=1.4, height=1.1, stroke_color=GREY_B, stroke_width=2)
        price_rect.move_to([4.60, 0.90, 0])
        price_line = VMobject(stroke_color=GREY_B, stroke_width=3)
        price_line.set_points_as_corners([
            [-0.45, -0.30, 0], [-0.15, 0.05, 0], [0.10, -0.10, 0], [0.45, 0.35, 0],
        ])
        price_line.move_to(price_rect.get_center())
        price_label = Text("prices", font_size=28, color=GREY_B)
        price_label.move_to([4.60, -0.05, 0])

        clock.play(
            FadeIn(doc_rect), FadeIn(doc_lines), FadeIn(doc_label),
            FadeIn(price_rect), FadeIn(price_line), FadeIn(price_label),
            run_time=1.0,
        )

        arrow1 = Arrow([1.85, 0.90, 0], [-2.55, 0.55, 0], color=GREY_B, stroke_width=3, buff=0.0)
        arrow2 = Arrow([3.90, 0.55, 0], [-2.55, 0.55, 0], color=GREY_B, stroke_width=3, buff=0.0)
        clock.play(Create(arrow1), Create(arrow2), run_time=1.0)

        never_label = Text("never estimated from returns", font_size=32, color=WHITE)
        never_label.move_to([0.90, -1.80, 0])
        clock.play(Write(never_label), run_time=1.0)

        clock.wait(1.0)
        clock.end_beat(4)

        # ---------- Beat 5: the six-week-old name, day one ----------
        clock.play(
            FadeOut(doc_rect), FadeOut(doc_lines), FadeOut(doc_label),
            FadeOut(price_rect), FadeOut(price_line), FadeOut(price_label),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(never_label),
            run_time=0.6,
        )

        new_square = Square(side_length=0.44, stroke_color=YELLOW, stroke_width=4,
                             fill_color=YELLOW, fill_opacity=0.30)
        new_square.move_to([2.60, 0.55, 0])
        new_square_label = Text("listed 6 weeks ago", font_size=26, color=YELLOW)
        new_square_label.move_to([2.60, -0.15, 0])
        clock.play(FadeIn(new_square), FadeIn(new_square_label), run_time=0.8)

        point_arrow = Arrow([-2.40, 0.55, 0], [2.25, 0.55, 0], color=YELLOW, stroke_width=4)
        clock.play(Create(point_arrow), run_time=0.8)

        full_desc_label = Text("full description, day one", font_size=30, color=GREEN)
        full_desc_label.move_to([2.60, 1.35, 0])
        clock.play(Write(full_desc_label), run_time=0.8)

        clock.wait(1.0)
        clock.end_beat(5)

        # ---------- Beat 6: forty columns ----------
        clock.play(
            FadeOut(chip1), FadeOut(chip2), FadeOut(chip3),
            FadeOut(new_square), FadeOut(new_square_label),
            FadeOut(point_arrow), FadeOut(full_desc_label),
            run_time=0.7,
        )

        cells = []
        for i in range(40):
            if i == 0:
                color, opacity = GREEN, 0.55
            elif i <= 9:
                color, opacity = BLUE, 0.55
            else:
                color, opacity = BLUE, 0.20
            c = Rectangle(width=0.28, height=0.55, stroke_color=WHITE, stroke_width=1,
                          fill_color=color, fill_opacity=opacity)
            cells.append(c)
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.01)
        cells_group.move_to([0, 1.40, 0])

        clock.play(
            LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02),
            run_time=1.5,
        )

        market_group = VGroup(cells[0])
        style_group = VGroup(*cells[1:10])
        industry_group = VGroup(*cells[10:40])
        market_brace = Brace(market_group, DOWN, buff=0.05)
        style_brace = Brace(style_group, DOWN, buff=0.05)
        industry_brace = Brace(industry_group, DOWN, buff=0.05)

        market_label = Text("1 market", font_size=28, color=GREEN)
        market_label.move_to([-5.52, 0.75, 0])
        style_label = Text("9 style", font_size=28, color=BLUE)
        style_label.move_to([-3.94, 0.75, 0])
        industry_label = Text("30 industry", font_size=28, color=BLUE)
        industry_label.move_to([1.87, 0.75, 0])

        clock.play(
            FadeIn(market_brace), FadeIn(style_brace), FadeIn(industry_brace),
            Write(market_label), Write(style_label), Write(industry_label),
            run_time=0.9,
        )

        style_names = VGroup(
            *[Text(t, font_size=28, color=WHITE).move_to([-2.20, y, 0])
              for t, y in [("size", -0.35), ("value", -0.90), ("growth", -1.45),
                           ("momentum", -2.00), ("beta", -2.55)]],
            *[Text(t, font_size=28, color=WHITE).move_to([1.60, y, 0])
              for t, y in [("volatility", -0.35), ("liquidity", -0.90),
                           ("quality", -1.45), ("leverage", -2.00)]],
        )
        clock.play(LaggedStart(*[FadeIn(t) for t in style_names], lag_ratio=0.15), run_time=1.8)

        clock.wait(1.0)
        clock.end_beat(6)

        # ---------- Beat 7: build the equation, X is known ----------
        clock.play(
            FadeOut(style_names), FadeOut(market_brace), FadeOut(style_brace),
            FadeOut(industry_brace), FadeOut(market_label), FadeOut(style_label),
            FadeOut(industry_label),
            run_time=0.6,
        )

        clock.play(cells_group.animate.move_to([0, 2.30, 0]).scale(0.75), run_time=0.8)

        r_i = MathTex("r_i", font_size=52, color=YELLOW)
        eq_sign = MathTex("=", font_size=52, color=WHITE)
        x_i = MathTex("X_i", font_size=52, color=BLUE)
        dot_f = MathTex(r"\cdot f", font_size=52, color=BLUE)
        plus_eps = MathTex(r"+\varepsilon_i", font_size=52, color=GREY_B)
        eq_group = VGroup(r_i, eq_sign, x_i, dot_f, plus_eps)
        eq_group.arrange(RIGHT, buff=0.18)
        eq_group.move_to([0, 0.40, 0])

        pieces = [r_i, eq_sign, x_i, dot_f, plus_eps]
        for idx_p, piece in enumerate(pieces):
            clock.play(Write(piece), run_time=0.3)
            if idx_p < len(pieces) - 1:
                clock.wait(0.25)

        strip_arrow = Arrow(cells_group.get_bottom(), x_i.get_top(), color=BLUE,
                             stroke_width=3, buff=0.1)
        clock.play(Create(strip_arrow), run_time=0.5)

        clock.wait(1.5)
        clock.end_beat(7)

        # ---------- Beat 8: known versus unknown ----------
        known_label = Text("known", font_size=30, color=BLUE)
        known_label.move_to([-0.55, -0.75, 0])
        known_arrow = Arrow(known_label.get_top(), x_i.get_bottom(), color=BLUE,
                             stroke_width=3, buff=0.1)
        clock.play(Write(known_label), Create(known_arrow), run_time=1.0)

        unknown_label = Text("unknown", font_size=30, color=RED)
        unknown_label.move_to([1.05, -0.75, 0])
        unknown_arrow = Arrow(unknown_label.get_top(), dot_f.get_bottom(), color=RED,
                               stroke_width=3, buff=0.1)
        clock.play(Write(unknown_label), Create(unknown_arrow), run_time=1.0)

        clock.wait(3.0)
        clock.end_beat(8)

        # ---------- Beat 9: run the regression sideways ----------
        clock.play(
            FadeOut(cells_group), FadeOut(strip_arrow), FadeOut(known_label),
            FadeOut(known_arrow), FadeOut(unknown_label), FadeOut(unknown_arrow),
            FadeOut(title),
            run_time=0.6,
        )

        clock.play(eq_group.animate.move_to([0, 3.05, 0]).scale(34 / 52), run_time=0.8)

        return_rect = Rectangle(width=0.50, height=4.0, fill_color=YELLOW, fill_opacity=0.35,
                                 stroke_color=YELLOW, stroke_width=2)
        return_rect.move_to([-4.60, -0.40, 0])
        return_label = Text("2,774 returns", font_size=26, color=YELLOW)
        return_label.rotate(PI / 2)
        return_label.move_to([-5.35, -0.40, 0])

        matrix_rect = Rectangle(width=3.6, height=4.0, fill_color=BLUE, fill_opacity=0.20,
                                 stroke_color=BLUE, stroke_width=2)
        matrix_rect.move_to([-1.20, -0.40, 0])
        rule_xs = np.linspace(-1.8, 1.8, 10)[1:-1]
        matrix_rules = VGroup(*[
            Line([matrix_rect.get_center()[0] + x, -2.40, 0],
                 [matrix_rect.get_center()[0] + x, 1.60, 0],
                 color=BLUE, stroke_width=1, stroke_opacity=0.4)
            for x in rule_xs
        ])
        matrix_label = Text("40 columns", font_size=26, color=BLUE)
        matrix_label.move_to([-1.20, -2.50, 0])

        factor_rect = Rectangle(width=0.50, height=1.0, fill_color=BLUE, fill_opacity=0.55,
                                 stroke_color=BLUE, stroke_width=2)
        factor_rect.move_to([2.30, -0.40, 0])
        factor_label = Text("40 unknowns", font_size=26, color=BLUE)
        factor_label.move_to([2.30, -1.15, 0])

        residual_rect = Rectangle(width=0.50, height=4.0, fill_color=GREY_B, fill_opacity=0.30,
                                   stroke_color=GREY_B, stroke_width=2)
        residual_rect.move_to([4.90, -0.40, 0])

        equals_sign = MathTex("=", font_size=44, color=WHITE).move_to([-2.95, -0.40, 0])
        plus_sign = MathTex("+", font_size=44, color=WHITE).move_to([3.05, -0.40, 0])

        diagram = VGroup(return_rect, return_label, matrix_rect, matrix_rules, matrix_label,
                          factor_rect, factor_label, residual_rect, equals_sign, plus_sign)

        clock.play(
            LaggedStart(
                Create(return_rect), FadeIn(return_label),
                Create(matrix_rect), Create(matrix_rules), FadeIn(matrix_label),
                Create(factor_rect), FadeIn(factor_label),
                Create(residual_rect), Write(equals_sign), Write(plus_sign),
                lag_ratio=0.12,
            ),
            run_time=2.5,
        )

        clock.wait(1.5)
        clock.end_beat(9)

        # ---------- Beat 10: one day, 2,774 equations, 40 unknowns ----------
        one_day = Text("one day", font_size=36, color=WHITE)
        one_day.move_to([0, -3.15, 0])
        clock.play(Write(one_day), run_time=0.8)

        clock.play(Indicate(diagram, scale_factor=1.03), run_time=0.8)

        equations_text = Text("2,774 equations, 40 unknowns", font_size=36, color=GREEN)
        equations_text.move_to([0, -3.15, 0])
        clock.play(ReplacementTransform(one_day, equations_text), run_time=1.2)

        clock.wait(2.5)
        clock.end_beat(10)

        # ---------- Beat 11: five points, one style column ----------
        clock.play(FadeOut(diagram), FadeOut(equations_text), run_time=0.8)

        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-1.5, 2.5, 1],
            x_length=7.2, y_length=4.0,
            axis_config={"color": GREY_B, "include_tip": False},
            tips=False,
        )
        axes.move_to([0, -0.35, 0])
        x_label = Text("style exposure", font_size=26, color=BLUE)
        x_label.move_to([3.90, -1.95, 0])
        y_label = Text("return, %", font_size=26, color=YELLOW)
        y_label.rotate(PI / 2)
        y_label.move_to([-4.15, -0.35, 0])
        clock.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)

        data = [("A", 2.0, 2.0), ("B", 1.0, 0.4), ("C", 0.0, 1.4),
                ("D", -1.0, -0.6), ("E", -2.0, 0.3)]
        dots = VGroup()
        letters = VGroup()
        for name, x, y in data:
            d = Dot(axes.c2p(x, y), radius=0.10, color=YELLOW)
            lbl = Text(name, font_size=24, color=WHITE)
            lbl.move_to(axes.c2p(x, y) + np.array([0, 0.35, 0]))
            dots.add(d)
            letters.add(lbl)
        clock.play(LaggedStart(*[FadeIn(VGroup(d, l)) for d, l in zip(dots, letters)],
                                lag_ratio=0.2), run_time=1.5)

        fit_line = Line(axes.c2p(-2.0, -0.18), axes.c2p(2.0, 1.58), color=BLUE, stroke_width=4)
        clock.play(Create(fit_line), run_time=1.2)

        clock.wait(1.0)
        clock.end_beat(11)

        # ---------- Beat 12: read the intercept and slope ----------
        intercept_dot = Dot(axes.c2p(0.0, 0.70), radius=0.07, color=GREEN)
        intercept_text = Text("0.70% market", font_size=28, color=GREEN)
        intercept_text.move_to([2.05, 2.55, 0])
        clock.play(FadeIn(intercept_dot), Write(intercept_text), run_time=0.8)

        slope_step = VMobject(stroke_color=BLUE, stroke_width=3)
        slope_step.set_points_as_corners([
            axes.c2p(0.0, 0.70), axes.c2p(1.0, 0.70), axes.c2p(1.0, 1.14),
        ])
        slope_text = Text("0.44% per unit of style", font_size=28, color=BLUE)
        slope_text.move_to([2.05, 1.95, 0])
        clock.play(Create(slope_step), Write(slope_text), run_time=1.0)

        clock.wait(2.5)
        clock.end_beat(12)

        # ---------- Beat 13: specific returns ----------
        residuals = [0.42, -0.74, 0.70, -0.86, 0.48]
        exposures = [2.0, 1.0, 0.0, -1.0, -2.0]
        gap_lines = VGroup()
        for x, resid in zip(exposures, residuals):
            fitted_y = 0.70 + 0.44 * x
            actual_y = fitted_y + resid
            gap_lines.add(Line(axes.c2p(x, fitted_y), axes.c2p(x, actual_y),
                               color=GREY_B, stroke_width=3))
        clock.play(LaggedStart(*[Create(l) for l in gap_lines], lag_ratio=0.2), run_time=1.5)

        specific_label = Text("specific returns", font_size=30, color=GREY_B)
        specific_label.move_to([-3.10, 2.55, 0])
        clock.play(Write(specific_label), run_time=0.8)

        clock.wait(2.5)
        clock.end_beat(13)

        # ---------- Beat 14: the cloud, R-squared 0.205 ----------
        clock.play(
            FadeOut(letters), FadeOut(intercept_dot), FadeOut(intercept_text),
            FadeOut(slope_step), FadeOut(slope_text),
            run_time=0.6,
        )

        cloud_xs = np.random.uniform(-2.4, 2.4, 200)
        cloud_noise = np.random.normal(0, 0.55, 200)
        cloud_ys = np.clip(0.70 + 0.44 * cloud_xs + cloud_noise, -1.45, 2.45)
        cloud = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.035, color=GREY_B, fill_opacity=0.45)
            for x, y in zip(cloud_xs, cloud_ys)
        ])
        clock.play(LaggedStart(*[FadeIn(d) for d in cloud], lag_ratio=0.01), run_time=2.0)

        r2_label = Text("mean daily R-squared = 0.205", font_size=34, color=WHITE)
        r2_label.move_to([0, -3.15, 0])
        clock.play(Write(r2_label), run_time=1.0)

        clock.wait(2.0)
        clock.end_beat(14)

        # ---------- Beat 15: which factors are significant ----------
        clock.play(
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(dots),
            FadeOut(fit_line), FadeOut(gap_lines), FadeOut(specific_label),
            FadeOut(cloud), FadeOut(r2_label),
            run_time=0.8,
        )

        rows = [
            ("market", 87.0, BLUE), ("beta", 83.7, BLUE), ("momentum", 75.0, BLUE),
            ("volatility", 73.9, BLUE), ("liquidity", 62.0, BLUE), ("quality", 49.2, BLUE),
            ("leverage", 47.2, BLUE), ("growth", 41.8, BLUE), ("value", 11.7, BLUE),
            ("dividend yield", 0.0, RED),
        ]
        row_ys = np.linspace(2.55, -2.65, len(rows))

        bar_items = []
        for (name, pct, color), y in zip(rows, row_ys):
            width = max(pct / 100.0 * 6.6, 0.001)
            bar = Rectangle(width=width, height=0.34, fill_color=color, fill_opacity=0.85,
                            stroke_opacity=0.0)
            bar.move_to([-1.40 + width / 2.0, y, 0])
            row_label = Text(name, font_size=26, color=WHITE)
            row_label.move_to([-1.60 - row_label.width / 2.0, y, 0])
            value_label = Text(f"{pct:g}%", font_size=24, color=color)
            value_label.next_to(bar, RIGHT, buff=0.15)
            bar_items.append((bar, row_label, value_label))

        clock.play(
            LaggedStart(*[
                AnimationGroup(FadeIn(rl), GrowFromEdge(bar, LEFT), FadeIn(vl))
                for bar, rl, vl in bar_items
            ], lag_ratio=0.08),
            run_time=2.5,
        )

        div_bar, div_label, div_value = bar_items[-1]
        strike_line = Line(
            [div_label.get_left()[0] - 0.05, row_ys[-1], 0],
            [div_value.get_right()[0] + 0.05, row_ys[-1], 0],
            color=RED, stroke_width=3,
        )
        clock.play(Create(strike_line), run_time=0.6)

        clock.wait(2.0)
        clock.end_beat(15)

        # ---------- Beat 16: every stock has a description ----------
        all_bars = VGroup(*[VGroup(*item) for item in bar_items])
        clock.play(FadeOut(all_bars), FadeOut(strike_line), run_time=0.8)

        line1 = Text("Every stock has a description.", font_size=38, color=WHITE)
        line1.move_to([0, 0.50, 0])
        clock.play(Write(line1), run_time=1.2)

        line2 = Text("None of it came from that stock's history.", font_size=38, color=GREY_B)
        line2.move_to([0, -0.40, 0])
        clock.play(Write(line2), run_time=1.2)

        clock.end_beat(16)
