import json
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Glyph-to-theme mapping (fallback when glyph_set.json unavailable)
_FALLBACK_THEMES = {
    "↺": "Inversion is required before transformation",
    "💓": "Emotion is a signal, not noise",
    "⚛️": "Structure emerges from energy resonance",
}

def _load_glyph_themes():
    """Build glyph-to-theme map from glyph_set.json meanings."""
    try:
        with open(os.path.join(_SCRIPT_DIR, "glyph_set.json"), "r") as f:
            glyph_map = json.load(f)
        return {g: f"Pattern emerges through {m}" for g, m in glyph_map.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return _FALLBACK_THEMES

GLYPH_THEMES = _load_glyph_themes()

def compass_to_cdda(root_node):
    """
    Traverses the symbolic tree and returns a theme based on dominant glyph cluster.
    """
    glyph_counts = {}

    def traverse(node):
        glyph_counts[node.glyph] = glyph_counts.get(node.glyph, 0) + 1
        for child in node.children:
            traverse(child)

    traverse(root_node)

    dominant_glyph = max(glyph_counts, key=glyph_counts.get)

    return GLYPH_THEMES.get(dominant_glyph, "Pattern recognition precedes understanding")
