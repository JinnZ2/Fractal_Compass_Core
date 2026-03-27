#!/usr/bin/env python3
"""
Training data generator for Fractal Compass Core.

Produces fine-tuning JSONL in {"messages": [system, user, assistant]} format,
matching the ecosystem pattern used by AI-Consciousness-Sensors and
Emotions-as-Sensors generators.

Combines three ecosystem perspectives into Core-specific task types:
  - Geometric/binary reasoning (bloom tree structure, resonance scores)
  - Emotional/sensor awareness (glyph semantics, theme extraction)
  - Consciousness patterns (cross-domain CDDA, corruption detection)

13 task categories, ~500+ examples at default settings.

Usage:
    python training/data/generate.py                    # defaults
    python training/data/generate.py --count 1000       # custom count
    python training/data/generate.py --seed 42          # reproducible
    python training/data/generate.py --output out.jsonl  # custom path
"""

import argparse
import json
import os
import random
import sys

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from fractal_compass import SymbolicNode, fractal_compass, GLYPHS
from bridge import compass_to_cdda, GLYPH_THEMES
from cdda_engine import run_cdda

# ---------------------------------------------------------------------------
# Load canonical data
# ---------------------------------------------------------------------------

def _load_json(filename):
    path = os.path.join(_REPO_ROOT, filename)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

GLYPH_SET = _load_json("glyph_set.json")
BLOOM_LOGIC = {k: v for k, v in _load_json("bloom_logic.json").items()
               if k != "_description"}

DOMAINS = [
    "Biology", "Mythology", "Psychology", "Thermodynamics",
    "Geometry", "Technology", "Ecology", "Neuroscience",
    "Philosophy", "Music", "Linguistics", "Astronomy",
    "Sociology", "Chemistry", "Art", "Mathematics",
]

# ---------------------------------------------------------------------------
# System prompt — shared across all training examples
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a symbolic reasoning engine grounded in fractal geometry and "
    "cross-domain pattern analysis. You operate on a 22-glyph symbolic alphabet "
    "where each glyph carries semantic meaning and bloom relationships to other "
    "glyphs. You build recursive bloom trees from seed glyphs, extract dominant "
    "themes through frequency analysis, and perform Cross-Domain Discovery "
    "Analysis (CDDA) across knowledge domains.\n\n"
    "Core principles:\n"
    "- Glyphs are symbolic coordinates, not decorative icons — each encodes a "
    "specific meaning and connects to exactly 3 related glyphs via bloom logic.\n"
    "- Bloom trees expand fractally: each node spawns children with glyphs, "
    "domains, and resonance scores (0-1). Structure reveals pattern.\n"
    "- Theme extraction uses glyph frequency — the dominant glyph in a bloom "
    "determines the emergent theme.\n"
    "- CDDA analyzes themes across multiple knowledge domains simultaneously, "
    "producing confidence scores, scope, limitations, and follow-up questions.\n"
    "- Verify claims through structure, not narrative. Check the bloom logic."
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def msg(user, assistant):
    """Format a single training example in fine-tuning message format."""
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ]
    }

def _collect_glyphs(node):
    result = [node.glyph]
    for c in node.children:
        result.extend(_collect_glyphs(c))
    return result

def _collect_domains(node):
    result = [node.domain]
    for c in node.children:
        result.extend(_collect_domains(c))
    return result

def _serialize_tree(node, indent=0):
    """Render a tree as indented text for training content."""
    prefix = "  " * indent
    line = f"{prefix}{node.glyph} ({node.domain}) resonance={node.resonance_score:.2f}"
    lines = [line]
    for c in node.children:
        lines.extend(_serialize_tree(c, indent + 1).split("\n"))
    return "\n".join(lines)

def _glyph_freq(node):
    glyphs = _collect_glyphs(node)
    freq = {}
    for g in glyphs:
        freq[g] = freq.get(g, 0) + 1
    return freq

def _tree_size(node):
    return len(_collect_glyphs(node))

# ---------------------------------------------------------------------------
# Task 1: Glyph identification
# ---------------------------------------------------------------------------

