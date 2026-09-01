import numpy as np
from manim import *
from teachme_manim import BeatClock

TEAL = "#5CD0B3"
BLUE = "#58C4DD"
GREY_B = "#CCCCCC"
RED = "#FC6255"
GREEN = "#83C167"
GOLD = "#F0AC5F"
YELLOW = "#F4D345"

BEATS = [6.8, 7.05, 8.05, 6.95, 8.1, 7.45, 5.98, 8.53, 8.73, 6.15, 6.68, 6.05, 6.4,
         5.8, 5.03, 13.38, 7.88, 7.08, 10.18, 7.68, 7.25, 6.4, 10.4, 4.3, 8.4, 7.1, 5.15]

# Card navigation geometry: each defect card lives at a fixed HOME slot when
# dimmed, or at ACTIVE (bright, larger) when it is the section in focus.
# This keeps parked cards away from the top-of-frame caption band and
# guarantees the active card never blocks a beat's headline caption.
HOME1 = np.array([-3.85, 0.60, 0])
HOME2 = np.array([0.00, 0.60, 0])
HOME3 = np.array([3.85, 0.60, 0])
ACTIVE = np.array([0.00, 2.20, 0])
BADGE3 = np.array([-5.40, 3.30, 0])


class TeachScene(Scene):
    def construct(self):
        self.camera.background_color = "#0e1015"
        np.random.seed(3)
        clock = BeatClock(self, BEATS)

        def make_card(label, center):
            rect = RoundedRectangle(
                corner_radius=0.15, width=3.5, height=1.4,
                stroke_color=TEAL, stroke_width=3,
                fill_color=TEAL, fill_opacity=0.08,
            ).move_to(center)
            text = Text(label, font_size=28, color=WHITE).move_to(center)
            return VGroup(rect, text)

        # ---------- Beat 1 (index 0): title, three defect cards ----------
        title = Text("Three measured defects", font_size=42, color=WHITE).move_to([0, 3.10, 0])
        clock.play(Write(title), run_time=1.2)

        card1 = make_card("autocorrelation", HOME1)
        card2 = make_card("regime shift", HOME2)
        card3 = make_card("noisy directions", HOME3)
        cards = VGroup(card1, card2, card3)

        clock.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.3), run_time=1.5)
        clock.wait(2.5)
        clock.end_beat(0)

        # ---------- Beat 2 (index 1): the annualizing rule, 252 dots ----------
        title_small = Text("Three measured defects", font_size=30, color=WHITE).move_to([0, 3.30, 0])
        clock.play(
            Transform(title, title_small),
            card2.animate.set_opacity(0.20).scale(0.6),
            card3.animate.set_opacity(0.20).scale(0.6),
            card1.animate.move_to(ACTIVE).scale(0.9),
            run_time=1.0,
        )

        scaling_rule = Text("annual variance equals daily variance times 252", font_size=44, color=WHITE)
        scaling_rule.move_to([0, 0.90, 0])
        clock.play(Write(scaling_rule), run_time=1.2)
        clock.wait(0.5)

        rows, cols, spacing = 7, 36, 0.13
        cx, cy = 0.0, -1.30
        dot_pts = [
            [cx + (c - (cols - 1) / 2) * spacing, cy + (r - (rows - 1) / 2) * spacing, 0]
            for r in range(rows) for c in range(cols)
        ]
        dots = VGroup(*[Dot(point=p, radius=0.03, color=GREY_B) for p in dot_pts])
        clock.play(FadeIn(dots, lag_ratio=0.008), run_time=1.5)
        clock.wait(1.0)
        clock.end_beat(1)

        # ---------- Beat 3 (index 2): independence assumption, five same-way days ----------
        assume_text = Text("assumes every day is independent", font_size=32, color=WHITE).move_to([0, -2.75, 0])
        clock.play(Write(assume_text), run_time=0.8)
        clock.play(FadeOut(dots), FadeOut(scaling_rule), run_time=0.6)

        direction = np.array([1.0, 0.6, 0])
        direction = direction / np.linalg.norm(direction) * 0.9
        arrow_start = np.array([-3.20, -1.40, 0])
        step_vec = np.array([1.40, 0.55, 0])
        arrows = VGroup(*[
            Arrow(arrow_start + step_vec * i, arrow_start + step_vec * i + direction,
                  color=BLUE, stroke_width=5, buff=0)
            for i in range(5)
        ])
        clock.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3), run_time=1.5)
        clock.wait(1.5)

        same_dir_text = Text("five days, same direction", font_size=32, color=RED).move_to([0, -2.75, 0])
        clock.play(ReplacementTransform(assume_text, same_dir_text), run_time=0.8)
        clock.end_beat(2)

        # ---------- Beat 4 (index 3): momentum, forecast vs realized ----------
        clock.play(FadeOut(arrows), FadeOut(same_dir_text), run_time=0.6)

        baseline_y = -1.90
        left_bar = Rectangle(width=0.90, height=2.00, fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
        left_bar.move_to([-1.10, baseline_y + 1.00, 0])
        right_bar = Rectangle(width=0.90, height=2.80, fill_color=RED, fill_opacity=0.85, stroke_width=0)
        right_bar.move_to([1.10, baseline_y + 1.40, 0])
        left_label = Text("forecast 1.0", font_size=28, color=WHITE).move_to([-1.10, -2.30, 0])
        right_label = Text("realized 1.40", font_size=28, color=WHITE).move_to([1.10, -2.30, 0])

        clock.play(
            GrowFromEdge(left_bar, DOWN), GrowFromEdge(right_bar, DOWN),
            FadeIn(left_label), FadeIn(right_label),
            run_time=1.2,
        )
        momentum_label = Text("momentum factor", font_size=32, color=WHITE).move_to([0, 1.55, 0])
        clock.play(Write(momentum_label), run_time=0.8)
        clock.wait(2.0)
        clock.end_beat(3)

        # ---------- Beat 5 (index 4): five declining lag weights ----------
        clock.play(FadeOut(VGroup(left_bar, right_bar, left_label, right_label, momentum_label)), run_time=0.7)

        heights5 = [1.40, 1.12, 0.84, 0.56, 0.28]
        xs5 = [-1.70, -0.85, 0.0, 0.85, 1.70]
        base5 = -1.20
        weight_bars = VGroup()
        weight_labels = VGroup()
        for i, (x, h) in enumerate(zip(xs5, heights5)):
            bar = Rectangle(width=0.60, height=h, fill_color=TEAL, fill_opacity=0.65, stroke_width=0)
            bar.move_to([x, base5 + h / 2, 0])
            weight_bars.add(bar)
            weight_labels.add(Text(f"lag {i + 1}", font_size=22, color=GREY_B).move_to([x, base5 - 0.25, 0]))

        clock.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in weight_bars], lag_ratio=0.2),
            FadeIn(weight_labels),
            run_time=1.5,
        )
        add_back_text = Text("add back 5 lags", font_size=34, color=TEAL).move_to([0, 1.20, 0])
        clock.play(Write(add_back_text), run_time=0.8)
        clipped_text = Text("clipped to [0.5, 2]", font_size=30, color=GREY_B).move_to([0, -2.40, 0])
        clock.play(Write(clipped_text), run_time=0.8)
        clock.wait(2.0)
        clock.end_beat(4)

        # ---------- Beat 6 (index 5): F = V C V, variances only ----------
        clock.play(FadeOut(VGroup(weight_bars, weight_labels, add_back_text, clipped_text)), run_time=0.7)

        sq_v1 = Square(side_length=1.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.20)
        sq_v1.move_to([-2.60, 0.20, 0])
        sq_c = Square(side_length=1.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.20)
        sq_c.move_to([0.0, 0.20, 0])
        sq_v2 = Square(side_length=1.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.20)
        sq_v2.move_to([2.60, 0.20, 0])
        lbl_v1 = Text("V", font_size=34, color=WHITE).move_to(sq_v1.get_center())
        lbl_c = Text("C", font_size=34, color=WHITE).move_to(sq_c.get_center())
        lbl_v2 = Text("V", font_size=34, color=WHITE).move_to(sq_v2.get_center())
        dot_ab = Dot(point=[-1.30, 0.20, 0], radius=0.05, color=WHITE)
        dot_bc = Dot(point=[1.30, 0.20, 0], radius=0.05, color=WHITE)
        squares_group = VGroup(sq_v1, lbl_v1, sq_c, lbl_c, sq_v2, lbl_v2, dot_ab, dot_bc)

        clock.play(FadeIn(squares_group), run_time=1.2)
        clock.play(
            sq_v1.animate.set_fill(TEAL, opacity=0.45).set_stroke(TEAL),
            sq_v2.animate.set_fill(TEAL, opacity=0.45).set_stroke(TEAL),
            run_time=0.8,
        )
        variances_text = Text("variances only", font_size=32, color=TEAL).move_to([0, -1.60, 0])
        clock.play(Write(variances_text), run_time=0.8)
        untouched_text = Text("correlations untouched", font_size=32, color=GREY_B).move_to([0, -2.35, 0])
        clock.play(Write(untouched_text), run_time=0.8)
        clock.wait(2.0)
        clock.end_beat(5)

        # ---------- Beat 7 (index 6): cards pivot to defect 2 ----------
        clock.play(FadeOut(VGroup(squares_group, variances_text, untouched_text)), run_time=0.7)
        clock.play(
            card1.animate.move_to(HOME1).scale(0.6 / 0.9).set_opacity(0.20),
            card2.animate.move_to(ACTIVE).scale(1.0 / 0.6).set_opacity(1.0),
            run_time=1.5,
        )
        clock.play(card2[0].animate.set_stroke(width=5).set_fill(opacity=0.20), run_time=0.3)
        clock.wait(2.0)
        clock.end_beat(6)

        # ---------- Beat 8 (index 7): the volatility lag chart ----------
        clock.play(FadeOut(title), run_time=0.4)
        axes_vol = Axes(
            x_range=[0, 200, 50], y_range=[0, 3, 1], x_length=9.4, y_length=3.4,
            axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2},
        ).move_to([0.30, -0.70, 0])
        x_axis_label = Text("trading days", font_size=26, color=GREY_B).move_to([3.60, -2.75, 0])
        y_axis_label = Text("volatility", font_size=26, color=GREY_B).rotate(90 * DEGREES).move_to([-4.70, -0.70, 0])

        step_pts = [axes_vol.c2p(0, 1.0), axes_vol.c2p(60, 1.0), axes_vol.c2p(60, 2.2), axes_vol.c2p(200, 2.2)]
        step_curve = VMobject(stroke_color=WHITE, stroke_width=4)
        step_curve.set_points_as_corners(step_pts)

        halflife = 28
        ewma_xs = np.linspace(60, 200, 80)
        ewma_ys = 2.2 - 1.2 * np.power(2.0, -(ewma_xs - 60) / halflife)
        ewma_pts = [axes_vol.c2p(0, 1.0), axes_vol.c2p(60, 1.0)] + \
                   [axes_vol.c2p(x, y) for x, y in zip(ewma_xs, ewma_ys)]
        ewma_curve = VMobject(stroke_color=TEAL, stroke_width=4)
        ewma_curve.set_points_smoothly(ewma_pts)

        clock.play(Create(axes_vol), FadeIn(x_axis_label), FadeIn(y_axis_label), run_time=1.2)
        clock.play(Create(step_curve), run_time=1.2)
        clock.play(Create(ewma_curve), run_time=1.8)

        shade_xs = np.linspace(60, 144, 40)
        upper_pts = [axes_vol.c2p(x, 2.2) for x in shade_xs]
        lower_pts = [axes_vol.c2p(x, 2.2 - 1.2 * np.power(2.0, -(x - 60) / halflife)) for x in shade_xs]
        region = Polygon(*(upper_pts + lower_pts[::-1]), fill_color=RED, fill_opacity=0.22, stroke_width=0)
        clock.play(FadeIn(region), run_time=0.8)

        lag_behind_text = Text("84 days behind", font_size=30, color=RED).move_to([-0.60, -0.30, 0])
        clock.play(Write(lag_behind_text), run_time=0.8)
        clock.wait(2.0)
        clock.end_beat(7)

        # ---------- Beat 9 (index 8): forty factors, today ----------
        clock.play(
            FadeOut(VGroup(axes_vol, x_axis_label, y_axis_label, step_curve, ewma_curve, region, lag_behind_text)),
            run_time=0.8,
        )
        clock.wait(0.5)

        header_text = Text("today, all 40 factors at once", font_size=34, color=WHITE).move_to([0, 3.25, 0])
        clock.play(Write(header_text), run_time=0.8)

        n_factors = 40
        forecast_vol = np.random.uniform(0.6, 0.8, n_factors)
        today_returns = np.random.uniform(-1.2, 1.4, n_factors)
        bar_xs = [(i - (n_factors - 1) / 2) * 0.28 for i in range(n_factors)]

        return_bars = VGroup()
        for x, h in zip(bar_xs, today_returns):
            bar = Rectangle(width=0.16, height=abs(h), fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
            bar.move_to([x, h / 2, 0])
            return_bars.add(bar)
        forecast_boxes = VGroup()
        for x, fv in zip(bar_xs, forecast_vol):
            box = Rectangle(width=0.22, height=fv, stroke_color=GREY_B, stroke_width=2.5, fill_opacity=0)
            box.move_to([x, 0, 0])
            forecast_boxes.add(box)
        forecast_boxes.set_z_index(0)
        return_bars.set_z_index(1)

        clock.play(FadeIn(forecast_boxes), run_time=0.8)
        clock.play(
            LaggedStart(*[GrowFromEdge(b, DOWN if h >= 0 else UP) for b, h in zip(return_bars, today_returns)],
                        lag_ratio=0.02),
            run_time=1.5,
        )
        clock.wait(1.5)
        clock.end_beat(8)

        # ---------- Beat 10 (index 9): divide by forecast, collapse to one number ----------
        ratios = today_returns / forecast_vol
        ratio_targets = []
        for x, r in zip(bar_xs, ratios):
            t = Rectangle(width=0.16, height=abs(r), fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
            t.move_to([x, r / 2, 0])
            ratio_targets.append(t)
        dashed_ref = DashedLine([-5.46, 1.0, 0], [5.46, 1.0, 0], color=WHITE, stroke_width=3)

        clock.play(
            ReplacementTransform(forecast_boxes, dashed_ref),
            *[Transform(b, t) for b, t in zip(return_bars, ratio_targets)],
            run_time=2.0,
        )

        collapsed_bar = Rectangle(width=4.4, height=1.8, fill_color=TEAL, fill_opacity=0.65,
                                   stroke_color=TEAL, stroke_width=3).move_to([0, -1.20, 0])
        collapsed_label = Text("mean of squared ratios", font_size=30, color=TEAL).move_to([0, -2.55, 0])
        clock.play(ReplacementTransform(VGroup(return_bars, dashed_ref), collapsed_bar), run_time=1.2)
        clock.play(Write(collapsed_label), run_time=0.6)
        clock.end_beat(9)

        # ---------- Beat 11 (index 10): sit with the question ----------
        question_text = Text("how large were the moves against the forecast?", font_size=32, color=WHITE)
        question_text.move_to([0, 3.25, 0])
        clock.play(ReplacementTransform(header_text, question_text), run_time=1.2)
        clock.wait(3.5)
        clock.end_beat(10)

        # ---------- Beat 12 (index 11): the gauge answers 1.8 ----------
        gauge_center = np.array([0, -0.60, 0])
        gauge_radius = 1.6
        gauge_arc = Arc(radius=gauge_radius, start_angle=PI, angle=-PI, arc_center=gauge_center,
                         stroke_color=GREY_B, stroke_width=4)
        tick_05 = Text("0.5", font_size=24, color=GREY_B).move_to(gauge_center + [-gauge_radius - 0.35, 0, 0])
        tick_10 = Text("1.0", font_size=24, color=GREY_B).move_to(gauge_center + [0, gauge_radius + 0.28, 0])
        tick_20 = Text("2.0", font_size=24, color=GREY_B).move_to(gauge_center + [gauge_radius + 0.35, 0, 0])
        tick_labels = VGroup(tick_05, tick_10, tick_20)

        def gauge_point(value):
            if value <= 1.0:
                angle = PI - (value - 0.5) / 0.5 * (PI / 2)
            else:
                angle = PI / 2 - (value - 1.0) / 1.0 * (PI / 2)
            return gauge_center + gauge_radius * np.array([np.cos(angle), np.sin(angle), 0])

        needle = Line(gauge_center, gauge_point(1.0), color=TEAL, stroke_width=6)
        clock.play(Create(gauge_arc), FadeIn(tick_labels), run_time=1.0)
        clock.play(Create(needle), run_time=0.6)

        needle_target = Line(gauge_center, gauge_point(1.8), color=TEAL, stroke_width=6)
        gauge_value_label = Text("1.8", font_size=44, color=TEAL).move_to([0, -0.05, 0])
        clock.play(Transform(needle, needle_target), run_time=1.5)
        clock.play(Write(gauge_value_label), run_time=0.6)
        clock.wait(2.0)
        clock.end_beat(11)

        gauge_group = VGroup(gauge_arc, tick_labels, needle, gauge_value_label)

        # ---------- Beat 13 (index 12): raise the forecast today, not in 84 days ----------
        clock.play(
            FadeOut(VGroup(collapsed_bar, collapsed_label, question_text)),
            gauge_group.animate.move_to([-4.10, 1.30, 0]).scale(0.55),
            run_time=1.0,
        )
        VGroup(axes_vol, x_axis_label, y_axis_label, step_curve, ewma_curve, region).shift([0.6, 0, 0])
        clock.play(
            FadeIn(axes_vol), FadeIn(x_axis_label), FadeIn(y_axis_label),
            FadeIn(step_curve), FadeIn(ewma_curve), FadeIn(region),
            run_time=0.8,
        )

        fast_xs = np.linspace(60, 200, 80)
        fast_ys = np.minimum(2.2, 1.0 + 1.2 * (fast_xs - 60) / 6.0)
        fast_pts = [axes_vol.c2p(0, 1.0), axes_vol.c2p(60, 1.0)] + \
                   [axes_vol.c2p(x, y) for x, y in zip(fast_xs, fast_ys)]
        ewma_fast = VMobject(stroke_color=TEAL, stroke_width=4)
        ewma_fast.set_points_smoothly(fast_pts)

        clock.play(Transform(ewma_curve, ewma_fast), region.animate.set_opacity(0.0), run_time=1.5)
        raise_text = Text("raise every volatility today", font_size=32, color=GREEN).move_to([1.90, 2.55, 0])
        clock.play(Write(raise_text), run_time=0.8)
        clock.wait(2.0)
        clock.end_beat(12)

        # ---------- Beat 14 (index 13): time axis vs cross-section ----------
        clock.play(
            FadeOut(VGroup(axes_vol, x_axis_label, y_axis_label, step_curve, ewma_curve, region, raise_text)),
            run_time=0.7,
        )
        time_arrow = Arrow([-4.60, -1.60, 0], [4.60, -1.60, 0], color=GREY_B, stroke_width=4, buff=0)
        time_label = Text("time axis", font_size=28, color=GREY_B).move_to([0, -2.15, 0])
        clock.play(Create(time_arrow), FadeIn(time_label), run_time=0.8)

        # Stop short of the active card's home band (bottom edge near y=1.50)
        # so the arrow tip never runs into the "regime shift" card above it.
        cross_arrow = Arrow([0, -1.10, 0], [0, 1.40, 0], color=TEAL, stroke_width=5, buff=0)
        cross_label = Text("cross-section", font_size=30, color=TEAL).move_to([1.90, 1.60, 0])
        clock.play(Create(cross_arrow), FadeIn(cross_label), run_time=0.8)
        clock.wait(2.5)
        clock.end_beat(13)

        # ---------- Beat 15 (index 14): forty measurements of one regime ----------
        n_dots = 40
        dot_ys = np.linspace(-1.00, 1.30, n_dots)
        cross_dots = VGroup(*[Dot(point=[0, y, 0], radius=0.05, color=TEAL) for y in dot_ys])
        clock.play(FadeIn(cross_dots, lag_ratio=0.03), run_time=1.5)
        measure_text = Text("40 measurements, one regime", font_size=34, color=TEAL).move_to([0, 3.25, 0])
        clock.play(Write(measure_text), run_time=1.0)
        clock.wait(2.5)
        clock.end_beat(14)

        # ---------- Beat 16 (index 15): Barra's published calibration ----------
        clock.play(
            FadeOut(VGroup(time_arrow, time_label, cross_arrow, cross_label, cross_dots, measure_text,
                           gauge_group)),
            run_time=0.8,
        )

        axes_bias = Axes(
            x_range=[0, 4, 1], y_range=[0.5, 1.5, 0.25], x_length=9.0, y_length=3.0,
            axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2},
        ).move_to([0.40, -0.40, 0])
        year_labels = VGroup(*[
            Text(yr, font_size=24, color=GREY_B).next_to(axes_bias.c2p(i, 0.5), DOWN, buff=0.2)
            for i, yr in enumerate(["2007", "2008", "2009", "2010"])
        ])
        y_axis_label_bias = Text("bias statistic", font_size=26, color=GREY_B).rotate(90 * DEGREES)
        y_axis_label_bias.move_to([-4.60, -0.40, 0])

        clock.play(Create(axes_bias), FadeIn(year_labels), FadeIn(y_axis_label_bias), run_time=1.2)
        clock.wait(1.0)

        target_line = DashedLine(axes_bias.c2p(0, 1.0), axes_bias.c2p(4, 1.0), color=WHITE, stroke_width=2)
        target_label = Text("target 1.0", font_size=24, color=WHITE).next_to(axes_bias.c2p(4, 1.0), RIGHT, buff=0.35)
        clock.play(Create(target_line), FadeIn(target_label), run_time=0.8)
        clock.wait(0.5)

        unadj_xs = np.linspace(0, 4, 60)
        unadj_ys = np.where(
            unadj_xs < 1.3, 1.0 + 0.30 * (unadj_xs / 1.3),
            np.where(unadj_xs < 2.2, 1.30 - 0.60 * ((unadj_xs - 1.3) / 0.9),
                     0.70 + 0.30 * ((unadj_xs - 2.2) / 1.8)),
        )
        unadj_line = VMobject(stroke_color=RED, stroke_width=5)
        unadj_line.set_points_smoothly([axes_bias.c2p(x, y) for x, y in zip(unadj_xs, unadj_ys)])
        unadj_label = Text("no adjustment", font_size=26, color=RED).move_to([-2.60, 1.90, 0])
        clock.play(Create(unadj_line), FadeIn(unadj_label), run_time=1.8)
        clock.wait(1.5)

        adj_xs = np.linspace(0, 4, 60)
        adj_ys = 1.0 + 0.03 * np.sin(3 * adj_xs)
        adj_line = VMobject(stroke_color=GREEN, stroke_width=5)
        adj_line.set_points_smoothly([axes_bias.c2p(x, y) for x, y in zip(adj_xs, adj_ys)])
        # Placed below the year labels, clear of both curves and the x-axis row.
        adj_label = Text("with the regime adjustment", font_size=26, color=GREEN).move_to([2.40, -2.70, 0])
        clock.play(Create(adj_line), FadeIn(adj_label), run_time=1.8)
        clock.wait(2.9)
        clock.end_beat(15)

        # ---------- Beat 17 (index 16): cards pivot to defect 3 ----------
        clock.play(
            FadeOut(VGroup(axes_bias, year_labels, y_axis_label_bias, target_line, target_label,
                           unadj_line, unadj_label, adj_line, adj_label)),
            run_time=0.8,
        )
        clock.play(
            card2.animate.move_to(HOME2).scale(0.6).set_opacity(0.20),
            card2[0].animate.set_stroke(width=3),
            card3.animate.move_to(ACTIVE).scale(1.0 / 0.6).set_opacity(1.0),
            run_time=1.2,
        )
        clock.play(card3[0].animate.set_stroke(width=5).set_fill(opacity=0.20), run_time=0.3)

        n_eig = 40
        eig_xs = [(i - (n_eig - 1) / 2) * 0.26 for i in range(n_eig)]
        k_decay = np.log(26.0) / 39.0
        eig_heights = 2.60 * np.exp(-k_decay * np.arange(n_eig))
        eig_bars = VGroup()
        for i, (x, h) in enumerate(zip(eig_xs, eig_heights)):
            color = BLUE if i < 5 else GREY_B
            opacity = 0.75 if i < 5 else 0.40
            bar = Rectangle(width=0.14, height=h, fill_color=color, fill_opacity=opacity, stroke_width=0)
            bar.move_to([x, -1.90 + h / 2, 0])
            eig_bars.add(bar)
        clock.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in eig_bars], lag_ratio=0.03), run_time=1.5)

        noise_brace = Brace(VGroup(*eig_bars[30:40]), direction=DOWN, color=RED)
        noise_label = Text("almost pure noise", font_size=28, color=RED).move_to([3.60, -2.60, 0])
        clock.play(Create(noise_brace), Write(noise_label), run_time=0.8)
        clock.end_beat(16)

        # ---------- Beat 18 (index 17): the 80/20 blend ----------
        clock.play(eig_bars[5:40].animate.set_fill(RED, opacity=0.35), run_time=0.6)

        blend_left = Rectangle(width=6.4, height=0.60, fill_color=BLUE, fill_opacity=0.60, stroke_width=0)
        blend_left.move_to([-0.8, 0.85, 0])
        blend_left_label = Text("80% sample", font_size=26, color=WHITE).move_to([-0.8, 0.85, 0])
        blend_right = Rectangle(width=1.6, height=0.60, fill_color=TEAL, fill_opacity=0.60, stroke_width=0)
        blend_right.move_to([3.2, 0.85, 0])
        blend_right_label = Text("20% rank 5", font_size=24, color=WHITE).move_to([3.2, 0.85, 0])
        blend_bar = VGroup(blend_left, blend_left_label, blend_right, blend_right_label)

        clock.play(
            GrowFromEdge(blend_left, RIGHT), GrowFromEdge(blend_right, LEFT),
            FadeIn(blend_left_label), FadeIn(blend_right_label),
            run_time=1.2,
        )
        clock.wait(2.0)
        clock.end_beat(17)

        # ---------- Beat 19 (index 18): the honest score, weekly ----------
        # card3 stays on screen as a small bright badge in the far corner,
        # instead of fading out, so "noisy directions" remains the visible
        # section header while the blend bar takes the top of the frame.
        clock.play(
            FadeOut(VGroup(eig_bars, noise_brace, noise_label)),
            card3.animate.move_to(BADGE3).scale(0.35),
            blend_bar.animate.move_to([0, 2.35, 0]).scale(0.8),
            run_time=0.7,
        )
        clock.wait(1.0)

        row1_label = Text("weekly, no blend", font_size=28, color=WHITE).move_to([-4.20, 0.45, 0])
        row1_value = Text("1.36", font_size=40, color=RED).move_to([2.60, 0.45, 0])
        row2_label = Text("weekly, with blend", font_size=28, color=WHITE).move_to([-4.20, -0.60, 0])
        row2_value = Text("1.29", font_size=40, color=RED).move_to([2.60, -0.60, 0])
        clock.play(
            LaggedStart(
                AnimationGroup(FadeIn(row1_label), FadeIn(row1_value)),
                AnimationGroup(FadeIn(row2_label), FadeIn(row2_value)),
                lag_ratio=0.5,
            ),
            run_time=1.5,
        )
        clock.wait(1.0)

        move_arrow = Arrow([1.55, 0.45, 0], [1.55, -0.35, 0], color=GREY_B, stroke_width=3, buff=0)
        clock.play(Create(move_arrow), run_time=0.5)
        clock.wait(4.5)
        clock.end_beat(18)

        # ---------- Beat 20 (index 19): daily estimation, no change ----------
        row3_label = Text("daily, with blend", font_size=28, color=WHITE).move_to([-4.20, -1.70, 0])
        row3_value = Text("no change beyond 0.003", font_size=30, color=GREY_B).move_to([2.60, -1.70, 0])
        row3 = VGroup(row3_label, row3_value)
        clock.play(Write(row3), run_time=1.2)
        clock.play(Indicate(row3), run_time=0.8)
        clock.wait(2.5)
        clock.end_beat(19)

        # ---------- Beat 21 (index 20): the extra data was the cure ----------
        clock.play(
            FadeOut(VGroup(row1_label, row1_value, row2_label, row2_value, row3, move_arrow, blend_bar)),
            run_time=0.8,
        )
        cure_text = Text("the extra data was the cure", font_size=40, color=GREEN).move_to([0, 0.50, 0])
        clock.play(Write(cure_text), run_time=1.2)
        insurance_text = Text("the blend stays on as insurance", font_size=34, color=GREY_B).move_to([0, -0.40, 0])
        clock.play(Write(insurance_text), run_time=1.0)
        clock.wait(2.5)
        clock.end_beat(20)

        # ---------- Beat 22 (index 21): now the leftovers ----------
        clock.play(
            FadeOut(VGroup(cure_text, insurance_text, card1, card2, card3)),
            run_time=0.8,
        )
        title2 = Text("Now the leftovers", font_size=42, color=GREY_B).move_to([0, 3.10, 0])
        clock.play(ReplacementTransform(title, title2), run_time=1.0)

        stack_left = Rectangle(width=4.0, height=0.90, fill_color=BLUE, fill_opacity=0.55, stroke_width=0)
        stack_left.move_to([-2.0, 1.20, 0])
        stack_left_label = Text("factor", font_size=30, color=WHITE).move_to([-2.0, 1.20, 0])
        stack_right = Rectangle(width=4.0, height=0.90, fill_color=GREY_B, fill_opacity=0.55, stroke_width=0)
        stack_right.move_to([2.0, 1.20, 0])
        stack_right_label = Text("specific", font_size=30, color=WHITE).move_to([2.0, 1.20, 0])
        stacked_bar = VGroup(stack_left, stack_left_label, stack_right, stack_right_label)

        clock.play(
            GrowFromEdge(stack_left, RIGHT), GrowFromEdge(stack_right, LEFT),
            FadeIn(stack_left_label), FadeIn(stack_right_label),
            run_time=1.2,
        )
        names30_text = Text("30 names", font_size=30, color=WHITE).move_to([0, 2.15, 0])
        clock.play(Write(names30_text), run_time=0.6)
        clock.wait(2.0)
        clock.end_beat(21)

        # ---------- Beat 23 (index 22): own residuals, structural prior ----------
        clock.play(stacked_bar.animate.move_to([0, 2.65, 0]).scale(0.6), run_time=0.8)
        clock.wait(1.0)

        box_left = Rectangle(width=4.4, height=1.5, stroke_color=GREY_B, stroke_width=3,
                              fill_color=GREY_B, fill_opacity=0.10).move_to([-2.70, 0.35, 0])
        box_left_label = Text("own squared residuals", font_size=28, color=WHITE).move_to([-2.70, 0.35, 0])
        clock.play(FadeIn(box_left), FadeIn(box_left_label), run_time=1.0)
        clock.wait(0.8)

        box_right = Rectangle(width=4.4, height=1.5, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.10).move_to([2.70, 0.35, 0])
        box_right_label = Text("predicted from size, liquidity,\nindustry", font_size=24, color=WHITE)
        box_right_label.move_to([2.70, 0.35, 0])
        clock.play(FadeIn(box_right), FadeIn(box_right_label), run_time=1.2)
        clock.wait(1.0)

        time_series_label = Text("time series", font_size=26, color=GREY_B).move_to([-2.70, -0.65, 0])
        structural_label = Text("structural prior", font_size=26, color=TEAL).move_to([2.70, -0.65, 0])
        clock.play(FadeIn(time_series_label), FadeIn(structural_label), run_time=0.8)
        clock.wait(3.5)
        clock.end_beat(22)

        # ---------- Beat 24 (index 23): both sources converge ----------
        arrow_left2 = Arrow([-2.70, -0.95, 0], [0, -1.75, 0], color=WHITE, stroke_width=3, buff=0)
        arrow_right2 = Arrow([2.70, -0.95, 0], [0, -1.75, 0], color=WHITE, stroke_width=3, buff=0)
        clock.play(Create(arrow_left2), Create(arrow_right2), run_time=0.8)

        slider_line = Line([-3.20, -2.45, 0], [3.20, -2.45, 0], color=GREY_B, stroke_width=4)
        slider_left_label = Text("all prior", font_size=24, color=GREY_B).move_to([-4.30, -2.45, 0])
        slider_right_label = Text("all measured", font_size=24, color=GREY_B).move_to([4.50, -2.45, 0])
        slider_dot = Dot(point=[0, -2.45, 0], radius=0.11, color=WHITE)
        clock.play(
            Create(slider_line), FadeIn(slider_left_label), FadeIn(slider_right_label), FadeIn(slider_dot),
            run_time=0.6,
        )
        clock.end_beat(23)

        # ---------- Beat 25 (index 24): the six-week-old name, weight 0.19 ----------
        yellow_square = Square(side_length=0.44, stroke_color=YELLOW, stroke_width=4,
                                fill_color=YELLOW, fill_opacity=0.30).move_to([0, -1.15, 0])
        clock.play(FadeIn(yellow_square), run_time=0.6)
        clock.wait(0.5)

        clock.play(slider_dot.animate.move_to([-1.98, -2.45, 0]).set_color(YELLOW), run_time=1.2)
        clock.wait(0.5)

        days30_text = Text("30 days of history", font_size=28, color=YELLOW).move_to([0, -3.15, 0])
        clock.play(Write(days30_text), run_time=0.8)
        weight_text = Text("blend weight 0.19", font_size=30, color=YELLOW).move_to([2.60, -1.90, 0])
        clock.play(Write(weight_text), run_time=0.8)
        clock.wait(3.0)
        clock.end_beat(24)

        # ---------- Beat 26 (index 25): published for every name ----------
        clock.play(
            FadeOut(VGroup(box_left, box_left_label, box_right, box_right_label,
                           time_series_label, structural_label, arrow_left2, arrow_right2, names30_text)),
            run_time=0.8,
        )
        remaining_group = VGroup(slider_line, slider_left_label, slider_right_label, slider_dot,
                                  yellow_square, days30_text, weight_text)
        clock.play(remaining_group.animate.move_to([0, 0.30, 0]), run_time=1.0)

        published_text = Text("published for every name", font_size=34, color=GREEN).move_to([0, 2.00, 0])
        clock.play(Write(published_text), run_time=1.0)
        clock.wait(2.5)
        clock.end_beat(25)

        # ---------- Beat 27 (index 26): closing verdict ----------
        clock.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        closing1 = Text("Three repairs, all measured.", font_size=38, color=WHITE).move_to([0, 0.50, 0])
        clock.play(Write(closing1), run_time=1.0)
        closing2 = Text("Only two of them changed a number.", font_size=38, color=GREY_B).move_to([0, -0.40, 0])
        clock.play(Write(closing2), run_time=1.0)
        clock.wait(1.5)
        clock.end_beat(26)
