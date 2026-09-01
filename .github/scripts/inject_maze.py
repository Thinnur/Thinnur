import os

def process_svg(filename, is_dark):
    if not os.path.exists(filename):
        return

    with open(filename, 'r') as f:
        svg = f.read()

    # The previous injection broke the SVG syntax because <svg> tag is not self-closing 
    # and has attributes. Doing `.replace('<svg', '<svg<style>...` results in `<svg<style>... xmlns=...>` which is invalid XML.
    
    # Correct way: insert <style> AFTER the opening <svg ...> tag closes with `>`.
    # Let's find the first occurrence of ">" after "<svg"
    svg_start = svg.find('<svg')
    if svg_start != -1:
        first_close = svg.find('>', svg_start)
        if first_close != -1:
            style_injection = """
<style>
    rect[rx="2"] {
        stroke: #ffffff;
        stroke-width: 0.5px;
    }
</style>
"""
            if not is_dark:
                style_injection = style_injection.replace('#ffffff', '#000000')
                
            # Insert right after the >
            svg = svg[:first_close+1] + style_injection + svg[first_close+1:]

    with open(filename, 'w') as f:
        f.write(svg)

process_svg('dist/github-contribution-grid-snake.svg', False)
process_svg('dist/github-contribution-grid-snake-dark.svg', True)
