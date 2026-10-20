# Architecture

**English** · [简体中文](zh-CN/Architecture.md)

High-level modules and data flow. Paths refer to the original project; this repository does not include the source.

## Layers

```
Assets/_Project/Scripts/
├─ Domain/        Plain C# rules and data (card assets, market, personas, talents, saves)
├─ Tcg/           Built-in card game rules and match engine
├─ App/           Game flow, UI, scene assembly, the computer's sites
├─ Interaction/   First-person interaction (pick up, place, inspect, counter, backpack)
├─ Npc/           Customers, sellers and duelists: behaviour and animation
├─ Player/        First-person controller
└─ Localization/  English / Chinese text catalogues and switching
```

Scale: about 375 C# files including third-party code, roughly 270 of them project-owned; about 108 test files (43 EditMode, 65 PlayMode).

## Core principles

1. **Domain is separate from presentation.** `Domain` does not depend on scene objects, so pricing, grading, negotiation, personas, the talent web and saves are covered by plain EditMode unit tests.
2. **One card = one instance.** Price, condition, authenticity, ownership and location live on the same card instance. Putting it on display, into a deck or selling it only changes where it is or who owns it — it never copies data.
3. **Hidden information is hidden by the system.** True authenticity, true grade and personal reputation cannot be read directly. The player only gets evidence: the loupe (a range that narrows as you look), UV light (depends on lamp tier), the market computer.
4. **Data-driven.** Card sets, talent nodes, products and NPC traits are defined in data and configuration, not hard-coded in rules.
5. **Every player-facing string is a localization key.** One catalogue per language, key for key, with English as the fallback. A PlayMode audit sweeps the live UI in English and fails if any Chinese is still on screen.

## Main data flow

```
Wholesale computer (MERIDIAN / PALLET / SHARD / LOT 47 / STOCK)
   │ order
   ▼
Delayed delivery → back room / shelves ──open pack──► card instances (Domain)
                                                      │
        Customers / sellers (Npc) ◄───────────────────┤ price, authenticity, grade
              │ dialogue / negotiation                │
              ▼                                       ▼
        Counter interaction (Interaction) → cash / reputation / stock → save (Saves)
              │
              └─► Play tables → Tcg match engine → physical card presentation
```

## Subsystems

| Subsystem | Notes |
|---|---|
| Card assets | Unique instances, condition ladder, authenticity, grading |
| Buying negotiation | Seller claims plus evidence-based claim cards; loupe range narrows with inspection; UV by lamp tier; patience and reputation |
| Market economy | Daily price movement, wholesale channels, precious-metal and scrap prices |
| Shop operations | Day cycle, tidiness, litter, security (theft and recovery), upgrades and expansion |
| NPCs | Customers, sellers and duelists with personality tags (e.g. introvert, impatient, expert) |
| Built-in TCG | Lanes, energy, fragments; played on physical tables; 8- and 16-player tournaments |
| Personas and talents | Nine personas, a 160-node talent web, cost-free keystone talents |
| The street | A pawn shop (buys scrap), fishing and a tackle shop, the riverside behind the shop |
| Saves | Versioned saves; when the talent web was restructured, old allocations were refunded wholesale |
| Localization | English / Chinese |

## Automated verification

- Headless Unity compile checks and batch scripts (`Tools/Unity/Invoke-UnityBatch.ps1`).
- EditMode: rules and numbers (259 tests passing as of 2026-10-21).
- PlayMode evidence tests: run a whole tournament day, drinks service, the fishing fight, computer clicks, negotiation flows, and an English-UI audit; each saves screenshots as visual evidence.
