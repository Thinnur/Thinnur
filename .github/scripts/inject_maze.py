import urllib.request
import re
import sys
import os

def process_svg(filename, is_dark):
    if not os.path.exists(filename):
        print(f"Skipping {filename}, not found.")
        return

    with open(filename, 'r') as f:
        svg = f.read()

    # Empty cells in Platane/snk have fill="#ebedf0" (light) or fill="#161b22" (dark)
    # We want to add a thin stroke around EVERY cell to create a "maze" effect.
    # Platane/snk cells usually have a class like 'class="ContributionCalendar-day"'
    
    # Alternatively, just inject a style block to add stroke to all rects that have rx="2"
    style_injection = """
<style>
    rect[rx="2"] {
        stroke: #ffffff;
        stroke-width: 0.5px;
    }
</style>
"""
    if is_dark:
        style_injection = style_injection.replace('#ffffff', '#ffffff') # White maze lines for dark mode
    else:
        style_injection = style_injection.replace('#ffffff', '#000000') # Black maze lines for light mode
        
    svg = svg.replace('<svg', '<svg' + style_injection, 1)

    with open(filename, 'w') as f:
        f.write(svg)

process_svg('dist/github-contribution-grid-snake.svg', False)
process_svg('dist/github-contribution-grid-snake-dark.svg', True)
print("Injected maze lines into SVGs.")
