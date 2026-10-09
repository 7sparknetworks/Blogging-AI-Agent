# EarnPace — "Set Your Pace" (18.5 s, 1920×1080, 60 fps)

**Brand inputs:** earnpace.com could not be reached from the build environment (egress blocked), so this uses the
EarnPace brand rulebook: four pillars (make, save, manage, grow money), the "Green Stride" palette
(#003024 deep green, #39C900 accent, #F5F7F2 background, #1F6B00 link green), and plain, research-first,
no-hype language. To meet the YMYL rules, no income figures, returns or promises appear anywhere.

**Visual through-line:** one line and one dot run through the whole film. The line starts as a frantic,
falling coral ticker, calms into a steady green track, folds up into a staircase, becomes a growth chart,
and ends as the stair mark in the logo. The dot is "you" from start to finish.

| # | Time | Headline (on screen) | Visual | Transition out |
|---|------|----------------------|--------|----------------|
| 1 | 0.0 – 3.4 s | **Money moves fast.** / Most of us are just chasing it. | Near-black frame. A jagged coral ticker line races right and falls, with the dot chasing at its tip. Expense chips (−$4.89 coffee, −$1,450 rent…) and speed streaks stream past. | The jagged line damps out like a settling spring, turns from coral to green, and the background floods deep green. The text lifts away. |
| 2 | 3.4 – 6.2 s | **So stop chasing.** / Set your **pace.** | A calm, straight green line with track ticks gliding by and a faint grid. The dot pulses steadily, like a metronome. | The line ahead of the dot folds upward into four steps, and the dot hops onto the first one. |
| 3 | 6.2 – 12.2 s | 01 **Earn** a little more. → 02 **Save** it first. → 03 **Manage** every dollar. → 04 **Grow** it over time. | The camera climbs with the dot, one step every 1.5 s. Each landing squashes the dot, lights the step and sends out a pulse ring, and that step's icon builds above it: coins stack, a jar fills, a budget donut sweeps, a sprout grows. | The camera pulls far back. The four steps fill in as the first bars of a long bar chart, and six more bars rise to the right. |
| 4 | 12.2 – 15.0 s | **Step by step,** / **it adds up.** | A glowing curve draws over the bar tops, catches the dot and carries it to the top. There are no numbers, just the shape of steady progress. | The dot flashes, and a light circle bursts out from it to wipe to the brand frame. |
| 5 | 15.0 – 18.5 s | **EarnPace** / Make, save, manage and grow your money — at your pace. / earnpace.com | A light Green Stride frame. The logo mark (a stair with the dot on top, the whole story in one glyph) springs in, the wordmark rises letter by letter, then the tagline and URL pill appear. This frame holds for about 1.2 s. | End. |

## Story check
- **Beginning (problem):** money feels like something you chase (1).
- **Turn (reframe):** you can set the pace yourself (2).
- **Progression (method):** the four EarnPace pillars as four steps, in the order the site teaches them (3).
- **Result:** small steps add up over time, shown by the same staircase from further back (4).
- **Ending (who helps):** EarnPace, whose name itself says "earn at your pace" (5).

Read the headlines in order: *Money moves fast. Most of us are just chasing it. So stop chasing. Set your pace.
Earn a little more. Save it first. Manage every dollar. Grow it over time. Step by step, it adds up.
EarnPace. Make, save, manage and grow your money, at your pace.* They read as one continuous thought.

Note: the wordmark is typeset in Inter Display as a stand-in. Swap in `EarnPace-Official-Logo-scaled.png` if the
official logo must appear.

## Files / re-render
- `EarnPace-Set-Your-Pace.mp4`: final cut, 18.5 s, 1920×1080, 60 fps, H.264 + AAC.
- `index.html`: the animation, rendered deterministically on canvas. Open it with `?play` for a live preview.
- `sound.py`: synthesised sound design, with cues locked to the same timeline.
- `render.mjs`: Playwright frame capture → ffmpeg, with 4-sample motion blur per frame.

```
python3 sound.py /tmp/sound.wav
NODE_PATH=$(npm root -g) node render.mjs video EarnPace-Set-Your-Pace.mp4 /tmp/sound.wav
```
