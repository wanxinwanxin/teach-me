# teachme visual style guide (3Blue1Brown-inspired)

These rules govern every scene. The critic grades against them.

## Composition
1. One idea on screen at a time. Before a new layout appears, fade out or
   transform away what the viewer no longer needs.
2. Nothing overlaps unless the overlap IS the point. Labels never sit on
   top of other labels, curves, or matrix entries.
3. Respect safe margins: keep all content inside x ∈ [-6.2, 6.2],
   y ∈ [-3.5, 3.5]. Titles live at the top; they shrink and move to the
   corner once the content arrives, or fade out.
4. Text is scarce. At most ~15 words visible at once, besides equations
   and axis labels. The narration carries the sentences; the screen
   carries the objects.

## Continuity ("objects have identity")
5. A concept keeps its color for the whole video. When the storyboard
   assigns a palette (e.g., returns = yellow, factors = blue, residuals =
   gray), obey it in every scene.
6. Prefer Transform / ReplacementTransform / TransformMatchingTex over
   FadeOut + FadeIn. When an equation evolves, the viewer must see WHICH
   symbol became WHAT.
7. Build formulas piece by piece, each piece appearing exactly when the
   narration mentions it. Never dump a finished formula on screen.

## Legibility
8. Font sizes: titles ≥ 40, labels ≥ 28, equation scale ≥ 0.8 of default.
   If something must shrink below that to fit, redesign the layout instead.
9. High contrast on the dark background (#0e1015). Use the classic palette:
   BLUE (#58C4DD), YELLOW (#FFFF00 sparingly, prefer #F4D345), GREEN
   (#83C167), RED (#FC6255), TEAL, GOLD, and GREY_B for de-emphasis.
   Pure white text; never dark colors on the dark background.
10. Motion is meaning. Nothing moves without a reason, and every reason in
    the narration gets its motion on screen.

## Pacing
11. Sync to the narration beats you are given. The visual for a beat starts
    when the beat starts. Do not front-load all animation into the first
    seconds of a long beat: spread it, or hold a deliberate pause after the
    key move so the viewer can look.
12. Big reveals get a beat of stillness after them.
13. run_time guidance: small appearances 0.5–1s, transforms 1–2s, sweeping
    camera-level changes 2–3s. Nothing takes longer than 4s.

## Honesty
14. Every number, equation, and label must match the storyboard's content.
    Never invent data. If the spec gives concrete numbers, use exactly those.
