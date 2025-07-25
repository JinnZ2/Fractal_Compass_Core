from fractal_compass import fractal_compass
from cdda_engine import run_cdda
from bridge import compass_to_cdda

# Seed + domain test
theme = "Inversion is required before transformation"
domains = ["Biology", "Mythology", "Thermodynamics", "Psychology"]

print(" Running Fractal Compass...")
root = fractal_compass("↺", depth=3, domains=domains)

print("\n Translating to CDDA theme...")
generated_theme = compass_to_cdda(root)

print("\n Running CDDA Inference...")
result = run_cdda(generated_theme, domains)

print("\n=== Result ===")
print(result)