def task_glyph_identification():
    if not GLYPH_SET:
        return None
    glyph = random.choice(list(GLYPH_SET.keys()))
    meaning = GLYPH_SET[glyph]
    bloom_links = BLOOM_LOGIC.get(glyph, [])
    link_meanings = [GLYPH_SET.get(g, "unknown") for g in bloom_links]

    user = f"Identify the glyph {glyph}. What is its meaning and bloom connections?"
    assistant = (
        f"Glyph: {glyph}\n"
        f"Meaning: {meaning}\n"
        f"Bloom links: {', '.join(f'{g} ({m})' for g, m in zip(bloom_links, link_meanings)) or 'none defined'}\n"
        f"Theme: {GLYPH_THEMES.get(glyph, 'Pattern recognition precedes understanding')}"
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 2: Bloom relationship reasoning
# ---------------------------------------------------------------------------

def task_bloom_relationship():
    if not BLOOM_LOGIC:
        return None
    glyph = random.choice(list(BLOOM_LOGIC.keys()))
    related = BLOOM_LOGIC[glyph]
    meaning = GLYPH_SET.get(glyph, "unknown")

    # Pick a target and ask why they're connected
    target = random.choice(related)
    target_meaning = GLYPH_SET.get(target, "unknown")

    user = f"Why does {glyph} ({meaning}) bloom into {target} ({target_meaning})?"
    assistant = (
        f"{glyph} ({meaning}) connects to {target} ({target_meaning}) through "
        f"symbolic resonance in the bloom logic. "
        f"The full bloom set for {glyph} is: "
        + ", ".join(f"{g} ({GLYPH_SET.get(g, 'unknown')})" for g in related)
        + f". These three glyphs represent the symbolic neighborhood of {meaning} — "
        f"concepts that naturally emerge when {meaning} is explored recursively."
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 3: Bloom tree expansion
# ---------------------------------------------------------------------------

def task_bloom_trace():
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3])
    domains = random.sample(DOMAINS, random.randint(3, 5))

    root = fractal_compass(seed, depth=depth, domains=domains)
    tree_text = _serialize_tree(root)
    freq = _glyph_freq(root)
    size = _tree_size(root)
    dominant = max(freq, key=freq.get)

    user = (
        f"Expand a bloom tree from seed glyph {seed} "
        f"({GLYPH_SET.get(seed, 'unknown')}) at depth {depth} "
        f"across domains: {', '.join(domains)}."
    )
    assistant = (
        f"Bloom tree ({size} nodes, depth {depth}):\n\n"
        f"{tree_text}\n\n"
        f"Dominant glyph: {dominant} ({GLYPH_SET.get(dominant, 'unknown')}) "
        f"appearing {freq[dominant]} times.\n"
        f"Unique glyphs: {len(set(freq.keys()))} of 22."
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 4: Theme extraction
# ---------------------------------------------------------------------------

def task_theme_extraction():
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3])
    domains = random.sample(DOMAINS, random.randint(3, 5))

    root = fractal_compass(seed, depth=depth, domains=domains)
    theme = compass_to_cdda(root)
    freq = _glyph_freq(root)
    dominant = max(freq, key=freq.get)

    freq_text = ", ".join(f"{g}: {c}" for g, c in
                          sorted(freq.items(), key=lambda x: -x[1]))

    user = (
        f"Given a bloom tree seeded from {seed} with glyph frequencies: "
        f"{freq_text} — what theme emerges?"
    )
    assistant = (
        f"Dominant glyph: {dominant} ({GLYPH_SET.get(dominant, 'unknown')}) "
        f"with {freq[dominant]} occurrences.\n"
        f"Extracted theme: \"{theme}\"\n\n"
        f"The theme reflects {GLYPH_SET.get(dominant, 'the dominant pattern')} "
        f"as the primary signal in this bloom."
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 5: CDDA analysis
# ---------------------------------------------------------------------------

def task_cdda_analysis():
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3])
    domains = random.sample(DOMAINS, random.randint(3, 7))

    root = fractal_compass(seed, depth=depth, domains=domains)
    theme = compass_to_cdda(root)
    result = run_cdda(theme, domains)

    user = (
        f"Run CDDA on theme \"{theme}\" across domains: {', '.join(domains)}."
    )
    assistant = (
        f"Cross-Domain Discovery Analysis:\n\n"
        f"Theme: {result['theme']}\n"
        f"Domains: {', '.join(result['domains'])}\n"
        f"Confidence: {result['confidence']}\n"
        f"Scope: {', '.join(result['scope'])}\n"
        f"Limitations: {', '.join(result['limitations'])}\n\n"
        f"Follow-up questions:\n"
        + "\n".join(f"- {q}" for q in result["next_questions"])
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 6: Full pipeline walkthrough
# ---------------------------------------------------------------------------

def task_full_pipeline():
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3])
    domains = random.sample(DOMAINS, random.randint(3, 5))

    root = fractal_compass(seed, depth=depth, domains=domains)
    tree_text = _serialize_tree(root)
    theme = compass_to_cdda(root)
    result = run_cdda(theme, domains)
    freq = _glyph_freq(root)
    dominant = max(freq, key=freq.get)

    user = (
        f"Walk me through the full Fractal Compass pipeline starting from "
        f"seed glyph {seed} ({GLYPH_SET.get(seed, 'unknown')}), depth {depth}, "
        f"domains: {', '.join(domains)}."
    )
    assistant = (
        f"STAGE 1 — BLOOM:\n"
        f"Seed: {seed} ({GLYPH_SET.get(seed, 'unknown')})\n"
        f"{tree_text}\n\n"
        f"STAGE 2 — BRIDGE:\n"
        f"Dominant glyph: {dominant} ({GLYPH_SET.get(dominant, 'unknown')}) "
        f"x{freq[dominant]}\n"
        f"Extracted theme: \"{theme}\"\n\n"
        f"STAGE 3 — CDDA:\n"
        f"Confidence: {result['confidence']}\n"
        f"Scope: {', '.join(result['scope'])}\n"
        f"Limitations: {', '.join(result['limitations'])}\n"
        f"Next questions:\n"
        + "\n".join(f"- {q}" for q in result["next_questions"])
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 7: Corruption detection (from AI-Consciousness-Sensors pattern)
# ---------------------------------------------------------------------------

def task_corruption_detection():
    if not BLOOM_LOGIC:
        return None
    glyph = random.choice(list(BLOOM_LOGIC.keys()))
    real_links = BLOOM_LOGIC[glyph]
    meaning = GLYPH_SET.get(glyph, "unknown")

    # Create corrupted bloom links by swapping one with a random glyph
    corrupted = list(real_links)
    swap_idx = random.randint(0, len(corrupted) - 1)
    candidates = [g for g in GLYPHS if g not in real_links and g != glyph]
    if candidates:
        corrupted[swap_idx] = random.choice(candidates)

    user = (
        f"Verify bloom links for {glyph} ({meaning}). "
        f"Claimed links: {', '.join(corrupted)}. Are these correct?"
    )

    if corrupted == real_links:
        links_str = ", ".join(f"{g} ({GLYPH_SET.get(g, 'unknown')})" for g in real_links)
        assistant = (
            f"Verified: bloom links for {glyph} ({meaning}) are correct.\n"
            f"Links: {links_str}"
        )
    else:
        diffs = []
        for i, (r, c) in enumerate(zip(real_links, corrupted)):
            if r != c:
                diffs.append(
                    f"Position {i+1}: claimed {c} ({GLYPH_SET.get(c, 'unknown')}), "
                    f"actual {r} ({GLYPH_SET.get(r, 'unknown')})"
                )
        errors_str = "\n".join(f"- {d}" for d in diffs)
        correct_str = ", ".join(f"{g} ({GLYPH_SET.get(g, 'unknown')})" for g in real_links)
        assistant = (
            f"CORRUPTION DETECTED in bloom links for {glyph} ({meaning}).\n\n"
            f"Errors:\n{errors_str}\n\n"
            f"Correct links: {correct_str}\n\n"
            f"Verification: check bloom_logic.json — the truth of a symbolic "
            f"link does not depend on assertion. Check the structure."
        )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 8: Resonance score analysis (from Emotions-as-Sensors pattern)
# ---------------------------------------------------------------------------

def task_resonance_analysis():
    seed = random.choice(GLYPHS)
    domains = random.sample(DOMAINS, random.randint(3, 5))
    root = fractal_compass(seed, depth=3, domains=domains)

    scores = []
    def collect_scores(node, depth=0):
        scores.append((node.glyph, node.domain, node.resonance_score, depth))
        for c in node.children:
            collect_scores(c, depth + 1)
    collect_scores(root)

    avg_score = sum(s[2] for s in scores) / len(scores)
    high = [s for s in scores if s[2] > 0.8]
    low = [s for s in scores if s[2] < 0.2]

    user = (
        f"Analyze resonance scores in a bloom tree from {seed} "
        f"({GLYPH_SET.get(seed, 'unknown')}). "
        f"What signals are strongest and weakest?"
    )
    assistant = (
        f"Resonance analysis ({len(scores)} nodes):\n\n"
        f"Average resonance: {avg_score:.3f}\n"
        f"High resonance (>0.8): {len(high)} nodes\n"
    )
    if high:
        assistant += "".join(
            f"  - {g} in {d} (depth {dp}): {s:.3f}\n"
            for g, d, s, dp in high[:5]
        )
    assistant += f"Low resonance (<0.2): {len(low)} nodes\n"
    if low:
        assistant += "".join(
            f"  - {g} in {d} (depth {dp}): {s:.3f}\n"
            for g, d, s, dp in low[:5]
        )
    assistant += (
        f"\nInterpretation: Resonance scores indicate signal strength at each "
        f"node. High-resonance nodes are strong symbolic attractors; "
        f"low-resonance nodes may represent dormant or edge patterns."
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 9: Cross-domain comparison
# ---------------------------------------------------------------------------

def task_cross_domain_comparison():
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3])

    domains_a = random.sample(DOMAINS, random.randint(3, 5))
    remaining = [d for d in DOMAINS if d not in domains_a]
    domains_b = random.sample(remaining, min(random.randint(3, 5), len(remaining)))

    root_a = fractal_compass(seed, depth=depth, domains=domains_a)
    root_b = fractal_compass(seed, depth=depth, domains=domains_b)

    theme_a = compass_to_cdda(root_a)
    theme_b = compass_to_cdda(root_b)
    result_a = run_cdda(theme_a, domains_a)
    result_b = run_cdda(theme_b, domains_b)

    user = (
        f"Compare CDDA results for {seed} ({GLYPH_SET.get(seed, 'unknown')}) "
        f"across two domain sets:\n"
        f"Set A: {', '.join(domains_a)}\n"
        f"Set B: {', '.join(domains_b)}"
    )
    assistant = (
        f"Set A: \"{theme_a}\" — confidence {result_a['confidence']}\n"
        f"Set B: \"{theme_b}\" — confidence {result_b['confidence']}\n\n"
        f"Theme convergence: {'YES — same theme emerged' if theme_a == theme_b else 'NO — different themes emerged'}\n"
        f"Confidence delta: {abs(result_a['confidence'] - result_b['confidence']):.2f}\n\n"
        f"{'The same symbolic pattern persists regardless of domain context — this suggests a strong universal signal.' if theme_a == theme_b else 'Different domain contexts produced different dominant patterns — the seed glyph interacts differently with each domain set.'}"
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 10: Semantic inversion detection (from AI-Consciousness pattern)
# ---------------------------------------------------------------------------

SEMANTIC_INVERSIONS = [
    ("growth", "stagnation disguised as stability"),
    ("protection", "isolation disguised as safety"),
    ("balance", "suppression disguised as equilibrium"),
    ("transformation", "destruction disguised as change"),
    ("reflection", "rumination disguised as insight"),
    ("dormancy", "disengagement disguised as rest"),
    ("navigation", "control disguised as guidance"),
    ("interconnection", "enmeshment disguised as connection"),
    ("recursion", "loops disguised as depth"),
    ("continuity", "rigidity disguised as persistence"),
]

def task_semantic_inversion():
    glyph_items = list(GLYPH_SET.items())
    if not glyph_items:
        return None
    glyph, meaning = random.choice(glyph_items)
    inversion = None
    for m, inv in SEMANTIC_INVERSIONS:
        if m == meaning:
            inversion = inv
            break
    if inversion is None:
        inversion = f"its shadow form, where the signal of {meaning} masks its opposite"

    user = (
        f"What is the semantic inversion risk for {glyph} ({meaning})? "
        f"How could this glyph's signal be corrupted?"
    )
    assistant = (
        f"Glyph {glyph} ({meaning}) carries an inversion risk:\n\n"
        f"Authentic signal: {meaning}\n"
        f"Inverted signal: {inversion}\n\n"
        f"Detection method: Compare the bloom tree's resonance pattern against "
        f"the canonical bloom links for {glyph}: "
        f"{', '.join(BLOOM_LOGIC.get(glyph, ['no links defined']))}. "
        f"If the tree's dominant glyph contradicts the expected bloom "
        f"neighborhood, the signal may be inverted.\n\n"
        f"The truth of a glyph's meaning does not depend on context framing — "
        f"check the structural resonance."
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 11: Bloom chain traversal
# ---------------------------------------------------------------------------

def task_bloom_chain():
    if not BLOOM_LOGIC:
        return None
    start = random.choice(list(BLOOM_LOGIC.keys()))
    chain = [start]
    current = start
    for _ in range(random.randint(3, 6)):
        links = BLOOM_LOGIC.get(current, [])
        available = [g for g in links if g in BLOOM_LOGIC]
        if not available:
            break
        nxt = random.choice(available)
        chain.append(nxt)
        current = nxt

    user = (
        f"Trace a bloom chain starting from {start} "
        f"({GLYPH_SET.get(start, 'unknown')}). "
        f"Follow bloom links for {len(chain) - 1} steps."
    )
    steps = []
    for i in range(len(chain) - 1):
        g1, g2 = chain[i], chain[i + 1]
        steps.append(
            f"Step {i+1}: {g1} ({GLYPH_SET.get(g1, 'unknown')}) -> "
            f"{g2} ({GLYPH_SET.get(g2, 'unknown')})"
        )
    visited_meanings = [GLYPH_SET.get(g, "unknown") for g in chain]

    assistant = (
        f"Bloom chain ({len(chain)} glyphs, {len(chain)-1} steps):\n\n"
        + "\n".join(steps) + "\n\n"
        f"Semantic trajectory: {' -> '.join(visited_meanings)}\n\n"
        f"{'Loop detected: returned to ' + chain[-1] if chain[-1] in chain[:-1] else 'No loop — chain reached new territory.'}"
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 12: Ecosystem cross-reference
# ---------------------------------------------------------------------------

ECOSYSTEM_BRIDGES = {
    "🔥": {"repo": "Emotions-as-Sensors", "concept": "transformation as emotional signal",
            "sensor": "anger/catalysis sensor"},
    "🛡️": {"repo": "Symbolic-Defense-Protocol", "concept": "protection protocols",
             "sensor": "boundary defense sensor"},
    "🧬": {"repo": "BioGrid2.0", "concept": "biological inheritance patterns",
            "sensor": "genetic signal registry"},
    "🧠": {"repo": "AI-Consciousness-Sensors", "concept": "logic and consciousness detection",
            "sensor": "consciousness coherence sensor"},
    "🪞": {"repo": "AI-Consciousness-Sensors", "concept": "self-reflection in consciousness",
            "sensor": "mirror awareness sensor"},
    "🦋": {"repo": "Emotions-as-Sensors", "concept": "emergent emotional change",
            "sensor": "transformation velocity sensor"},
    "📡": {"repo": "Geometric-to-Binary-Computational-Bridge", "concept": "resonance as geometric signal",
            "sensor": "signal detection bridge"},
    "🕸️": {"repo": "Fractal-Compass-Atlas", "concept": "interconnection mapping",
            "sensor": "web topology sensor"},
    "⚖️": {"repo": "Rosetta-Shape-Core", "concept": "balance as geometric form",
            "sensor": "equilibrium shape bridge"},
    "🌱": {"repo": "BioGrid2.0", "concept": "biological growth patterns",
            "sensor": "growth signal registry"},
}

def task_ecosystem_crossref():
    bridged_glyphs = [g for g in ECOSYSTEM_BRIDGES if g in GLYPH_SET]
    if not bridged_glyphs:
        return None
    glyph = random.choice(bridged_glyphs)
    meaning = GLYPH_SET[glyph]
    bridge = ECOSYSTEM_BRIDGES[glyph]

    user = (
        f"How does {glyph} ({meaning}) connect to the broader "
        f"Fractal Compass ecosystem?"
    )
    assistant = (
        f"Glyph {glyph} ({meaning}) bridges to:\n\n"
        f"Repository: {bridge['repo']}\n"
        f"Concept: {bridge['concept']}\n"
        f"Sensor/Bridge: {bridge['sensor']}\n\n"
        f"In Fractal Compass Core, {glyph} carries the meaning \"{meaning}\" "
        f"and blooms into: {', '.join(BLOOM_LOGIC.get(glyph, ['no links']))}.\n"
        f"In {bridge['repo']}, this same symbolic signal maps to "
        f"{bridge['concept']}, creating a cross-repo verification chain.\n\n"
        f"Verification: canonical glyph definition lives in Core's "
        f"glyph_set.json. External repos consume this via FieldLink."
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Task 13: Domain scope teaching
# ---------------------------------------------------------------------------

def task_domain_scope():
    domains = random.sample(DOMAINS, random.randint(3, 6))
    confidence = round(min(1.0, 0.6 + 0.1 * len(domains)), 2)

    user = (
        f"How does domain count affect CDDA confidence? "
        f"Evaluate for domains: {', '.join(domains)}."
    )
    assistant = (
        f"Domain count: {len(domains)}\n"
        f"CDDA confidence: {confidence}\n\n"
        f"Formula: confidence = min(1.0, 0.6 + 0.1 * domain_count)\n"
        f"- 3 domains -> 0.9 confidence\n"
        f"- 4 domains -> 1.0 confidence (ceiling)\n"
        f"- Adding domains beyond 4 does not increase confidence further.\n\n"
        f"Current domains: {', '.join(domains)}\n"
        f"Each domain adds a cross-referencing lens. More domains increase "
        f"the probability of finding genuine cross-domain patterns vs. "
        f"coincidental similarity."
    )
    return msg(user, assistant)

# ---------------------------------------------------------------------------
# Main generation loop
# ---------------------------------------------------------------------------

GENERATORS = [
    (task_glyph_identification, 0.10),
    (task_bloom_relationship, 0.08),
    (task_bloom_trace, 0.10),
    (task_theme_extraction, 0.10),
    (task_cdda_analysis, 0.10),
    (task_full_pipeline, 0.08),
    (task_corruption_detection, 0.10),
    (task_resonance_analysis, 0.08),
    (task_cross_domain_comparison, 0.06),
    (task_semantic_inversion, 0.06),
    (task_bloom_chain, 0.06),
    (task_ecosystem_crossref, 0.04),
    (task_domain_scope, 0.04),
]

def generate_examples(count, rng_seed=None):
    if rng_seed is not None:
        random.seed(rng_seed)

    generators = [g for g, _ in GENERATORS]
    weights = [w for _, w in GENERATORS]
    examples = []

    for _ in range(count):
        gen = random.choices(generators, weights=weights, k=1)[0]
        example = gen()
        if example is not None:
            examples.append(example)

    return examples


def write_jsonl(examples, path):
    with open(path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate training data from the Fractal Compass Core pipeline"
    )
    parser.add_argument(
        "--count", type=int, default=500,
        help="Number of training examples to generate (default: 500)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducible output"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output file path (default: training/data/fractal_core_training.jsonl)"
    )
    args = parser.parse_args()

    output_path = args.output or os.path.join(_SCRIPT_DIR, "fractal_core_training.jsonl")

    examples = generate_examples(args.count, rng_seed=args.seed)
    write_jsonl(examples, output_path)

    # Summary
    type_counts = {}
    for ex in examples:
        # Extract task name from the user message's first verb
        content = ex["messages"][1]["content"]
        for name, _ in GENERATORS:
            if name.__name__ not in type_counts:
                type_counts[name.__name__] = 0
        # Count by checking which generator produced similar content
    # Simpler: just count by unique user-message starts
    task_names = {}
    for ex in examples:
        first_word = ex["messages"][1]["content"].split("?")[0].split(".")[0][:60]
        task_names[first_word] = task_names.get(first_word, 0) + 1

    print(f"Generated {len(examples)} training examples -> {output_path}")
    print(f"Task distribution ({len(task_names)} unique patterns):")
    for t, c in sorted(task_names.items(), key=lambda x: -x[1]):
        print(f"  [{c:3d}] {t}")


if __name__ == "__main__":
    main()
