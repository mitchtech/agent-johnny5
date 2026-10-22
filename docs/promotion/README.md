# Agent Johnny 5 promotion kit

An owner-run, 30-day organic campaign for successful installs, GitHub visibility,
and recognition of Michael J. Mitchell as the maker. Budget: 3-5 hours per week,
no ad spend. The destructive-command alarm is the hook; the event map is the
substance. The Codex pet gets its own demonstration and is measured separately.

## Start here

1. Read [validation and launch readiness](validation.md). Complete the remaining
   physical/native checks before claiming a live host demonstration.
2. Use the [install walkthrough](install.md) to help early users.
3. Review [ready-to-edit posts](posts.md), the [maker story](maker-story.md), and
   [answers to common questions](responses.md).
4. Select the appropriate [media and capture script](demos.md).
5. Record publications and voluntary feedback in [campaign.csv](campaign.csv).
   Keep personal feedback details in a private copy, not a public PR.

This kit prepares promotion; it does not publish posts, contact people, schedule
messages, or submit the project to directories. Michael reviews and publishes
from his accounts. Distribution continues through this repository, Releases,
Pages, and compatible official host channels. npm registry publication remains
deferred.

## Positioning and destinations

> Agent Johnny 5 plays Johnny 5's lines from *Short Circuit* when Claude Code,
> Codex, or Gemini CLI needs you: "Need input" for approvals, "I have questions"
> for questions, and "No disassemble, Number Five!" when the approval is for
> `rm -rf` or a force push. Runs locally, with no runtime telemetry. An optional
> Codex pet with nine animations installs independently.

Primary audience: developers running local Claude Code or Codex sessions who
want audible attention cues. Secondary audience: Agent Navi users who want a
different voice. Tertiary audience: Codex users who enjoy custom pets. Gemini
support is a supporting fact, not another campaign.

Use one primary link per post:

- Install: <https://github.com/mitchtech/agent-johnny5#install>
- Event map: <https://github.com/mitchtech/agent-johnny5#sounds>
- Interactive preview: <https://mitchtech.github.io/agent-johnny5/>
- Pet posts: <https://mitchtech.github.io/agent-johnny5/#pet>

Lead with an actual behavior, identify yourself as the maker, state that the
project is free to try, and invite one specific piece of feedback. Do not imply
every host has identical events, that the destructive-command cue is a safety
feature, or that a sound proves the agent completed a task successfully. Avoid
unmeasured time-saving claims. Do not imply the pet appears in Claude Code or
Gemini, or that the atlas preview is a native host recording.

## Publishing calendar

Day 1 is the owner's first preparation day. Start publication after the launch
checks are complete, not on an invented fixed launch date. Pick a time when you
can answer replies for the following hour. The budgets below include replies.

| Timing | Action | Budget |
|---|---|---|
| Days 1-7 | Capture baseline; verify fresh installs and physical audio; review copy; capture live demo if available | 5 hours |
| Day 8 | Publish X sound post X1 with the sound preview or a verified live clip | Included below |
| Day 10 | Share R1 in r/ClaudeCode's current weekly showcase thread | Included below |
| Day 12 | Publish LinkedIn L1 and link the maker story if it is publicly available | Days 8-14: 4 hours |
| Day 16 | Publish R2 in r/codex, with the current appropriate showcase flair | Included below |
| Day 18 | Publish X2 about the destructive-command alarm | Included below |
| Day 20 | Publish X3 about the attention preset | Days 15-21: 4 hours |
| Day 22 | Publish X5 with the pet preview or a verified native pet clip | Included below |
| Day 25 | Publish X4, a useful install/configuration follow-up | Included below |
| Day 27 | Publish LinkedIn L2 about the privacy boundary in command detection | Included below |
| Days 28-30 | Ask willing early users about continued use; write results and select the next channel | Days 22-30: 4 hours |

Spend approximately 45% of publishing/conversation time on Reddit, 35% on X,
and 20% on LinkedIn. Recheck rules, pinned threads, eligibility, and flair before
posting. r/ClaudeCode directs simple project sharing to its weekly showcase; do
not turn R1 into a standalone feed post. r/codex prioritizes useful setup
detail. If a destination does not permit the post, skip it and use that time to
help existing users. Do not work around moderation or solicit upvotes.

Sources: [r/ClaudeCode rules](https://www.reddit.com/r/ClaudeCode/about/rules.json),
[r/codex rules](https://www.reddit.com/r/codex/about/rules.json).

On posting days, return for roughly 15 minutes to answer follow-up questions.
Link Agent Johnny 5 in other conversations only when it answers the actual
question. Defer paid ads, Product Hunt, cold outreach, newsletters, and curated lists.

## Measurement and decisions

Targets are working goals, not forecasts or current usage claims:

| Outcome | Day-30 target | Measurement |
|---|---|---|
| Successful use | 10 distinct people voluntarily report a successful install | Replies or issue comments; count each person once privately |
| Continued use | 5 report using Johnny 5 after at least a week | Follow up only in an existing, willing conversation |
| Visibility | 25 net new GitHub stars | Difference from initial repository count |
| Product learning | 5 actionable observations | Reproducible blockers or specific preferences |
| Maker recognition | 3 substantive conversations about the work | Technical discussion, collaboration interest, unsolicited mentions |

Capture metrics at the beginning and on days 7, 14, 21, and 30:

```bash
python3 docs/promotion/capture-metrics.py
```

The standard-library script uses an already authenticated `gh` CLI, reads only
GitHub APIs, and writes a timestamped JSON file under ignored `dist/promotion/metrics`.
It captures stars, forks, releases/assets, and available traffic. An unavailable
endpoint is recorded as unavailable, never as zero. It does not install, publish,
modify GitHub settings, or contact users.

GitHub's traffic window is 14 days. Preserve weekly observations, but do not sum
overlapping windows or unique counts. Full clones, downloads, and stars do not
prove installation or retention. Exclude known validation downloads when
discussing campaign results. Platform impressions and referrers provide
approximate attribution, not an install conversion rate.
[GitHub traffic documentation](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository).

| Observation | Action |
|---|---|
| Two people hit the same install blocker | Fix instructions or behavior before the next promotion |
| Interest without install reports | Check destination and simplify the setup explanation |
| Sounds seem too frequent | Demonstrate the attention preset; do not change defaults for marketing |
| Someone treats the alarm as a safety guarantee | Correct it plainly: it is a cue, not a guard |
| Pet content attracts interest | Reply with pet-specific installation; count pet installs separately |
| A channel produces installs or substantive discussion | Give it the next available content slot |
| Two distinct posts on a channel produce neither | Stop adding posts there during this campaign |

At day 30, complete [results.md](results.md). Continue at two hours per week on
the strongest channel if five people report continued use. Otherwise address
the leading adoption obstacle before another promotional effort.
