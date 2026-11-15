# Alternate account for [datakid](https://github.com/datakid)

Pharmacy, insurance and data tools. Most are static web apps that run in the browser; the exceptions are marked below. Each entry states what the tool does, what it does not do, and whether it touches the network.

[Selected tools](#selected-tools) · [How these are built](#how-these-are-built) · [More tools](#more-tools) · [Formulary and search](#formulary-and-search) · [Reporting and analytics](#reporting-and-analytics-arabic) · [Trackers and launchers](#trackers-and-launchers) · [Utilities, data and games](#utilities-data-and-games) · [Archived](#archived-or-superseded)

### Selected tools

Three tools with the most recorded checks. Each ledger lists what has been run and what has not. Every row comes from a file in that tool's repository. Screenshots show the apps with bundled or seeded data; the Tacit captures come from CI emulators.

#### Tacit

[Source](https://github.com/nickburser122/tacit) · [Known limits](https://github.com/nickburser122/tacit/blob/main/docs/limits.md) · [Decisions](https://github.com/nickburser122/tacit/blob/main/docs/decisions.md)

![Tacit search results: a settings screen, a file, a folder, a snippet, a clipboard entry, a calculator result, a web search and a link](assets/tacit-light.png#gh-light-mode-only)
![Tacit search results: a settings screen, a file, a folder, a snippet, a clipboard entry, a calculator result, a web search and a link](assets/tacit-dark.png#gh-dark-mode-only)

Keyboard-first Android launcher: one search field opens apps, contacts, files, settings screens and quicklinks. Typos are matched by a budget that grows with word length, and Arabic letters are folded so Latin spellings find Arabic names. It asks for contacts, phone-call and all-files permissions. No INTERNET permission is declared.

| Checked | Not checked |
| --- | --- |
| 68 test source files. Unit tests and device tests run in CI on Android 14, 15 and 16 emulators. | Nothing has been measured on a real phone. The 35-item on-device checklist in `docs/HANDOFF.md` has no ticked item. |
| Ranking and file search are compared against golden files. | Benchmark numbers come from an API 35 emulator and are a trend only. |
| The release build is repeated in CI and compared byte for byte. | `SettingsApplyTest` failed once in each of three milestones and passed on re-run. The cause is not found. |

#### Cadence

[Source](https://github.com/nickburser122/alt-plan-maker) · [Live](https://alt-plan-maker.vercel.app) · [Solver status](https://github.com/nickburser122/alt-plan-maker/blob/main/docs/solver-plan-status.md)

![Cadence Insights tab for a one-month plan: 61 of 61 seats filled, 0 rule breaks, and the rules audit](assets/cadence-light.png#gh-light-mode-only)
![Cadence Insights tab for a one-month plan: 61 of 61 seats filled, 0 rule breaks, and the rules audit](assets/cadence-dark.png#gh-dark-mode-only)

Builds visit rotations for teams visiting facilities, in English and Arabic. The solver uses simulated annealing, so a plan is a good result and not a proven optimum. No network calls after load; loads Google Fonts from a CDN. Not installable; no service worker.

| Checked | Not checked |
| --- | --- |
| 53 Node checks pass: oracle, fixtures, moves, preflight and golden. | A plan is not proven optimal. The exact checks cover open seats and rest conflicts. |
| 40 golden runs reproduce identically. | The 1.5x speed target for a quarter plan is not met. |
| The open-seat lower bound is tight on 79 of 83 instances that have one. The solver never beats it across 120 random instances. | |

#### Tarq

[Source](https://github.com/nickburser122/typing-practice) · [Live](https://typing-practice-wine-eta.vercel.app)

![Tarq Learn screen: a lesson on four unlocked keys, with the on-screen keyboard below](assets/tarq-light.png#gh-light-mode-only)
![Tarq Learn screen: a lesson on four unlocked keys, with the on-screen keyboard below](assets/tarq-dark.png#gh-dark-mode-only)

Typing trainer in English and Arabic, built into one self-contained `index.html`. The Content-Security-Policy sets `connect-src 'none'`. Progress is kept in `localStorage`, so it is per browser and per device. No network calls. Files stay in the tab. Not installable; no service worker.

| Checked | Not checked |
| --- | --- |
| 192 headless engine tests pass in Node. | Lesson progress is compared on simulated typists, not on people. |
| The build fails on network calls, native dropdowns and a module boundary violation. | On a Mac, the number row and shifted symbols are not modelled, because the repository has no verified key table for them. Their hints follow Arabic 101. |

### How these are built

The code in these repositories is written by AI models. The usual workflow is Claude Opus 5.5 planning a change and Claude Sonnet 5.5 carrying it out. Claude Fable 5.2 is used rarely, as a creative director. Opus and Sonnet review the output, and how much review a project gets depends on its complexity. Which model did which part of a tool is not recorded. The owner sets the rules a change must follow, for example no code comments in Tacit and no INTERNET permission.

Where a tool has them, files in `docs/` record the build. [Tacit's decisions](https://github.com/nickburser122/tacit/blob/main/docs/decisions.md) explain why the code is as it is. [Cadence's solver status](https://github.com/nickburser122/alt-plan-maker/blob/main/docs/solver-plan-status.md) lists each option and the evidence behind its default. The ledgers above state what has been run and what has not.

### More tools

| Tool | What it does, and what it does not | Network / install |
| --- | --- | --- |
| [Daleel](https://github.com/nickburser122/460-prices) · [live](https://460-prices.vercel.app) | Searches 2,714 records from Egypt's HIO price lists (decrees 460/2024 and 996/2020), with a source and confidence score on each amount. Beneficiary co-payments outside radiology are not covered. | No network calls after load; loads Google Fonts from a CDN. Not installable; no service worker. |
| [AG Search](https://github.com/nickburser122/AG-search) · [live](https://ag-search.vercel.app) | Typo-tolerant lookup over 1,121 formulary items: 977 free and 144 paid with a patient contribution. The data is the formulary file bundled in the repository. | Installable (PWA); works offline after the first load. Loads Google Fonts from a CDN. |
| [Bayan](https://github.com/nickburser122/bayan) · [live](https://bayan-mauve.vercel.app) | Analyses health-insurance pharmacy cost reports from xlsx, xls and xlsm files read in the browser. The interface is Arabic and right-to-left only. | No network calls after load; loads Google Fonts from a CDN. Not installable; no service worker. |
| [Duckbench](https://github.com/nickburser122/duckbench) · [live](https://duckbench.vercel.app) | Cleans, reshapes, joins and exports files in two engines: Full (DuckDB-wasm, every transform, Parquet) and Express (Arquero, common transforms, CSV and Excel only). Full downloads DuckDB-wasm at run time, so its first load needs a connection. | Calls registry.npmjs.org for the latest DuckDB version when asked; nothing else leaves the browser. Loads DuckDB-wasm and Arquero from a CDN. Not installable; no service worker. |
| [Waymark](https://github.com/nickburser122/Waymark) · [live](https://waymark-hazel.vercel.app) | Care-routing and clinic-flow tool; every feature runs through one six-stage pipeline from demand to decision. It must be served over HTTP, because modules and the batch worker do not load from `file://`. | No network calls. Files stay in the tab. Not installable; no service worker. |

### Formulary and search

- [lx-search-svg](https://github.com/nickburser122/lx-search-svg) — Lx Search. Formulary lookup. Installable (PWA); works offline after the first load. Loads Google Fonts from a CDN.
- [newlist-svg](https://github.com/nickburser122/newlist-svg) — LX Search 4.1. Medicine search with calculator. No network calls after load; loads Google Fonts from a CDN.

### Reporting and analytics (Arabic)

- [msar](https://github.com/nickburser122/msar) — Masar. Inspection-visit analytics. No network calls after load; loads SheetJS and Google Fonts from a CDN.
- [letters](https://github.com/nickburser122/letters) — Letter counts. No network calls after load; loads SheetJS and Google Fonts from a CDN.
- [visit-tracker](https://github.com/nickburser122/visit-tracker) — Addad. Travel allowances. No network calls after load; loads Google Fonts from a CDN.
- [daftar](https://github.com/nickburser122/daftar) — Ledger reports from dispensing sheets. No network calls. Files stay in the tab.
- [MIzan](https://github.com/nickburser122/MIzan) — Mizan. Splits incentive pools. No network calls after load; loads SheetJS and Google Fonts from a CDN.
- [rushed-plan](https://github.com/nickburser122/rushed-plan) — Weekly visit planner. No network calls after load; loads Google Fonts from a CDN.

### Trackers and launchers

- [To-Do](https://github.com/nickburser122/To-Do) — Gov To Do. Calls the Google Sheets API when sync is configured; nothing else leaves the browser.
- [entity-tracker](https://github.com/nickburser122/entity-tracker) — Contracted-entity statements. Calls Firebase for storage and sign-in, and Google Sheets when sync is used. Loads the Firebase SDK, Google sign-in, SheetJS and Google Fonts from CDNs.
- [entity-viewer](https://github.com/nickburser122/entity-viewer) — Reads entity statements. No network calls after load; loads SheetJS and Google Fonts from a CDN.
- [roi-calculator](https://github.com/nickburser122/roi-calculator) — Investment-return calculator. No network calls after load; loads SheetJS and Google Fonts from a CDN.
- [tacit-web](https://github.com/nickburser122/tacit-web) — Tacit start page. Installable (PWA); works offline after the first load.

### Utilities, data and games

- [randomizer](https://github.com/nickburser122/randomizer) — Passwords, fake-data tables, random picks, dice and tokens. Passwords use the browser's cryptographic generator; a seeded table does not, so it is not for secrets. No network calls. Files stay in the tab.
- [icleaner](https://github.com/nickburser122/icleaner) — Pasted text to table. No network calls after load; loads Google Fonts from a CDN.
- [simple-font-maker](https://github.com/nickburser122/simple-font-maker) — Handwriting to font. Installable (PWA); works offline after the first load.
- [basic-cover](https://github.com/nickburser122/basic-cover) — Printable cover forms. No network calls after load; loads Google Fonts from a CDN.
- [survival-mirror2](https://github.com/nickburser122/survival-mirror2) — Population survival curves. No network calls. Files stay in the tab.
- [sloppy-bird](https://github.com/nickburser122/sloppy-bird) — Above the Fold game. Installable (PWA); works offline after the first load.

### Archived or superseded

- [app-launcher](https://github.com/nickburser122/app-launcher) — LinkExpress. Superseded by the launcher on [datakid](https://github.com/datakid).
