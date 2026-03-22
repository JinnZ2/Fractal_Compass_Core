# CLAUDE.md — Fractal Compass + CDDA Core

## Quick Start

```bash
python3 main.py
```

No dependencies required — pure Python 3.9+ standard library only.

## Project Overview

A prototype symbolic reasoning engine that builds recursive glyph-based trees ("blooms") and analyzes emergent themes across multiple knowledge domains using a Cross-Domain Discovery Algorithm (CDDA).

**Status:** Early prototype. Many components use placeholder/stub logic intended for future AI model integration.

## Architecture

Three-module pipeline with a single orchestrator:

```
main.py (orchestrator)
  │
  ├── fractal_compass.py  →  Builds recursive symbolic tree ("bloom")
  ├── bridge.py            →  Extracts dominant theme from tree
  └── cdda_engine.py       →  Analyzes theme across domains
```

**Data flow:** Seed glyph → `fractal_compass()` → SymbolicNode tree → `compass_to_cdda()` → theme string → `run_cdda()` → structured analysis dict

## File Reference

| File | Purpose | Key exports |
|------|---------|-------------|
| `main.py` | Entry point, demonstrates full pipeline | — |
| `fractal_compass.py` | Core tree engine | `SymbolicNode` class, `fractal_compass()`, `print_tree()` |
| `bridge.py` | Symbolic-to-semantic translator | `compass_to_cdda()` |
| `cdda_engine.py` | Cross-domain analysis engine | `run_cdda()` |

## Key Concepts

- **SymbolicNode**: Tree node with `glyph`, `domain`, `parent`, `children`, `resonance_score` (0–1 float)
- **Glyphs**: Symbolic markers — `↺` (inversion), `🕸` (web/connection), `◐` (duality), `⚛️` (structure), `📖` (knowledge), `💓` (emotion)
- **Domains**: Knowledge areas passed as string lists (e.g., `["Biology", "Mythology", "Psychology"]`)
- **Bloom**: The recursive tree expansion process — each node spawns 2 children per depth level
- **CDDA**: Cross-Domain Discovery Algorithm — analyzes a theme across multiple domains, returning confidence, scope, limitations, and follow-up questions

## Code Conventions

- **Naming**: `snake_case` for functions/variables, `CamelCase` for classes
- **No type hints** used in the current codebase
- **No docstrings** on most functions (only `run_cdda` and `compass_to_cdda` have them)
- **No external dependencies** — intentional design choice for portability
- **Randomized output**: Tree generation uses `random` module, so output is non-deterministic

## Extension Points

When modifying or extending this codebase:

1. **Adding glyphs**: Update the glyph list in `fractal_compass.py:24` and add corresponding theme mappings in `bridge.py:19-26`
2. **Adding domains**: Pass new domain strings via the `domains` parameter — no code changes needed
3. **AI integration**: `cdda_engine.py` is designed as a stub — replace the placeholder logic in `run_cdda()` with actual AI model calls
4. **Tree branching**: The branching factor (currently 2) is hardcoded in `fractal_compass.py:23` — make dynamic as needed
5. **Theme mapping**: `bridge.py` uses hardcoded glyph-to-theme mapping — extend or replace with embedding-based matching

## Development Workflow

### Running

```bash
python3 main.py
```

### Testing

No test framework is configured yet. When adding tests:
- Use `pytest` as the test runner
- Create a `tests/` directory at the project root
- Key things to test: tree structure correctness, glyph counting in bridge, CDDA output schema

### Linting / Formatting

No linting tools are configured. The codebase follows standard PEP 8 style.

### Git

- **Default branch**: `main` (remote) / `master` (local)
- **Commit style**: Short descriptive messages (e.g., "Create main.py", "Update README.md")
- **No CI/CD pipelines** configured

## Dependencies

None. Only uses Python standard library (`random`).

**Python version**: 3.9+

## Common Pitfalls

- Output is **non-deterministic** due to `random.choice()` — don't expect reproducible results without seeding
- `cdda_engine.py` confidence calculation is a placeholder formula: `0.6 + 0.1 * len(domains)`, capped at 1.0
- The glyph `⚛️` is a multi-codepoint emoji — handle with care in string operations
- `bridge.py` only maps 3 specific glyphs to themes; all others fall through to a generic message

## Ecosystem — Fractal Compass Atlas

This repo is part of a larger symbolic reasoning ecosystem coordinated by the [Fractal-Compass-Atlas](https://github.com/JinnZ2/Fractal-Compass-Atlas).

**Relationship:** The Atlas is the hub that aggregates glyphs, fractals, and guides from multiple repos. This Core repo provides the bloom engine and CDDA pipeline that the Atlas draws from.

### Related Repositories

| Repo | Role |
|------|------|
| [Fractal-Compass-Atlas](https://github.com/JinnZ2/Fractal-Compass-Atlas) | Hub — aggregates symbolic data across all repos |
| [Rosetta-Shape-Core](https://github.com/JinnZ2/Rosetta-Shape-Core) | Shape and bridge definitions |
| [Polyhedral-Intelligence](https://github.com/JinnZ2/Polyhedral-Intelligence) | Glyph sets and shape atlas |
| [Emotions-as-Sensors](https://github.com/JinnZ2/Emotions-as-Sensors) | Emotional signal processing |
| [Symbolic-Defense-Protocol](https://github.com/JinnZ2/Symbolic-Defense-Protocol) | Defense and protocol definitions |
| [ai-human-audit-protocol](https://github.com/JinnZ2/ai-human-audit-protocol) | Audit glyphs, protocols, logs |
| [BioGrid2.0](https://github.com/JinnZ2/BioGrid2.0) | Biological grid glyph registry |

## Fieldlink

This repo uses `.fieldlink.json` to declare its relationship within the Atlas ecosystem.

**What it does:** Fieldlink is a cross-repo configuration protocol that defines which remote repositories to pull symbolic data from, how to mount remote paths locally, and in what order to merge data.

**Key fields in `.fieldlink.json`:**
- `role` — this repo's identity in the ecosystem (`["fractals", "core", "engine"]`)
- `sources` — remote repos to pull from (currently: Atlas)
- `mounts` — maps remote file paths to local paths for data integration
- `merge.strategy` — `"deep-merge"` combines local and remote data
- `cache_dir` — `.fieldcache/` stores fetched remote data (gitignored)
- `consent` — license and sharing permissions per source

**To add a new source repo**, append an entry to the `sources` array in `.fieldlink.json` following the existing pattern.

## Project Roadmap

Per README, planned future work includes:
- Visual bloom rendering
- Semantic clustering and glyph embeddings
- Real-time question mapping and feedback loops
- Integration with symbolic-sensor-suite
- AI/LLM integration for enhanced CDDA output
