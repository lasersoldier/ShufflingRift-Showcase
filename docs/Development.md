# Development

**English** · [简体中文](zh-CN/Development.md)

## Who does what

| | Me (design / acceptance) | AI agents (implementation) |
|---|---|---|
| Gameplay design | Propose ideas, discuss round by round and **decide**; nothing is built before the design is settled | Offer options and trade-offs, write them up |
| Rules and numbers | Set direction and limits (e.g. "price = a base price that cannot be haggled + a grade premium") | Turn them into code and data |
| Code | Review behaviour and results | Implement, refactor, write tests |
| Art | Set style and the quality bar ("no flat boxes glued together") | Concept images (Codex image generation) → Blender scripts → import |
| Acceptance | Play it myself and decide whether it passes | Compile, test, capture screenshot evidence |

This is not "give an AI one sentence and accept the result": every feature goes through design discussion, a recorded decision, automated verification and my hands-on acceptance.

## Workflow

1. **Design before implementation.** Talk the gameplay through first, then write it into the frozen design spec and a decision log.
2. **Atomic tasks.** One module at a time, each with acceptance criteria — delivered per module rather than as scattered small fixes.
3. **Minimum sufficient verification.** Run the narrowest compile or test first, then the full EditMode / PlayMode suites.
4. **Visual evidence.** UI, animation and art changes need screenshots or frame sequences, checked against the concept before they reach me.
5. **Recoverable.** Each session ends by updating a state file, a work log and the current-task file, so the next session can pick up directly.

## Examples of my contribution

- The whole design of the buying-negotiation system and its three revisions: price structure, the three haggling moves, the penalty for wrongly accusing an expert, the introvert trait, and two ways to handle a caught forgery.
- Personas and the talent web: nine personas, how many intersection nodes sit between neighbours, and the principle that "costs live on personas, talents are free".
- Economy and shop layout: back room and warehouses, machines bought separately, batched deliveries, the pawn shop buying scrap.
- Art direction: a unified look of dark walnut, black metal and warm LED light; quality acceptance of every model.
- Repeated playtesting and change requests (for example removing the always-on inventory HUD and trimming interface text).

## How it is tested

```text
Compile check   Tools/Unity/Invoke-UnityBatch.ps1 (headless)
EditMode        rules, prices, personas, talent web, saves ... (259 tests)
PlayMode        a full tournament day, drinks service, fishing fight, negotiation, computer clicks, English-UI audit ...
Screenshots     captured automatically during PlayMode and kept as evidence
```

## Known limitations

- Mostly single-player; the multiplayer approach has not been locked.
- Some art is still procedural placeholder, to be replaced step by step.
- Look and feel still need to be confirmed by hand.
