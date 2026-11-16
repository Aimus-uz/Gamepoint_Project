# usage: python build_css.py <output.css> <skillsInfo.json | source dir>...
import json
import os
import re
import sys

HEX = re.compile(r'^#[0-9a-fA-F]{6}$')
QUOTED = re.compile(r'["\'](#[0-9a-fA-F]{6})["\']')
EXTRA = ['#ffffff', '#00ffff', '#008000', '#ffff00', '#ff0000', '#00ff00']

FONTS = {
    'stratum': 'Stratum2',
    'light': 'Stratum2 Light',
    'cond': 'Stratum2 Condensed',
    'boldcond': 'Stratum2 Bold Condensed',
    'mono': 'Stratum2 Mono',
    'noto': 'Noto Sans',
    'serif': 'Noto Serif',
    'notomono': 'Noto Mono',
}
SIZES = {
    '.js-info': 12,
    '.js-name': 28,
    '.js-seg': 15,
    '.js-card-name': 17,
    '.js-card-info': 14,
    '.js-menu-title': 20,
    '.js-menu-info': 13,
    '.js-row-text': 15,
    '.js-fseg': 11,
}

BASE = '''/* GAMEPOINT skin: design-system tokens (Нейтральный / Синий / Розовый / Красный). The font stays Stratum2. */
@define panel-bg: #12151cf0;
@define line: #303641;
@define raised: #20252e;
@define text: #f6f7f9;
@define muted: #aeb4bf;
@define faint: #858d9b;
@define soft: #ced2d9;
@define accent: #009bed;
@define accent-bg: #0d2232;
@define danger: #ef4444;

.js-root,
.js-scope
{
	width: 100%;
	height: 100%;
}

.js-off
{
	visibility: collapse;
}

/* ---------- skill card ---------- */

.js-skill
{
	horizontal-align: center;
	vertical-align: bottom;
	margin-bottom: 16px;
	width: 380px;
	height: fit-children;
	flow-children: down;
	background-color: panel-bg;
	border: 1px solid line;
	/* the skill colour comes from the generated .js-skill.sc-* rules below */
	border-left: 4px solid line;
	border-radius: 8px;
	box-shadow: #00000099 0px 8px 24px 0px;
}

.js-scope.is-spec .js-skill,
.js-scope.is-spec .js-menu
{
	margin-bottom: 86px;
}

.js-scope.is-spec.is-other .js-skill
{
	visibility: collapse;
}

.js-body
{
	width: 100%;
	height: fit-children;
	padding: 12px 16px 14px 16px;
	flow-children: down;
}

/* "Your skill" / "Drawing a skill": Badge S (capsule) */
.js-info
{
	horizontal-align: left;
	margin-bottom: 4px;
	padding: 3px 8px 2px 8px;
	border-radius: 10px;
	background-color: raised;
	font-family: Stratum2, "Arial Unicode MS";
	font-weight: bold;
	font-size: 12px;
	letter-spacing: 1px;
	text-transform: uppercase;
	color: muted;
}

.js-name
{
	horizontal-align: left;
	text-align: left;
	width: 100%;
	font-family: Stratum2, "Arial Unicode MS";
	font-weight: bold;
	font-size: 28px;
	color: text;
	white-space: nowrap;
	text-overflow: ellipsis;
}

.js-desc,
.js-status
{
	horizontal-align: left;
	width: fit-children;
	max-width: 100%;
	height: fit-children;
	margin-top: 2px;
	flow-children: right-wrap;
}

.js-desc
{
	max-height: 66px;
}

.js-seg
{
	max-width: 340px;
	text-align: left;
	font-family: Stratum2, "Arial Unicode MS";
	font-size: 15px;
	color: muted;
}

.js-status .js-seg
{
	font-weight: bold;
	color: text;
}

.js-skill.no-info .js-info,
.js-skill.no-desc .js-desc,
.js-skill.no-status .js-status
{
	visibility: collapse;
}

/* cooldown: brand gradient on a dark track */
.js-track
{
	width: 100%;
	height: 4px;
	background-color: raised;
	border-radius: 0px 0px 6px 0px;
	visibility: collapse;
}

.js-skill.has-cd .js-track
{
	visibility: visible;
}

.js-cd
{
	horizontal-align: left;
	width: 0%;
	height: 100%;
	background-color: gradient( linear, 0% 0%, 100% 0%, from( #009bed ), to( #f3009a ) );
	visibility: collapse;
}

.js-skill.has-cd .js-cd
{
	visibility: visible;
}

/* ---------- effects on you (left column) ---------- */

.js-side
{
	horizontal-align: left;
	vertical-align: top;
	margin-left: 12px;
	margin-top: 452px;
	width: 380px;
	height: fit-children;
	flow-children: down;
}

.js-card
{
	width: fit-children;
	max-width: 380px;
	height: fit-children;
	margin-bottom: 8px;
	padding: 8px 12px 8px 12px;
	flow-children: right;
	background-color: panel-bg;
	border: 1px solid line;
	border-left: 3px solid danger;
	border-radius: 6px;
}

.js-card-name
{
	vertical-align: middle;
	font-family: Stratum2, "Arial Unicode MS";
	font-weight: bold;
	font-size: 17px;
	color: text;
	white-space: nowrap;
	text-overflow: ellipsis;
}

.js-card-info
{
	vertical-align: middle;
	max-width: 250px;
	margin-left: 8px;
	font-family: Stratum2, "Arial Unicode MS";
	font-size: 14px;
	color: muted;
}

.js-card.no-info .js-card-info
{
	visibility: collapse;
}

/* ---------- WASD menu ---------- */

.js-menu
{
	horizontal-align: center;
	vertical-align: bottom;
	margin-bottom: 16px;
	width: 380px;
	height: fit-children;
	padding: 12px 0px 10px 0px;
	flow-children: down;
	background-color: panel-bg;
	border: 1px solid line;
	border-radius: 8px;
	box-shadow: #00000099 0px 8px 24px 0px;
}

.js-menu-title
{
	width: 100%;
	padding: 0px 16px;
	font-family: Stratum2, "Arial Unicode MS";
	font-weight: bold;
	font-size: 20px;
	color: text;
	white-space: nowrap;
	text-overflow: ellipsis;
}

.js-menu-info
{
	width: 100%;
	margin-top: 2px;
	padding: 0px 16px;
	font-family: Stratum2, "Arial Unicode MS";
	font-size: 13px;
	color: muted;
}

.js-menu.no-info .js-menu-info
{
	visibility: collapse;
}

.js-div
{
	width: 100%;
	height: 1px;
	margin: 10px 0px 4px 0px;
	background-color: raised;
}

.js-row
{
	width: 100%;
	height: 32px;
	flow-children: right;
}

.js-row-bar
{
	width: 3px;
	height: 100%;
}

.js-row-text
{
	vertical-align: middle;
	width: fill-parent-flow( 1.0 );
	margin-left: 13px;
	margin-right: 13px;
	font-family: Stratum2, "Arial Unicode MS";
	font-size: 15px;
	color: soft;
	white-space: nowrap;
	text-overflow: ellipsis;
}

.js-row.is-sel
{
	background-color: accent-bg;
}

.js-row.is-sel .js-row-bar
{
	background-color: accent;
}

.js-row.is-sel .js-row-text
{
	font-weight: bold;
	color: #ffffff;
}

/* footer: js-mf0 "W/S - scroll", js-mf1 "·", js-mf2 "E - select", js-mf3 "· 2/3" */
.js-menu-foot
{
	horizontal-align: center;
	width: fit-children;
	height: fit-children;
	margin-top: 10px;
	flow-children: right;
}

.js-fseg
{
	vertical-align: middle;
	margin: 0px 3px;
	font-family: Stratum2, "Arial Unicode MS";
	font-weight: bold;
	font-size: 11px;
	letter-spacing: 1px;
	text-transform: uppercase;
	color: faint;
}

#js-mf0,
#js-mf2
{
	padding: 3px 8px 2px 8px;
	border-radius: 10px;
	background-color: raised;
	color: muted;
}

#js-mf1
{
	visibility: collapse;
}
'''


