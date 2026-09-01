from manim import *
from teachme_manim import BeatClock
import numpy as np

YELLOW = "#F4D345"
BLUE = "#58C4DD"
GREY_B = "#CCCCCC"
RED = "#FC6255"
GREEN = "#83C167"
GOLD = "#F0AC5F"
TEAL = "#5CD0B3"
WHITE = "#FFFFFF"

BEATS = [5.73, 6.25, 6.83, 7.45, 6.25, 8.28, 5.05, 5.4, 6.28, 4.6, 7.98, 4.55, 6.43, 3.85,
         7.53, 7.0, 5.7, 12.98, 8.65, 8.93, 6.93, 4.58, 7.03, 7.78, 8.9, 11.08]

GRID_COL_XS = [-1.65, -0.99, -0.33, 0.33, 0.99, 1.65]
GRID_ROW_YS = [1.67, 1.01, 0.35, -0.31, -0.97]


def mk_text(s, font_size, color, max_width=11.8):
    t = Text(s, font_size=font_size, color=color)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def clamp_width(mobj, max_width=11.8):
    if mobj.width > max_width:
        mobj.scale_to_fit_width(max_width)
    return mobj


def build_grid():
    squares = VGroup()
    for y in GRID_ROW_YS:
        for x in GRID_COL_XS:
            sq = Square(side_length=0.44, stroke_color=BLUE, stroke_width=2,
                        fill_color=BLUE, fill_opacity=0.12)
            sq.move_to([x, y, 0])
            squares.add(sq)
    squares[-1].set_stroke(color=YELLOW, width=4).set_fill(color=YELLOW, opacity=0.30)
    return squares


def build_mini_icon(center, color):
    icon = VGroup()
    for oy in (-0.20, 0.0, 0.20):
        for ox in (-0.20, 0.0, 0.20):
            sq = Square(side_length=0.16, stroke_color=color, stroke_width=1.5, fill_opacity=0.0)
            sq.move_to([center[0] + ox, center[1] + oy, 0])
            icon.add(sq)
    return icon


