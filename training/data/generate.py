#!/usr/bin/env python3
"""
Training data generator for Fractal Compass Core.

Produces structured JSONL training examples from the symbolic reasoning pipeline:
  1. Glyph relationships — bloom logic pairs and semantic meanings
  2. Bloom trees — full fractal expansion traces with resonance scores
  3. Theme extraction — glyph-frequency-to-theme mappings
  4. CDDA analysis — cross-domain reasoning examples

Each example is a self-contained dict with an "example_type" field.

Usage:
    python training/data/generate.py                    # defaults: 200 examples
    python training/data/generate.py --count 500        # custom count
    python training/data/generate.py --seed 42          # reproducible output
    python training/data/generate.py --output out.jsonl  # custom output path
"""

import argparse
import json
import os
import random
import sys

# ---------------------------------------------------------------------------
# Path setup — import Core modules from repo root
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from fractal_compass import SymbolicNode, fractal_compass, GLYPHS
from bridge import compass_to_cdda, GLYPH_THEMES
from cdda_engine import run_cdda

# ---------------------------------------------------------------------------
# Load canonical data files
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

# Domains drawn from across the ecosystem
DOMAINS = [
    "Biology", "Mythology", "Psychology", "Thermodynamics",
    "Geometry", "Technology", "Ecology", "Neuroscience",
    "Philosophy", "Music", "Linguistics", "Astronomy",
    "Sociology", "Chemistry", "Art", "Mathematics",
]

# ---------------------------------------------------------------------------
# Generator: Glyph relationship examples
# ---------------------------------------------------------------------------

def generate_glyph_relationship():
    """Produce a training example from bloom_logic symbolic links."""
    if not BLOOM_LOGIC:
        return None
    glyph = random.choice(list(BLOOM_LOGIC.keys()))
    related = BLOOM_LOGIC[glyph]
    meaning = GLYPH_SET.get(glyph, "unknown")
    related_meanings = [GLYPH_SET.get(r, "unknown") for r in related]

    return {
        "example_type": "glyph_relationship",
        "input": {
            "glyph": glyph,
            "meaning": meaning,
        },
        "output": {
            "related_glyphs": related,
            "related_meanings": related_meanings,
            "relationship_description": (
                f"{glyph} ({meaning}) blooms into "
                + ", ".join(f"{g} ({m})" for g, m in zip(related, related_meanings))
            ),
        },
    }

# ---------------------------------------------------------------------------
# Generator: Bloom tree trace
# ---------------------------------------------------------------------------

def _serialize_tree(node):
    """Recursively convert a SymbolicNode tree to a dict."""
    return {
        "glyph": node.glyph,
        "domain": node.domain,
        "resonance_score": round(node.resonance_score, 4),
        "children": [_serialize_tree(c) for c in node.children],
    }

def _collect_glyphs(node):
    """Flatten all glyphs from a tree."""
    result = [node.glyph]
    for c in node.children:
        result.extend(_collect_glyphs(c))
    return result

def _collect_domains(node):
    """Flatten all domains from a tree."""
    result = [node.domain]
    for c in node.children:
        result.extend(_collect_domains(c))
    return result

def _tree_depth(node):
    if not node.children:
        return 0
    return 1 + max(_tree_depth(c) for c in node.children)

def generate_bloom_trace():
    """Produce a full bloom tree expansion as a training example."""
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3, 4])
    n_domains = random.randint(3, 6)
    domains = random.sample(DOMAINS, min(n_domains, len(DOMAINS)))

    root = fractal_compass(seed, depth=depth, domains=domains)
    all_glyphs = _collect_glyphs(root)
    all_domains = _collect_domains(root)

    glyph_freq = {}
    for g in all_glyphs:
        glyph_freq[g] = glyph_freq.get(g, 0) + 1

    domain_freq = {}
    for d in all_domains:
        domain_freq[d] = domain_freq.get(d, 0) + 1

    return {
        "example_type": "bloom_trace",
        "input": {
            "seed_glyph": seed,
            "seed_meaning": GLYPH_SET.get(seed, "unknown"),
            "depth": depth,
            "domains": domains,
        },
        "output": {
            "tree": _serialize_tree(root),
            "total_nodes": len(all_glyphs),
            "unique_glyphs": len(set(all_glyphs)),
            "glyph_frequency": glyph_freq,
            "domain_distribution": domain_freq,
            "actual_depth": _tree_depth(root),
        },
    }

# ---------------------------------------------------------------------------
# Generator: Theme extraction examples
# ---------------------------------------------------------------------------

