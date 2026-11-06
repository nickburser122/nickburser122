Alternate account. Main account: [datakid](https://github.com/datakid).

Pharmacy, insurance and data tools. Most are static web apps that run in the browser; the exceptions are marked below.

### Selected tools

| Tool | What it does, and what it does not | Network / install |
| --- | --- | --- |
| [Daleel](https://github.com/nickburser122/460-prices) · [live](https://460-prices.vercel.app) | Searches 2,714 records from Egypt's HIO price lists (decrees 460/2024 and 996/2020), with a source and confidence score on each amount. Beneficiary co-payments outside radiology are not covered. | No network calls after load; loads Google Fonts from a CDN. Not installable; no service worker. |
| [AG Search](https://github.com/nickburser122/AG-search) · [live](https://ag-search.vercel.app) | Typo-tolerant lookup over 1,121 formulary items: 977 free and 144 paid with a patient contribution. The data is the formulary file bundled in the repository. | Installable (PWA); works offline after the first load. Loads Google Fonts from a CDN. |
| [Bayan](https://github.com/nickburser122/bayan) · [live](https://bayan-mauve.vercel.app) | Analyses health-insurance pharmacy cost reports from xlsx, xls and xlsm files read in the browser. The interface is Arabic and right-to-left only. | No network calls after load; loads Google Fonts from a CDN. Not installable; no service worker. |
| [Cadence](https://github.com/nickburser122/alt-plan-maker) · [live](https://alt-plan-maker.vercel.app) | Builds visit rotations for teams visiting facilities, in English and Arabic. The solver uses simulated annealing, so a plan is a good result, not a proven optimum. | No network calls after load; loads Google Fonts from a CDN. Not installable; no service worker. |
| [Duckbench](https://github.com/nickburser122/duckbench) · [live](https://duckbench.vercel.app) | Cleans, reshapes, joins and exports files in two engines: Full (DuckDB-wasm, every transform, Parquet) and Express (Arquero, common transforms, CSV and Excel only). Full downloads DuckDB-wasm at run time, so its first load needs a connection. | Calls registry.npmjs.org for the latest DuckDB version when asked; nothing else leaves the browser. Loads DuckDB-wasm and Arquero from a CDN. Not installable; no service worker. |
| [Waymark](https://github.com/nickburser122/Waymark) · [live](https://waymark-hazel.vercel.app) | Care-routing and clinic-flow tool; every feature runs through one six-stage pipeline from demand to decision. It must be served over HTTP, because modules and the batch worker do not load from `file://`. | No network calls. Files stay in the tab. Not installable; no service worker. |
| [Tarq](https://github.com/nickburser122/typing-practice) · [live](https://typing-practice-wine-eta.vercel.app) | Typing trainer in English and Arabic, built into one self-contained `index.html`. Progress is kept in `localStorage`, so it is per browser and per device. | No network calls. Files stay in the tab. Not installable; no service worker. |
| [Tacit](https://github.com/nickburser122/tacit) | Keyboard-first Android launcher: one search field opens apps, contacts and files. It asks for contacts, phone-call and all-files permissions. | Android (Kotlin); APK in Releases. No INTERNET permission is declared. |

### Formulary and search

- [lx-search-svg](https://github.com/nickburser122/lx-search-svg) — Lx Search. Formulary lookup. Installable (PWA); works offline after the first load.
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
- [entity-tracker](https://github.com/nickburser122/entity-tracker) — Contracted-entity statements. Calls Firebase for storage, and Google Sheets when sync is used; nothing else leaves the browser.
- [entity-viewer](https://github.com/nickburser122/entity-viewer) — Reads entity statements. No network calls after load; loads SheetJS and Google Fonts from a CDN.
- [roi-calculator](https://github.com/nickburser122/roi-calculator) — Investment-return calculator. No network calls after load; loads SheetJS from a CDN.
- [tacit-web](https://github.com/nickburser122/tacit-web) — Tacit start page. Installable (PWA); works offline after the first load.

### Utilities, data and games

- [icleaner](https://github.com/nickburser122/icleaner) — Pasted text to table. No network calls after load; loads Google Fonts from a CDN.
- [simple-font-maker](https://github.com/nickburser122/simple-font-maker) — Handwriting to font. Installable (PWA); works offline after the first load.
- [basic-cover](https://github.com/nickburser122/basic-cover) — Printable cover forms. No network calls after load; loads Google Fonts from a CDN.
- [survival-mirror2](https://github.com/nickburser122/survival-mirror2) — Population survival curves. No network calls. Files stay in the tab.
- [sloppy-bird](https://github.com/nickburser122/sloppy-bird) — Above the Fold game. Installable (PWA); works offline after the first load.

### Archived or superseded

- [app-launcher](https://github.com/nickburser122/app-launcher) — LinkExpress. Superseded by the launcher on [datakid](https://github.com/datakid).

Forks on this account (app-launcher, daftar, duckbench, lx-search-svg, newlist-svg, survival-mirror2) are forks of repositories on datakid, not third-party code.
