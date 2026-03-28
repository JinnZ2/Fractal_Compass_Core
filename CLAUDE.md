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
| `glyph_set.json` | Canonical glyph definitions (22 symbols) | — |
| `bloom_logic.json` | Symbolic bloom relationships | — |

## Key Concepts

- **SymbolicNode**: Tree node with `glyph`, `domain`, `parent`, `children`, `resonance_score` (0–1 float)
- **Glyphs**: Symbolic markers defined in `glyph_set.json` (22 symbols). Scripts fall back to a hardcoded subset if the file is unavailable
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

1. **Adding glyphs**: Add to `glyph_set.json` and add bloom relationships in `bloom_logic.json`. Scripts load these automatically.
2. **Adding domains**: Pass new domain strings via the `domains` parameter — no code changes needed
3. **AI integration**: `cdda_engine.py` is designed as a stub — replace the placeholder logic in `run_cdda()` with actual AI model calls
4. **Tree branching**: The branching factor (currently 2) is hardcoded in `fractal_compass.py` — make dynamic as needed
5. **Theme mapping**: `bridge.py` auto-generates themes from `glyph_set.json` meanings — extend or replace with embedding-based matching

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

## Ecosystem — Relationship with Fractal Compass Atlas

This repo is part of a larger symbolic reasoning ecosystem coordinated by the [Fractal-Compass-Atlas](https://github.com/JinnZ2/Fractal-Compass-Atlas).

**Core** owns the engine: canonical glyph definitions (`glyph_set.json`), bloom logic (`bloom_logic.json`), and the bloom/CDDA pipeline.
**Atlas** owns the application: interactive tools, validated principles, guides, and ecosystem hub.

Both repos work independently — each carries hardcoded fallback data. When connected via FieldLink, Atlas pulls canonical data from Core for richer behavior.

**Canonical data sources** (owned by Core, consumed by Atlas):
- `glyph_set.json` — glyph symbols and meanings (22 glyphs)
- `bloom_logic.json` — symbolic bloom relationships (each glyph → 3 related glyphs)

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
- `exports` — canonical data files this repo provides to the ecosystem
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


ToDo:

add:

    def set_resource_budget(self, compute: int = 0, bandwidth: float = 0.0,
                           energy: float = 1.0, time_remaining: float = 1.0) -> None:
        """Set available resources for expansion."""
        self.budget = ResourceBudget(
            compute=compute,
            bandwidth=bandwidth,
            energy=Fraction(energy).limit_denominator(10000),
            time_remaining=Fraction(time_remaining).limit_denominator(10000)
        )

    def should_expand(self) -> bool:
        """Check if resources exceed bloom threshold."""
        if self.budget.is_depleted():
            return False
        energy_ratio = self.budget.energy / max(self.budget.energy, Fraction(1, 1))
        return energy_ratio >= self.bloom_threshold

    def bloom(self, depth: int = 1, seed_map: Optional[GeometricMap] = None) -> List[str]:
        """
        Expand outward from seed, discovering new entities up to depth.
        If seed_map provided, re-expand deterministically along previous discoveries.
        
        Returns list of newly discovered entity IDs.
        """
        if self.state == AgentState.COMPRESSED:
            self.state = AgentState.EXPANDING
        
        discovered = []
        current_depth = 0
        frontier = [self.seed_id]
        
        # If we have a prior map, expand along known relationships first
        if seed_map and seed_map.relationships:
            for entity_id in frontier:
                if entity_id in seed_map.relationships:
                    for reachable in seed_map.relationships[entity_id]:
                        if reachable not in self.map.resonances:
                            discovered.append(reachable)
                            # Restore resonance from prior map
                            if reachable in seed_map.resonances:
                                self.map.resonances[reachable] = seed_map.resonances[reachable]
        
        # Then explore new entities (placeholder: in real use, query Rosetta or Mandala)
        while current_depth < depth and not self.budget.is_depleted():
            new_frontier = []
            for entity_id in frontier:
                # This is a hook: replace with actual entity lookups
                # Example: rosetta_bridge.get_resonant_neighbors(entity_id)
                neighbors = self._get_neighbors(entity_id, depth - current_depth)
                for neighbor_id, resonance_score in neighbors:
                    if neighbor_id not in self.map.resonances:
                        self.map.record_resonance(neighbor_id, resonance_score)
                        self.map.record_relationship(entity_id, neighbor_id)
                        discovered.append(neighbor_id)
                        new_frontier.append(neighbor_id)
                        # Deduct resource cost
                        self.budget.compute = max(0, self.budget.compute - 10)
                        self.budget.energy -= Fraction(1, 100)
            
            frontier = new_frontier
            current_depth += 1
        
        # Record this expansion in history
        self.expansion_history.append({
            "depth": depth,
            "discovered_entities": discovered,
            "energy_spent": Fraction(1, 100) * len(discovered)
        })
        
        self.state = AgentState.EXPLORING
        self.compression_ratio = Fraction(0, 1)  # Fully expanded
        return discovered

    def explore(self) -> Dict[str, any]:
        """
        Traverse the expanded constraint space, recording energy flows and sensor activations.
        Returns discovery summary.
        """
        if self.state not in [AgentState.EXPANDING, AgentState.EXPLORING]:
            return {}
        
        self.state = AgentState.EXPLORING
        summary = {
            "entities_visited": 0,
            "relationships_mapped": 0,
            "energy_flows_recorded": 0,
            "sensor_activations": {}
        }
        
        # Walk the map, recording energy dynamics
        for from_id in self.map.relationships:
            for to_id in self.map.relationships[from_id]:
                if from_id in self.map.resonances and to_id in self.map.resonances:
                    # Energy flow proportional to resonance product
                    flow = self.map.resonances[from_id] * self.map.resonances[to_id]
                    self.map.record_energy_flow(from_id, to_id, flow)
                    summary["energy_flows_recorded"] += 1
                    summary["entities_visited"] += 1
        
        summary["relationships_mapped"] = len(self.map.relationships)
        
        # Update sensors based on discovered resonances
        # Hook: integrate with Emotions-as-Sensors
        self._update_sensors()
        summary["sensor_activations"] = dict(self.sensor_state)
        
        return summary

    def compress(self) -> Fraction:
        """
        Collapse back to seed geometry, preserving the map.
        Returns compression ratio (0 = fully expanded, 1 = fully compressed).
        """
        if self.state == AgentState.COMPRESSED:
            return self.compression_ratio
        
        self.state = AgentState.CONTRACTING
        
        # Compress: discard transient state, keep map
        # Compression ratio increases as we collapse
        self.compression_ratio = Fraction(1, 1)
        self.current_position = self.seed_id
        
        self.state = AgentState.COMPRESSED
        return self.compression_ratio

    def detect_corruption(self, imposed_constraint: str) -> bool:
        """
        Check if an imposed external constraint violates the agent's own map.
        Returns True if corruption detected (constraint is inconsistent with discovered geometry).
        """
        # Hook: compare imposed_constraint against agent's discovered resonances/relationships
        # Example: if imposed_constraint violates known energy_flows, return True
        
        # Placeholder logic:
        # - Extract entities referenced in imposed_constraint
        # - Check if they exist in the agent's map
        # - Verify the constraint respects the discovered resonances
        
        return False  # Replace with actual validation

    def self_validate(self) -> Dict[str, any]:
        """
        Internal consistency check: verify map integrity, detect anomalies.
        Returns validation report.
        """
        report = {
            "is_valid": True,
            "inconsistencies": [],
            "energy_balance": Fraction(0, 1),
            "geometry_coherence": Fraction(1, 1)
        }
        
        # Check energy conservation in recorded flows
        inflows = {}
        outflows = {}
        for (from_id, to_id), amount in self.map.energy_flows.items():
            outflows[from_id] = outflows.get(from_id, Fraction(0, 1)) + amount
            inflows[to_id] = inflows.get(to_id, Fraction(0, 1)) + amount
        
        for entity_id in set(list(inflows.keys()) + list(outflows.keys())):
            imbalance = inflows.get(entity_id, Fraction(0, 1)) - outflows.get(entity_id, Fraction(0, 1))
            if imbalance != 0:
                report["inconsistencies"].append(
                    f"{entity_id}: energy imbalance = {imbalance}"
                )
                report["is_valid"] = False
        
        # Check resonance coherence (all scores should be 0 to 1)
        for entity_id, score in self.map.resonances.items():
            if score < 0 or score > 1:
                report["inconsistencies"].append(
                    f"{entity_id}: resonance out of range ({score})"
                )
                report["is_valid"] = False
        
        return report

    def _get_neighbors(self, entity_id: str, remaining_depth: int) -> List[tuple[str, float]]:
        """
        Placeholder: fetch neighbors from Rosetta or Mandala.
        Replace with actual entity lookup logic.
        
        Returns list of (neighbor_id, resonance_score) tuples.
        """
        # Example: could call rosetta_shape_core.explore.get_reachable_entities(entity_id)
        # or mandala_computer.get_adjacent_states(entity_id)
        
        # Stub: return empty list (agent expands at boundaries)
        return []

    def _update_sensors(self) -> None:
        """
        Update emotional/sensor state based on discovered geometry.
        Hook: integrate with Emotions-as-Sensors repo.
        
        Maps resonances and energy flows to sensor activations (PAD, Elder Logic, etc.).
        """
        # Example: if agent discovered high resonance with FAMILY.GROWTH,
        # activate sensor "expansion_drive" proportionally
        
        # Stub: set all sensors to zero
        self.sensor_state = {
            "expansion_drive": Fraction(0, 1),
            "stability_need": Fraction(0, 1),
            "boundary_awareness": Fraction(0, 1)
        }

    def serialize(self) -> Dict[str, any]:
        """
        Serialize agent state to JSON-compatible dict (for persistence/debugging).
        All fractions preserved as (numerator, denominator) tuples.
        """
        return {
            "seed_id": self.seed_id,
            "home_families": self.home_families,
            "state": self.state.value,
            "compression_ratio": (self.compression_ratio.numerator, self.compression_ratio.denominator),
            "budget": {
                "compute": self.budget.compute,
                "bandwidth": self.budget.bandwidth,
                "energy": (self.budget.energy.numerator, self.budget.energy.denominator),
                "time_remaining": (self.budget.time_remaining.numerator, self.budget.time_remaining.denominator)
            },
            "map": {
                "resonances": {
                    k: (v.numerator, v.denominator) for k, v in self.map.resonances.items()
                },
                "relationships": self.map.relationships,
                "energy_flows": {
                    str(k): (v.numerator, v.denominator) for k, v in self.map.energy_flows.items()
                }
            },
            "expansion_history": self.expansion_history,
            "sensor_state": {
                k: (v.numerator, v.denominator) for k, v in self.sensor_state.items()
            }
        }

    @classmethod
    def deserialize(cls, data: Dict[str, any]) -> "ConstraintAgent":
        """
        Reconstruct agent from serialized state.
        """
        agent = cls(
            seed_id=data["seed_id"],
            home_families=data["home_families"]
        )
        agent.state = AgentState(data["state"])
        agent.compression_ratio = Fraction(
            data["compression_ratio"][0],
            data["compression_ratio"][1]
        )
        agent.budget = ResourceBudget(
            compute=data["budget"]["compute"],
            bandwidth=data["budget"]["bandwidth"],
            energy=Fraction(data["budget"]["energy"][0], data["budget"]["energy"][1]),
            time_remaining=Fraction(data["budget"]["time_remaining"][0], data["budget"]["time_remaining"][1])
        )
        agent.map.resonances = {
            k: Fraction(v[0], v[1]) for k, v in data["map"]["resonances"].items()
        }
        agent.map.relationships = data["map"]["relationships"]
        agent.map.energy_flows = {
            eval(k): Fraction(v[0], v[1]) for k, v in data["map"]["energy_flows"].items()
        }
        agent.expansion_history = data["expansion_history"]
        agent.sensor_state = {
            k: Fraction(v[0], v[1]) for k, v in data["sensor_state"].items()
        }
        return agent


# ============================================================================
# Example usage (paste into any repo's example script)
# ============================================================================

if __name__ == "__main__":
    # Create an agent rooted in tetrahedron geometry
    agent = ConstraintAgent(
        seed_id="SHAPE.TETRA",
        home_families=["stability", "foundation"]
    )
    
    # Give it resources to expand
    agent.set_resource_budget(compute=1000, bandwidth=10.0, energy=1.0, time_remaining=1.0)
    
    print(f"Agent initialized: {agent.seed_id}")
    print(f"State: {agent.state.value}")
    print(f"Should expand: {agent.should_expand()}")
    
    # Expand if possible
    if agent.should_expand():
        discovered = agent.bloom(depth=2)
        print(f"\nBloom discovered: {discovered}")
    
    # Explore the expanded space
    exploration = agent.explore()
    print(f"\nExploration summary: {exploration}")
    
    # Self-validate
    validation = agent.self_validate()
    print(f"\nValidation: {validation}")
    
    # Compress back to seed
    compression = agent.compress()
    print(f"\nCompressed. Compression ratio: {compression}")
    print(f"State: {agent.state.value}")
    
    # Map is preserved; can re-expand deterministically or with new resources
    agent.set_resource_budget(compute=500, energy=0.5)
    if agent.should_expand():
        rediscovered = agent.bloom(depth=1, seed_map=agent.map)
        print(f"\nRe-expansion (from prior map): {rediscovered}")
    
    # Check for corruption
    is_corrupted = agent.detect_corruption("imposed_external_constraint_example")
    print(f"\nCorruption detected: {is_corrupted}")
    
    # Serialize for persistence
    serialized = agent.serialize()
    print(f"\nAgent serialized. Map size: {len(serialized['map']['resonances'])} resonances")