class TeachScene(Scene):
    def construct(self):
        self.camera.background_color = "#0e1015"
        np.random.seed(3)
        clock = BeatClock(self, BEATS)

        # ---------- Beat 0: back to the thirty stocks ----------
        title = mk_text("Back to your thirty stocks", 42, WHITE).move_to([0, 3.10, 0])
        clock.play(Write(title), run_time=1.2)

        grid = build_grid().move_to([0, 0.20, 0])
        clock.play(FadeIn(grid), run_time=1.2)
        clock.wait(2.0)
        clock.end_beat(0)

        # ---------- Beat 1: x = X^T w, the portfolio's own description ----------
        clock.play(grid.animate.scale(0.45).move_to([-5.20, 2.30, 0]), run_time=1.0)

        x_tex = MathTex("x", font_size=46, color=WHITE)
        eq_tex = MathTex("=", font_size=46, color=WHITE)
        XT_tex = MathTex("X^T", font_size=46, color=BLUE)
        w_tex = MathTex("w", font_size=46, color=YELLOW)
        exposure_line = VGroup(x_tex, eq_tex, XT_tex, w_tex).arrange(RIGHT, buff=0.25)
        exposure_line.move_to([0, 1.40, 0])

        clock.play(Write(x_tex), run_time=0.3)
        clock.play(Write(eq_tex), run_time=0.3)
        clock.play(Write(XT_tex), run_time=0.5)
        clock.play(Write(w_tex), run_time=0.4)

        caption1 = mk_text("the portfolio's own description", 30, WHITE).move_to([0, 0.55, 0])
        clock.play(Write(caption1), run_time=0.8)
        clock.wait(1.5)
        clock.end_beat(1)

        # ---------- Beat 2: a small example, header and weight column ----------
        clock.play(FadeOut(caption1), run_time=0.4)
        clock.play(
            FadeOut(title),
            exposure_line.animate.move_to([0, 3.10, 0]).scale(30 / 46),
            run_time=0.9,
        )

        col_xs = [-3.60, -1.20, 1.20, 3.60]
        headers = ["asset", "weight", "market", "style"]
        header_row = VGroup(*[mk_text(h, 28, GREY_B).move_to([x, 1.85, 0]) for h, x in zip(headers, col_xs)])
        rule1 = Line([-4.60, 1.50, 0], [4.60, 1.50, 0], color=GREY_B, stroke_width=1.5)

        table_rows = [("A", "0.50", "1.0", "+1.0", 0.95),
                      ("B", "0.30", "1.0", "0.0", 0.15),
                      ("C", "0.20", "1.0", "-0.5", -0.65)]

        asset_col = VGroup(*[mk_text(n, 28, WHITE).move_to([col_xs[0], y, 0]) for n, _, _, _, y in table_rows])
        weight_col = VGroup(*[mk_text(w, 28, YELLOW).move_to([col_xs[1], y, 0]) for _, w, _, _, y in table_rows])
        market_col = VGroup(*[mk_text(m, 28, BLUE).move_to([col_xs[2], y, 0]) for _, _, m, _, y in table_rows])
        style_col = VGroup(*[mk_text(s, 28, BLUE).move_to([col_xs[3], y, 0]) for _, _, _, s, y in table_rows])

        clock.play(Create(rule1), FadeIn(header_row), run_time=0.9)
        clock.play(FadeIn(asset_col), FadeIn(weight_col), run_time=0.9)
        clock.wait(1.0)
        clock.end_beat(2)

        # ---------- Beat 3: market and style columns ----------
        clock.play(FadeIn(market_col), run_time=0.7)
        clock.play(FadeIn(style_col), run_time=0.7)
        clock.play(Indicate(style_col, color=BLUE), run_time=0.6)
        clock.wait(2.5)
        clock.end_beat(3)

        # ---------- Beat 4: the portfolio's own row ----------
        rule2 = Line([-4.60, -1.15, 0], [4.60, -1.15, 0], color=GREY_B, stroke_width=1.5)
        portfolio_label = mk_text("portfolio", 28, WHITE).move_to([col_xs[0], -1.85, 0])
        result_market = mk_text("1.00", 28, BLUE).move_to([col_xs[2], -1.85, 0])
        result_style = mk_text("0.40", 28, BLUE).move_to([col_xs[3], -1.85, 0])

        clock.play(
            Create(rule2), Write(portfolio_label), Write(result_market), Write(result_style),
            run_time=1.2,
        )

        arithmetic_line = MathTex(
            r"0.5\times1.0+0.3\times0.0+0.2\times(-0.5)=0.40", font_size=28, color=GREY_B
        ).move_to([0, -2.85, 0])
        clamp_width(arithmetic_line)
        clock.play(Write(arithmetic_line), run_time=1.2)
        clock.wait(1.5)
        clock.end_beat(4)

        # ---------- Beat 5: factor vol and specific vol ----------
        clock.play(
            FadeOut(VGroup(header_row, rule1, asset_col, weight_col, market_col, style_col,
                            rule2, portfolio_label, result_market, result_style, arithmetic_line)),
            run_time=0.7,
        )

        baseline_y = -2.20
        bar_factor = Rectangle(width=1.10, height=2.03, fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
        bar_factor.move_to([-1.80, baseline_y + 2.03 / 2, 0])
        bar_specific = Rectangle(width=1.10, height=2.23, fill_color=GREY_B, fill_opacity=0.85, stroke_width=0)
        bar_specific.move_to([1.80, baseline_y + 2.23 / 2, 0])

        clock.play(
            LaggedStart(GrowFromEdge(bar_factor, DOWN), GrowFromEdge(bar_specific, DOWN), lag_ratio=0.4),
            run_time=1.5,
        )

        label_factor_val = mk_text("16.2%", 30, BLUE).next_to(bar_factor, UP, buff=0.15)
        label_factor_cap = mk_text("factor", 28, WHITE).move_to([-1.80, -2.60, 0])
        label_specific_val = mk_text("17.8%", 30, GREY_B).next_to(bar_specific, UP, buff=0.15)
        label_specific_cap = mk_text("specific", 28, WHITE).move_to([1.80, -2.60, 0])

        clock.play(
            FadeIn(label_factor_val), FadeIn(label_specific_val),
            FadeIn(label_factor_cap), FadeIn(label_specific_cap),
            run_time=0.8,
        )
        clock.wait(2.0)
        clock.end_beat(5)

        # ---------- Beat 6: add the squares, take the root ----------
        stacked_bottom = Rectangle(width=1.10, height=2.03, fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
        stacked_bottom.move_to([0, baseline_y + 2.03 / 2, 0])
        stacked_top = Rectangle(width=1.10, height=2.23, fill_color=GREY_B, fill_opacity=0.85, stroke_width=0)
        stacked_top.move_to([0, baseline_y + 2.03 + 2.23 / 2, 0])

        clock.play(
            Transform(bar_factor, stacked_bottom),
            Transform(bar_specific, stacked_top),
            FadeOut(label_factor_val), FadeOut(label_specific_val),
            FadeOut(label_factor_cap), FadeOut(label_specific_cap),
            run_time=1.0,
        )

        variances_caption = mk_text("variances add", 26, GREY_B).move_to([2.90, -0.40, 0])
        clock.play(FadeIn(variances_caption), run_time=0.3)

        total_label = mk_text("24.1% per year", 52, WHITE).move_to([0, 2.30, 0])
        clock.play(Write(total_label), run_time=1.0)
        clock.wait(2.3)
        clock.end_beat(6)

        # ---------- Beat 7: split the factor part ----------
        clock.play(FadeOut(bar_specific), FadeOut(variances_caption), run_time=0.5)

        horiz_bar_target = Rectangle(width=8.0, height=0.80, fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
        horiz_bar_target.move_to([0, 0.60, 0])
        clock.play(Transform(bar_factor, horiz_bar_target), run_time=0.8)

        left_part = Rectangle(width=7.82, height=0.80, fill_color=BLUE, fill_opacity=0.70, stroke_width=0)
        left_part.move_to([-4.0 + 7.82 / 2, 0.60, 0])
        right_part = Rectangle(width=0.18, height=0.80, fill_color=TEAL, fill_opacity=0.70, stroke_width=0)
        right_part.move_to([4.0 - 0.18 / 2, 0.60, 0])

        clock.play(ReplacementTransform(bar_factor, VGroup(left_part, right_part)), run_time=1.0)

        market_label = mk_text("97.8% market", 30, WHITE).move_to(left_part.get_center())
        style_leader = Line([4.0 - 0.09, 1.0, 0], [3.90, 1.65, 0], color=TEAL, stroke_width=2)
        style_label = mk_text("style", 26, TEAL).next_to(style_leader, UP, buff=0.05)

        clock.play(FadeIn(market_label), Create(style_leader), FadeIn(style_label), run_time=0.8)
        clock.end_beat(7)

        # ---------- Beat 8: sums exactly ----------
        sums_exactly = mk_text("sums exactly", 32, GREEN).move_to([0, -0.60, 0])
        clock.play(Write(sums_exactly), run_time=0.7)
        no_rule = mk_text("no rule of thumb", 28, GREY_B).move_to([0, -1.35, 0])
        clock.play(Write(no_rule), run_time=0.7)
        clock.wait(2.5)
        clock.end_beat(8)

        # ---------- Beat 9: a fact vs a decision ----------
        clock.play(FadeOut(sums_exactly), FadeOut(no_rule), run_time=0.5)

        fact_value = mk_text("24.1%", 44, GREY_B).move_to([-3.30, -1.90, 0])
        fact_caption = mk_text("a fact", 28, GREY_B).move_to([-3.30, -2.75, 0])
        decision_value = mk_text("97.8% market", 36, GREEN).move_to([3.10, -1.90, 0])
        decision_caption = mk_text("a decision", 28, GREEN).move_to([3.10, -2.75, 0])

        clock.play(
            LaggedStart(
                AnimationGroup(FadeIn(fact_value), FadeIn(fact_caption)),
                AnimationGroup(FadeIn(decision_value), FadeIn(decision_caption)),
                lag_ratio=0.5,
            ),
            run_time=1.2,
        )
        clock.wait(2.0)
        clock.end_beat(9)

        # ---------- Beat 10: stress test setup ----------
        clock.play(
            FadeOut(VGroup(left_part, right_part, market_label, style_leader, style_label,
                            fact_value, fact_caption, decision_value, decision_caption, total_label)),
            run_time=0.8,
        )

        stress_title = mk_text("Stress test", 42, WHITE).move_to([0, 3.10, 0])
        clock.play(ReplacementTransform(exposure_line, stress_title), run_time=1.0)

        arrow_market = Arrow([-2.20, 1.90, 0], [-2.20, 0.40, 0], color=BLUE, stroke_width=6, buff=0)
        label_market_shock = mk_text("market -5%", 30, BLUE).move_to([-2.20, 2.35, 0])
        arrow_style = Arrow([2.20, 1.90, 0], [2.20, 0.40, 0], color=TEAL, stroke_width=6, buff=0)
        label_style_shock = mk_text("style -2%", 30, TEAL).move_to([2.20, 2.35, 0])

        clock.play(
            Create(arrow_market), FadeIn(label_market_shock),
            Create(arrow_style), FadeIn(label_style_shock),
            run_time=1.2,
        )

        stress_arith = MathTex(r"1.00\times(-5)+0.40\times(-2)", font_size=34, color=WHITE)
        stress_arith.move_to([0, -0.55, 0])
        clamp_width(stress_arith)
        clock.play(Write(stress_arith), run_time=1.2)
        clock.end_beat(10)

        # ---------- Beat 11: -5.8%, -$58,000 ----------
        result_pct = mk_text("-5.8%", 56, RED).move_to([0, -0.55, 0])
        clock.play(Transform(stress_arith, result_pct), run_time=1.0)

        dollar_loss = mk_text("-$58,000", 48, RED).move_to([0, -1.80, 0])
        clock.play(Write(dollar_loss), run_time=0.8)
        clock.wait(2.0)
        clock.end_beat(11)

        # ---------- Beat 12: the honest label ----------
        clock.play(
            FadeOut(VGroup(arrow_market, label_market_shock, arrow_style, label_style_shock, stress_arith)),
            dollar_loss.animate.move_to([-3.40, 2.35, 0]).scale(30 / 48),
            run_time=0.8,
        )

        infer_square = Square(side_length=0.60, stroke_color=YELLOW, stroke_width=4,
                               fill_color=YELLOW, fill_opacity=0.30)
        infer_square.move_to([2.00, 0.60, 0])
        clock.play(FadeIn(infer_square), run_time=0.5)

        specific_vol_label = mk_text("specific vol 47%", 28, GREY_B).move_to([2.00, -0.60, 0])
        inferred_label = mk_text("81% inferred", 28, YELLOW).move_to([2.00, -1.25, 0])
        clock.play(Write(specific_vol_label), Write(inferred_label), run_time=1.0)
        clock.wait(2.0)
        clock.end_beat(12)

        # ---------- Beat 13: one warning is left ----------
        leftover = Group(*[m for m in self.mobjects if m is not stress_title])
        clock.play(FadeOut(leftover), run_time=0.8)

        warning_title = mk_text("One warning is left", 42, GOLD).move_to([0, 3.10, 0])
        clock.play(ReplacementTransform(stress_title, warning_title), run_time=1.0)
        clock.wait(1.8)
        clock.end_beat(13)

        # ---------- Beat 14: the risk surface ----------
        def blue_curve_point(t):
            y = 0.40
            y += 0.45 * np.exp(-((t + 4.60) ** 2) / (2 * 0.60 ** 2))
            y -= 0.55 * np.exp(-((t + 2.60) ** 2) / (2 * 0.70 ** 2))
            y -= 0.55 * np.exp(-((t - 3.40) ** 2) / (2 * 0.70 ** 2))
            y -= 2.20 * np.exp(-((t - 1.00) ** 2) / (2 * 0.35 ** 2))
            return np.array([t, y, 0.0])

        risk_curve = ParametricFunction(blue_curve_point, t_range=[-5.40, 5.40], color=BLUE, stroke_width=4)
        estimated_caption = mk_text("estimated risk", 28, BLUE).move_to([-4.10, 1.55, 0])

        clock.play(Create(risk_curve), FadeIn(estimated_caption), run_time=2.0)

        gold_dot = Dot(point=[-4.60, 0.85, 0], radius=0.15, color=GOLD)
        clock.play(FadeIn(gold_dot), run_time=0.5)
        clock.wait(2.0)
        clock.end_beat(14)

        # ---------- Beat 15: the gap ----------
        path_pts = [blue_curve_point(t) for t in np.linspace(-4.60, 1.00, 60)]
        roll_path = VMobject()
        roll_path.set_points_smoothly(path_pts)
        clock.play(MoveAlongPath(gold_dot, roll_path), run_time=2.2, rate_func=smooth)

        def true_curve_point(t):
            y = 0.40
            y += 0.45 * np.exp(-((t + 4.60) ** 2) / (2 * 0.60 ** 2))
            y -= 0.55 * np.exp(-((t + 2.60) ** 2) / (2 * 0.70 ** 2))
            y -= 0.55 * np.exp(-((t - 3.40) ** 2) / (2 * 0.70 ** 2))
            y += 0.50 * np.exp(-((t - 1.00) ** 2) / (2 * 0.35 ** 2))
            return np.array([t, y, 0.0])

        true_curve_solid = ParametricFunction(true_curve_point, t_range=[-5.40, 5.40],
                                               color=WHITE, stroke_width=3)
        true_curve = DashedVMobject(true_curve_solid, num_dashes=45, dashed_ratio=0.6)
        clock.play(FadeIn(true_curve), run_time=1.0)

        gap_arrow = DoubleArrow([1.00, -1.80, 0], [1.00, 0.90, 0], color=RED, stroke_width=4, buff=0)
        gap_label = mk_text("the gap", 28, RED).move_to([2.30, -0.45, 0])
        clock.play(Create(gap_arrow), FadeIn(gap_label), run_time=0.8)
        clock.end_beat(15)

        # ---------- Beat 16: the optimizer hunts your errors ----------
        hunt_text = mk_text("the optimizer hunts your errors", 36, GOLD).move_to([0, 2.35, 0])
        clock.play(Write(hunt_text), run_time=1.2)
        clock.wait(3.0)
        clock.end_beat(16)

        # ---------- Beat 17: the bias statistics ----------
        clock.play(
            FadeOut(VGroup(risk_curve, estimated_caption, gold_dot, true_curve, gap_arrow, gap_label, hunt_text)),
            run_time=0.8,
        )

        bias_baseline = -2.10
        bias_cats = ["min-var", "style", "market", "random", "equal"]
        bias_xs = [-4.20, -2.10, 0.00, 2.10, 4.20]
        bias_vals = [1.36, 1.16, 1.04, 0.93, 0.98]
        bias_colors = [RED, GREY_B, GREY_B, GREY_B, GREY_B]

        target_dashed = DashedLine([-5.60, bias_baseline + 2.00, 0], [5.60, bias_baseline + 2.00, 0],
                                    color=WHITE, stroke_width=2)
        target_label = mk_text("target 1.0", 22, WHITE).move_to([5.55, bias_baseline + 2.20, 0])
        clock.play(Create(target_dashed), FadeIn(target_label), run_time=0.8)

        bias_bars = VGroup()
        bias_val_labels = VGroup()
        bias_cat_labels = VGroup()
        for x, v, c, cat in zip(bias_xs, bias_vals, bias_colors, bias_cats):
            h = v * 2.0
            bar = Rectangle(width=0.85, height=h, fill_color=c, fill_opacity=0.85, stroke_width=0)
            bar.move_to([x, bias_baseline + h / 2, 0])
            bias_bars.add(bar)
            bias_val_labels.add(mk_text(f"{v:.2f}", 22, c).next_to(bar, UP, buff=0.28))
            bias_cat_labels.add(mk_text(cat, 24, WHITE).move_to([x, bias_baseline - 0.35, 0]))

        clock.play(
            GrowFromEdge(bias_bars[0], DOWN), FadeIn(bias_val_labels[0]), FadeIn(bias_cat_labels[0]),
            run_time=1.0,
        )
        clock.wait(0.5)
        clock.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bias_bars[1:]], lag_ratio=0.2),
            FadeIn(VGroup(*bias_val_labels[1:])), FadeIn(VGroup(*bias_cat_labels[1:])),
            run_time=1.5,
        )
        clock.play(Indicate(bias_bars[0], color=RED), run_time=0.8)
        clock.wait(3.5)
        clock.end_beat(17)

        # ---------- Beat 18: the famous cure ----------
        new_vals = [0.98, 0.92, 0.97, 0.75, 0.77]
        new_colors = [GREEN, GREY_B, GREY_B, RED, RED]

        transforms = []
        for i, (x, v, c) in enumerate(zip(bias_xs, new_vals, new_colors)):
            h = v * 2.0
            new_bar = Rectangle(width=0.85, height=h, fill_color=c, fill_opacity=0.85, stroke_width=0)
            new_bar.move_to([x, bias_baseline + h / 2, 0])
            transforms.append(Transform(bias_bars[i], new_bar))
            new_val_lbl = mk_text(f"{v:.2f}", 22, c).next_to(new_bar, UP, buff=0.28)
            transforms.append(Transform(bias_val_labels[i], new_val_lbl))

        cure_title = mk_text("the famous cure", 36, GOLD).move_to([0, 3.10, 0])
        clock.play(*transforms, ReplacementTransform(warning_title, cure_title), run_time=2.0)
        clock.wait(2.5)
        clock.end_beat(18)

        # ---------- Beat 19: shipped off by default ----------
        clock.play(Indicate(bias_bars[3], color=RED), Indicate(bias_bars[4], color=RED), run_time=0.8)
        shipped_text = mk_text("shipped off by default", 32, RED).move_to([0, 2.35, 0])
        clock.play(Write(shipped_text), run_time=1.0)
        clock.wait(3.0)
        clock.end_beat(19)

        # ---------- Beat 20: the bias belongs to the choosing ----------
        clock.play(
            FadeOut(VGroup(bias_bars, bias_val_labels, bias_cat_labels, target_dashed, target_label,
                            shipped_text)),
            run_time=0.8,
        )

        belongs_line1 = mk_text("the bias belongs to the choosing", 40, GOLD).move_to([0, 0.55, 0])
        clock.play(Write(belongs_line1), run_time=1.2)
        belongs_line2 = mk_text("not to the matrix", 40, WHITE).move_to([0, -0.40, 0])
        clock.play(Write(belongs_line2), run_time=1.0)
        clock.wait(2.5)
        clock.end_beat(20)

        # ---------- Beat 21: from the matrix to the report ----------
        clock.play(FadeOut(belongs_line1), FadeOut(belongs_line2), run_time=0.6)

        f_square = Square(side_length=1.5, fill_color=BLUE, fill_opacity=0.60, stroke_color=BLUE, stroke_width=3)
        f_square.move_to([-3.20, 0.30, 0])
        f_label = mk_text("F", 40, WHITE).move_to(f_square.get_center())
        f_badge = VGroup(f_square, f_label)
        clock.play(FadeIn(f_badge), run_time=0.6)

        doc_rect = Rectangle(width=2.0, height=2.6, stroke_color=GREEN, stroke_width=3,
                              fill_color=GREEN, fill_opacity=0.08).move_to([3.20, 0.30, 0])
        doc_lines = VGroup(*[
            Line([3.20 - 0.7, 1.0 - i * 0.35, 0], [3.20 + 0.7, 1.0 - i * 0.35, 0], color=GREY_B, stroke_width=1.5)
            for i in range(4)
        ])
        doc_label = mk_text("the report", 30, GREEN).move_to([3.20, -1.40, 0])
        doc_group = VGroup(doc_rect, doc_lines, doc_label)
        clock.play(FadeIn(doc_group), run_time=0.6)

        correction_dot = Dot(point=f_square.get_center(), radius=0.08, color=TEAL)
        correction_label = mk_text("correction", 22, TEAL).next_to(correction_dot, UP, buff=0.1)
        correction_group = VGroup(correction_dot, correction_label)
        arc_path = ArcBetweenPoints(f_square.get_center(), doc_rect.get_center(), angle=-PI / 3)

        clock.play(FadeIn(correction_group), run_time=0.3)
        clock.play(MoveAlongPath(correction_group, arc_path), run_time=1.0)
        clock.wait(0.5)
        clock.end_beat(21)

        # ---------- Beat 22: the question ----------
        clock.play(FadeOut(VGroup(f_badge, doc_group, correction_group)), run_time=0.8)

        question1 = mk_text("Did you choose these weights,", 40, WHITE).move_to([0, 0.75, 0])
        clock.play(Write(question1), run_time=1.4)
        clock.wait(0.4)
        question2 = mk_text("or did a machine choose them by looking at me?", 40, GOLD).move_to([0, -0.20, 0])
        clock.play(Write(question2), run_time=1.4)
        clock.wait(3.0)
        clock.end_beat(22)

        # ---------- Beat 23: graded every week ----------
        clock.play(FadeOut(question1), FadeOut(question2), run_time=0.8)

        know_title = mk_text("How you know any of this", 40, WHITE).move_to([0, 3.10, 0])
        clock.play(ReplacementTransform(cure_title, know_title), run_time=1.0)

        icon_xs = [-5.10, -3.40, -1.70, 0.00, 1.70, 3.40, 5.10]
        icons = VGroup()
        for i, x in enumerate(icon_xs):
            color = GOLD if i == len(icon_xs) - 1 else BLUE
            icons.add(build_mini_icon([x, 1.30], color))

        clock.play(LaggedStart(*[FadeIn(icon) for icon in icons], lag_ratio=0.15), run_time=1.5)

        graded_caption = mk_text("graded every week, out of sample", 30, WHITE).move_to([0, 0.20, 0])
        clock.play(Write(graded_caption), run_time=1.0)

        break_label = mk_text("built to break it", 22, GOLD).move_to([4.90, 0.85, 0])
        clock.play(FadeIn(break_label), run_time=0.5)
        clock.end_beat(23)

        # ---------- Beat 24: 0.988 overall, 0.99 optimized ----------
        clock.play(FadeOut(graded_caption), run_time=0.5)

        number_line = Line([-4.60, -1.40, 0], [4.60, -1.40, 0], color=GREY_B, stroke_width=3)
        ticks = VGroup(
            mk_text("0.90", 26, GREY_B).next_to([-4.60, -1.40, 0], DOWN, buff=0.25),
            mk_text("1.00", 26, GREY_B).next_to([0.00, -1.40, 0], DOWN, buff=0.25),
            mk_text("1.10", 26, GREY_B).next_to([4.60, -1.40, 0], DOWN, buff=0.25),
        )
        clock.play(Create(number_line), FadeIn(ticks), run_time=0.8)

        target_marker = DashedLine([0.00, -1.90, 0], [0.00, -0.90, 0], color=WHITE, stroke_width=2)
        target_marker_label = mk_text("target", 24, WHITE).move_to([0.00, -0.55, 0])
        clock.play(Create(target_marker), FadeIn(target_marker_label), run_time=0.6)

        overall_dot = Dot(point=[-0.55, -1.40, 0], radius=0.12, color=GREEN)
        overall_label = mk_text("0.988 overall", 26, GREEN).move_to([-1.20, -2.30, 0])
        optimized_dot = Dot(point=[-0.46, -1.40, 0], radius=0.12, color=GOLD)
        optimized_label = mk_text("0.99 optimized", 26, GOLD).move_to([1.50, -2.30, 0])

        clock.play(
            LaggedStart(
                AnimationGroup(FadeIn(overall_dot), FadeIn(overall_label)),
                AnimationGroup(FadeIn(optimized_dot), FadeIn(optimized_label)),
                lag_ratio=0.5,
            ),
            run_time=1.5,
        )
        clock.wait(2.5)
        clock.end_beat(24)

        # ---------- Beat 25: the closing card ----------
        clock.play(
            FadeOut(VGroup(icons, break_label, number_line, ticks, target_marker, target_marker_label,
                            overall_dot, overall_label, optimized_dot, optimized_label, know_title)),
            run_time=0.8,
        )

        final_grid = build_grid().scale(0.55).move_to([-4.10, 0.30, 0])
        clock.play(FadeIn(final_grid), run_time=0.8)

        summary_items = [
            ("24.1% per year", WHITE, 1.65),
            ("97.8% market", BLUE, 0.70),
            ("-$58,000 stressed", RED, -0.25),
            ("81% inferred", YELLOW, -1.20),
        ]
        summary_group = VGroup()
        for text, color, y in summary_items:
            dot = Dot(point=[-1.75, y, 0], radius=0.07, color=color)
            label = mk_text(text, 30, color).next_to(dot, RIGHT, buff=0.25)
            summary_group.add(dot, label)

        clock.play(LaggedStart(*[FadeIn(m) for m in summary_group], lag_ratio=0.15), run_time=2.0)

        closing_line = mk_text("and one honest question about who chose the weights", 30, GOLD)
        closing_line.move_to([0, -2.75, 0])
        clock.play(Write(closing_line), run_time=1.2)
        clock.wait(3.0)
        clock.end_beat(25)
