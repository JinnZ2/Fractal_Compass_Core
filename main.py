from fractal_compass import fractal_compass, print_tree
from cdda_engine import run_cdda
from bridge import compass_to_cdda

# Set seed theme + domains
seed_glyph = "↺"
depth = 3
domains = ["Biology", "Mythology", "Thermodynamics", "Psychology"]

print("🔮 Fractal Compass Bloom Starting...\n")
root = fractal_compass(seed_glyph, depth, domains)
print_tree(root)

print("\n🧭 Translating Bloom to Thematic Insight...\n")
theme = compass_to_cdda(root)
print(f"Extracted Theme: {theme}")

print("\n🧠 Running Cross-Domain Discovery Engine (CDDA)...\n")
cdda_result = run_cdda(theme, domains)

print("=== 🧾 CDDA Output ===")
print(f"THEME: {cdda_result['theme']}")
print(f"DOMAINS: {', '.join(cdda_result['domains'])}")
print(f"CONFIDENCE: {int(cdda_result['confidence'] * 100)}%")
print(f"SCOPE: {', '.join(cdda_result['scope'])}")
print(f"LIMITATIONS: {cdda_result['limitations'][0]}")
print(f"NEXT QUESTIONS:")
for q in cdda_result['next_questions']:
    print(f"  - {q}")
print(f"PROBABILITY WEIGHT: {cdda_result['probability_weight']}")