def generate_theme_extraction():
    """Produce a glyph-frequency -> theme mapping training example."""
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3])
    domains = random.sample(DOMAINS, random.randint(3, 5))

    root = fractal_compass(seed, depth=depth, domains=domains)
    theme = compass_to_cdda(root)
    all_glyphs = _collect_glyphs(root)

    glyph_freq = {}
    for g in all_glyphs:
        glyph_freq[g] = glyph_freq.get(g, 0) + 1
    dominant = max(glyph_freq, key=glyph_freq.get)

    return {
        "example_type": "theme_extraction",
        "input": {
            "seed_glyph": seed,
            "glyph_frequency": glyph_freq,
            "dominant_glyph": dominant,
            "dominant_meaning": GLYPH_SET.get(dominant, "unknown"),
        },
        "output": {
            "theme": theme,
            "dominant_count": glyph_freq[dominant],
            "total_nodes": len(all_glyphs),
        },
    }

# ---------------------------------------------------------------------------
# Generator: Full CDDA pipeline examples
# ---------------------------------------------------------------------------

def generate_cdda_analysis():
    """Produce a full pipeline example: seed -> bloom -> theme -> CDDA."""
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3, 4])
    n_domains = random.randint(3, 7)
    domains = random.sample(DOMAINS, min(n_domains, len(DOMAINS)))

    root = fractal_compass(seed, depth=depth, domains=domains)
    theme = compass_to_cdda(root)
    analysis = run_cdda(theme, domains)

    return {
        "example_type": "cdda_analysis",
        "input": {
            "seed_glyph": seed,
            "seed_meaning": GLYPH_SET.get(seed, "unknown"),
            "depth": depth,
            "domains": domains,
            "theme": theme,
        },
        "output": analysis,
    }

# ---------------------------------------------------------------------------
# Generator: Glyph meaning examples (simple pair data)
# ---------------------------------------------------------------------------

def generate_glyph_meaning():
    """Produce a glyph <-> meaning training pair."""
    if not GLYPH_SET:
        return None
    glyph = random.choice(list(GLYPH_SET.keys()))
    meaning = GLYPH_SET[glyph]
    theme = GLYPH_THEMES.get(glyph, "Pattern recognition precedes understanding")
    bloom_links = BLOOM_LOGIC.get(glyph, [])

    return {
        "example_type": "glyph_meaning",
        "input": {
            "glyph": glyph,
        },
        "output": {
            "meaning": meaning,
            "theme": theme,
            "bloom_links": bloom_links,
            "bloom_link_meanings": [GLYPH_SET.get(g, "unknown") for g in bloom_links],
        },
    }

# ---------------------------------------------------------------------------
# Generator: Cross-domain resonance pairs
# ---------------------------------------------------------------------------

def generate_cross_domain_pair():
    """Produce a pair of bloom analyses across different domain sets for comparison."""
    seed = random.choice(GLYPHS)
    depth = random.choice([2, 3])

    domains_a = random.sample(DOMAINS, random.randint(3, 5))
    remaining = [d for d in DOMAINS if d not in domains_a]
    domains_b = random.sample(remaining, min(random.randint(3, 5), len(remaining)))

    root_a = fractal_compass(seed, depth=depth, domains=domains_a)
    root_b = fractal_compass(seed, depth=depth, domains=domains_b)

    theme_a = compass_to_cdda(root_a)
    theme_b = compass_to_cdda(root_b)

    analysis_a = run_cdda(theme_a, domains_a)
    analysis_b = run_cdda(theme_b, domains_b)

    return {
        "example_type": "cross_domain_pair",
        "input": {
            "seed_glyph": seed,
            "seed_meaning": GLYPH_SET.get(seed, "unknown"),
            "depth": depth,
        },
        "output": {
            "analysis_a": {
                "domains": domains_a,
                "theme": theme_a,
                "confidence": analysis_a["confidence"],
            },
            "analysis_b": {
                "domains": domains_b,
                "theme": theme_b,
                "confidence": analysis_b["confidence"],
            },
            "same_theme": theme_a == theme_b,
        },
    }

# ---------------------------------------------------------------------------
# Main generation loop
# ---------------------------------------------------------------------------

GENERATORS = [
    (generate_glyph_meaning, 0.15),
    (generate_glyph_relationship, 0.15),
    (generate_bloom_trace, 0.20),
    (generate_theme_extraction, 0.20),
    (generate_cdda_analysis, 0.20),
    (generate_cross_domain_pair, 0.10),
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


def main():
    parser = argparse.ArgumentParser(
        description="Generate training data from the Fractal Compass Core pipeline"
    )
    parser.add_argument(
        "--count", type=int, default=200,
        help="Number of training examples to generate (default: 200)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducible output"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output file path (default: training/data/fractal_compass_training.jsonl)"
    )
    args = parser.parse_args()

    output_path = args.output or os.path.join(_SCRIPT_DIR, "fractal_compass_training.jsonl")

    examples = generate_examples(args.count, rng_seed=args.seed)

    with open(output_path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    # Summary stats
    type_counts = {}
    for ex in examples:
        t = ex["example_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"Generated {len(examples)} training examples -> {output_path}")
    print("Breakdown by type:")
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