def colors(paths):
    found = set(EXTRA)
    for path in paths:
        if os.path.isdir(path):
            for folder, _, files in os.walk(path):
                for name in files:
                    if name.endswith(('.cs', '.json')):
                        for line in open(os.path.join(folder, name), encoding='utf-8-sig', errors='ignore'):
                            if 'class SkillConfig' not in line:
                                found.update(c.lower() for c in QUOTED.findall(line))
            continue
        for skill in json.load(open(path, encoding='utf-8-sig')):
            color = str(skill.get('Color', '')).strip()
            if HEX.match(color):
                found.add(color.lower())
    return sorted(found)


def build(found):
    out = [BASE]
    for name, family in FONTS.items():
        selectors = ',\n'.join(f'.js-scope.ff-{name} {element}' for element in SIZES)
        out.append(f'{selectors}\n{{\n\tfont-family: {family}, "Arial Unicode MS";\n}}\n')
    for size in range(80, 135, 5):
        if size == 100:
            continue
        for element, base in SIZES.items():
            out.append(f'.js-scope.fs-{size} {element}\n{{\n\tfont-size: {round(base * size / 100)}px;\n}}\n')
    for color in found:
        cls = 'sc-' + color[1:]
        out.append(f'.js-skill.{cls} .js-name,\n.js-seg.{cls},\n.js-card.{cls} .js-card-name,\n.js-menu.{cls} .js-menu-title,\n.js-row.{cls} .js-row-text\n{{\n\tcolor: {color};\n}}\n')
        # GAMEPOINT: the strip on the left of the skill card takes the skill colour
        out.append(f'.js-skill.{cls}\n{{\n\tborder-left: 4px solid {color};\n}}\n')
    for pct in range(101):
        out.append(f'.js-skill.cd-{pct} .js-cd\n{{\n\twidth: {pct}%;\n}}\n')
    # HUD position (jRandomSkills 1.2.4.b8+: PanoramaHud.yOffset / ySpecOffset / xOffset), same rules as upstream.
    # They come after BASE, so they win over its margin-bottom; with an older plugin they are never set and
    # BASE (16px, is-spec 86px) stays in charge.
    for y in range(0, 51):
        out.append(f'.yOffset-{y} {{ margin-bottom: {y}%; }}\n')
    for x in range(-100, 101):
        out.append(f'.xOffset-{x} {{ margin-left: {x}%; }}\n')
    return '\n'.join(out)


output, sources = sys.argv[1], sys.argv[2:]
found = colors(sources)
open(output, 'w', encoding='utf-8', newline='\n').write(build(found))
print(output, len(found), 'colors')
