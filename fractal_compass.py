import random

class SymbolicNode:
    def __init__(self, glyph, domain, parent=None, resonance_score=0.5):
        self.glyph = glyph
        self.domain = domain
        self.parent = parent
        self.children = []
        self.resonance_score = resonance_score

    def __repr__(self):
        return f"{self.glyph} ({self.domain})"

def fractal_compass(seed_glyph="↺", depth=3, domains=None):
    if domains is None:
        domains = ["Nature", "Myth", "Geometry", "Psychology", "Technology"]
    
    root = SymbolicNode(seed_glyph, domain=random.choice(domains))

    def bloom(node, current_depth):
        if current_depth == 0:
            return
        for _ in range(2):  # You can make this dynamic later
            glyph = random.choice(["↺", "🕸", "◐", "⚛️", "📖", "💓"])
            domain = random.choice(domains)
            child = SymbolicNode(glyph, domain, parent=node, resonance_score=random.random())
            node.children.append(child)
            bloom(child, current_depth - 1)

    bloom(root, depth)
    return root

def print_tree(node, indent=0):
    print(" " * indent + f"{node.glyph} ({node.domain}) - Score: {node.resonance_score:.2f}")
    for child in node.children:
        print_tree(child, indent + 2)
