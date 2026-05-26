"""Scan all templates for old badge patterns."""
import glob, re, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
files = sorted(glob.glob("templates/*.html"))

print("=== 1. Inline background styles ===")
for f in files:
    content = open(f, encoding="utf-8").read()
    for m in re.finditer(r'style="[^"]*background[^"]*"', content):
        print(f"  {f}: {m.group()[:100]}")

print("\n=== 2. Old Bootstrap badge classes ===")
for f in files:
    content = open(f, encoding="utf-8").read()
    for cls in ["bg-success", "bg-warning", "bg-danger", "bg-secondary", "bg-primary", "bg-info"]:
        if f'class="badge {cls}' in content or f'class="badge bg-{cls}' in content:
            print(f"  {f}: badge {cls} found")

print("\n=== 3. Old light/hext background colors ===")
old_colors = ["#E3F0FF", "#FFF3E0", "#F3E5F5", "#FFFDE7", "#E8F5E9", "#F7F9FD", "#EEF2F9"]
for f in files:
    content = open(f, encoding="utf-8").read()
    for color in old_colors:
        if color in content:
            print(f"  {f}: old color {color} found")

print("\n=== 4. status-* CSS classes (new pattern audit) ===")
new_classes = ["s-avaliacao", "s-execucao", "s-validacao", "s-envio", "s-concluido", "s-atraso"]
for f in files:
    content = open(f, encoding="utf-8").read()
    for cls in new_classes:
        if cls in content:
            print(f"  {f}: uses new class {cls}")

print("\n=== 5. badge-status with inline style (should be replaced) ===")
for f in files:
    content = open(f, encoding="utf-8").read()
    for m in re.finditer(r'<span class="badge-status"[^>]*style="[^"]*"[^>]*>', content):
        print(f"  {f}: {m.group()[:120]}")

print("\nDone.")
