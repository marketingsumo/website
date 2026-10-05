"""The Marketing Lab cover generator: renders an HTML template in the house style to a 1600x900 image."""
import html, json, sys, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
Y = "#F2B705"      # brand yellow
YD = "#E3A600"     # darker yellow for small text
INK = "#151515"

ICONS = {
 "search": '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5 21 21"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.6c3 .1 5.5 2 5.5 5"/>',
 "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2.8h6V4"/><path d="m8.5 13 2.5 2.5 4.5-5"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/><path d="M15 9l5-5M17 4h3v3"/>',
 "chart": '<path d="M4 20h16"/><rect x="5.5" y="11" width="3" height="7"/><rect x="10.5" y="7" width="3" height="11"/><rect x="15.5" y="3.5" width="3" height="14.5"/>',
 "scale": '<path d="M12 3v18M7 21h10M5 7h14"/><path d="M5 7l-3 6a3 3 0 0 0 6 0z"/><path d="M19 7l-3 6a3 3 0 0 0 6 0z"/>',
 "receipt": '<path d="M6 2.5h12v19l-2-1.4-2 1.4-2-1.4-2 1.4-2-1.4-2 1.4z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
 "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="m9 15 2 2 4-4"/>',
}

def icon(name, size=44):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{Y}" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')

CHECK = (f'<svg width="30" height="30" viewBox="0 0 30 30"><rect x="3" y="5" width="20" height="20" rx="2" fill="none" '
         f'stroke="{Y}" stroke-width="2.6"/><path d="M8 15l5 5 12-15" fill="none" stroke="{Y}" stroke-width="3.2" '
         f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

FLASK = (f'<svg width="62" height="72" viewBox="0 0 62 72"><circle cx="34" cy="7" r="3" fill="none" stroke="{Y}" stroke-width="2.4"/>'
         f'<circle cx="42" cy="3" r="2" fill="none" stroke="{Y}" stroke-width="2"/>'
         f'<path d="M22 14h18M25 14v18L8 62c-1.6 3 .5 6 4 6h38c3.5 0 5.6-3 4-6L37 32V14" fill="none" stroke="{INK}" stroke-width="4.2" stroke-linejoin="round"/>'
         f'<path d="M15 50h32l6 11c.8 1.7-.2 3-2 3H11c-1.8 0-2.8-1.3-2-3z" fill="{Y}"/>'
         f'<circle cx="27" cy="44" r="2.4" fill="{Y}"/><circle cx="33" cy="39" r="1.6" fill="{Y}"/></svg>')

def underline(width, color=Y, sw=5):
    return (f'<svg width="{width}" height="18" viewBox="0 0 {width} 18" preserveAspectRatio="none">'
            f'<path d="M4 11 C {width*.25:.0f} 5, {width*.6:.0f} 14, {width-4} 6" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round"/></svg>')

ARROW_RIGHT = (f'<svg width="74" height="34" viewBox="0 0 74 34"><path d="M3 20 C 22 15, 44 19, 66 16" fill="none" '
               f'stroke="{Y}" stroke-width="4" stroke-linecap="round"/><path d="M54 6 L68 16 L55 27" fill="none" '
               f'stroke="{Y}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def doodle_arrow(w, h, path, head):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="{path}" fill="none" stroke="{INK}" '
            f'stroke-width="3.2" stroke-linecap="round"/><path d="{head}" fill="none" stroke="{INK}" stroke-width="3.2" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

BUBBLE = (f'<svg width="330" height="210" viewBox="0 0 330 210"><path d="M165 12 C 255 10, 318 48, 316 98 '
          f'C 314 146, 262 176, 196 180 C 210 196, 236 202, 250 203 C 214 206, 182 196, 164 182 '
          f'C 82 182, 16 148, 14 98 C 12 46, 76 14, 165 12 Z" fill="#FBF8F2" stroke="{INK}" stroke-width="3.4" '
          f'stroke-linejoin="round"/></svg>')

SPARK = (f'<svg width="70" height="60" viewBox="0 0 70 60"><path d="M10 40 L22 52 M30 30 L36 48 M50 26 L48 44" '
         f'stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/></svg>')
SPARK_Y = (f'<svg width="60" height="50" viewBox="0 0 60 50"><path d="M8 34 L18 44 M26 24 L30 40 M44 18 L42 34" '
           f'stroke="{Y}" stroke-width="3.4" stroke-linecap="round"/></svg>')
STAR = (f'<svg width="46" height="46" viewBox="0 0 24 24"><path d="M12 2.8l2.7 6 6.5.6-4.9 4.3 1.5 6.4L12 16.8 6.2 20.1 7.7 13.7 '
        f'2.8 9.4l6.5-.6z" fill="none" stroke="{Y}" stroke-width="1.6" stroke-linejoin="round"/></svg>')

# Centre illustrations, drawn as line doodles with yellow accents
ILLUSTRATIONS = {
 "profile": f'''<svg width="430" height="380" viewBox="0 0 430 380">
  <g transform="rotate(-4 200 190)">
   <rect x="40" y="40" width="300" height="290" rx="16" fill="#FFFDF8" stroke="{INK}" stroke-width="4"/>
   <circle cx="110" cy="115" r="38" fill="{Y}" stroke="{INK}" stroke-width="4"/>
   <circle cx="110" cy="103" r="13" fill="#FFFDF8" stroke="{INK}" stroke-width="3.5"/>
   <path d="M86 140c5-14 14-20 24-20s19 6 24 20" fill="#FFFDF8" stroke="{INK}" stroke-width="3.5"/>
   <path d="M170 98h130M170 124h96" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
   <path d="M76 190h220M76 222h190M76 254h205M76 286h140" stroke="#BDB6AA" stroke-width="6" stroke-linecap="round"/>
   <path d="M66 186l10 10 18-20" fill="none" stroke="{Y}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" transform="translate(-36 4)"/>
  </g>
  <g transform="rotate(-18 330 250)">
   <circle cx="320" cy="235" r="62" fill="rgba(242,183,5,.18)" stroke="{INK}" stroke-width="9"/>
   <path d="M366 282 L414 332" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>
   <path d="M290 212 c10-12 26-16 40-12" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  </g></svg>''',
 "pricetag": f'''<svg width="430" height="380" viewBox="0 0 430 380">
  <g transform="rotate(-8 215 190)">
   <path d="M120 70 H300 a14 14 0 0 1 14 14 V300 a14 14 0 0 1 -14 14 H120 a14 14 0 0 1 -14 -14 V84 a14 14 0 0 1 14 -14 Z" fill="#FFFDF8" stroke="{INK}" stroke-width="4"/>
   <rect x="134" y="96" width="152" height="62" rx="8" fill="{Y}" stroke="{INK}" stroke-width="3.5"/>
   <text x="276" y="140" text-anchor="end" font-family="Courier Prime" font-weight="700" font-size="36" fill="{INK}">S$ ?</text>
   {''.join(f'<rect x="{134+c*54}" y="{180+r*42}" width="40" height="30" rx="6" fill="{"#FFFDF8" if (r,c)!=(2,2) else Y}" stroke="{INK}" stroke-width="3.2"/>' for r in range(3) for c in range(3))}
  </g>
  <g transform="rotate(14 330 120)">
   <path d="M300 60 L380 60 L400 100 L380 140 L300 140 Z" fill="{Y}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
   <circle cx="384" cy="100" r="8" fill="#FFFDF8" stroke="{INK}" stroke-width="3.5"/>
   <path d="M392 100 C 410 92, 418 70, 404 52" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>
   <text x="336" y="109" text-anchor="middle" font-family="Archivo Black" font-size="24" fill="{INK}">2026</text>
  </g></svg>''',
}

def build_html(c):
    fonts = (HERE / "fonts.css").read_text()
    head_lines = "".join(f'<div>{html.escape(l)}</div>' for l in c["headline"])
    sub = html.escape(c["sub_before"]) + f'<mark>{html.escape(c["sub_mark"])}</mark>' + html.escape(c.get("sub_after", ""))
    sub2 = html.escape(c.get("sub_line2", ""))
    feats = "".join(
        f'<div class="feat">{icon(i)}<span>{html.escape(a)}<br>{html.escape(b)}</span></div>'
        + ('<i class="div"></i>' if n < len(c["footer"]) - 1 else "")
        for n, (i, a, b) in enumerate(c["footer"]))
    checks = "".join(f'<li>{CHECK}<span>{html.escape(t)}</span></li>' for t in c["notebook_items"])
    bubble_lines = "<br>".join(html.escape(l) for l in c["bubble"])
    y_lines = "<br>".join(html.escape(l) for l in c["note_yellow"])
    p_lines = "<br>".join(html.escape(l) for l in c["note_purple"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:900px;overflow:hidden;position:relative;background:#F2EDE4;
 background-image:linear-gradient(rgba(60,50,30,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(60,50,30,.045) 1px,transparent 1px);
 background-size:34px 34px;font-family:Inter;color:{INK}}}
.abs{{position:absolute}}
.brand{{left:56px;top:38px;display:flex;align-items:center;gap:12px}}
.brand b{{font-family:'Archivo Narrow';font-weight:700;font-size:66px;letter-spacing:-1.5px;line-height:1}}
.brand sup{{font-family:'Archivo Black';color:{Y};font-size:52px;position:relative;top:-6px;margin-left:3px;vertical-align:top;line-height:1}}
.tag{{left:58px;top:146px;font-family:'Courier Prime';font-size:22px;letter-spacing:2.2px;color:{YD};line-height:1.42}}
.tagline{{left:52px;top:206px}}
.issue{{left:722px;top:48px;border:4px solid {Y};padding:6px 18px 4px;transform:rotate(-3deg);text-align:center;
 font-family:'Courier Prime';color:{Y};line-height:1}}
.issue small{{display:block;font-size:27px;letter-spacing:1px}}.issue strong{{font-size:54px;font-weight:700}}
.h1{{left:56px;top:{c.get("h1_top",238)}px;font-family:'Archivo Black';font-size:{c.get("h1_size",92)}px;line-height:1.02;letter-spacing:-1.5px;width:820px}}
.script{{left:56px;top:{c["script_top"]}px;font-family:Caveat;font-weight:700;font-size:{c.get("script_size",100)}px;color:{Y};line-height:1;letter-spacing:1px}}
.scriptline{{left:60px;top:{c["script_top"]+c.get("script_size",100)-6}px}}
.sub{{left:56px;top:{c["sub_top"]}px;display:flex;gap:18px;align-items:flex-start}}
.sub p{{font-family:'Courier Prime';font-size:25px;line-height:1.36;color:#262626;margin-top:2px}}
mark{{background:{Y};color:{INK};padding:0 4px}}
.footer{{left:0;bottom:0;width:1120px;height:150px;background:#151515;
 clip-path:polygon(0 18%,4% 22%,9% 14%,14% 20%,19% 12%,25% 19%,31% 13%,37% 21%,43% 14%,49% 20%,55% 12%,61% 19%,67% 13%,73% 21%,79% 14%,85% 22%,90% 15%,95% 24%,100% 30%,100% 100%,0 100%)}}
.feats{{left:46px;bottom:28px;display:flex;align-items:center;gap:22px}}
.feat{{display:flex;align-items:center;gap:14px;color:#EDEDED;font-size:19px;line-height:1.28;font-weight:500}}
.div{{width:1px;height:46px;background:#4a4a4a}}
.bubble{{left:{c.get("bubble_left",930)}px;top:28px}}
.bubble p{{position:absolute;left:0;top:{97-len(c["bubble"])*16}px;width:330px;text-align:center;font-family:Kalam;font-size:26px;line-height:1.22;transform:rotate(-2deg)}}
.note{{width:270px;padding:44px 26px 30px;box-shadow:0 14px 22px rgba(60,40,10,.18),0 2px 4px rgba(60,40,10,.12)}}
.note p{{font-family:Kalam;font-size:30px;line-height:1.26}}
.note::before{{content:"";position:absolute;left:50%;top:-14px;width:110px;height:34px;margin-left:-55px;background:rgba(222,210,180,.78);transform:rotate(-2deg)}}
.ny{{left:1278px;top:{c.get("ny_top",70)}px;background:#F8DD82;transform:rotate(4deg)}}
.np{{left:1236px;top:{c.get("np_top",348)}px;background:#8D6AD6;color:#fff;transform:rotate(-3deg);width:280px}}
.np p{{color:#fff}}
.illo{{left:{c.get("illo_left",820)}px;top:{c.get("illo_top",250)}px;transform:scale({c.get("illo_scale",1)});transform-origin:top left}}
.book{{left:{c.get("book_left",1060)}px;top:{c.get("book_top",540)}px;width:400px;height:380px;background:#FFFDF8;transform:rotate(5deg);border-radius:6px;
 box-shadow:0 16px 26px rgba(60,40,10,.22);padding:34px 30px 0 60px}}
.book::before{{content:"";position:absolute;left:16px;top:18px;bottom:30px;width:22px;
 background:radial-gradient(circle at 11px 11px,transparent 5px,#333 6px,#333 7.5px,transparent 8.5px) 0 0/22px 28px repeat-y}}
.book h4{{font-family:Kalam;font-weight:700;color:{YD};font-size:27px;letter-spacing:1px;margin-bottom:12px}}
.book ul{{list-style:none}}.book li{{display:flex;align-items:center;gap:12px;font-family:Kalam;font-size:27px;margin:6px 0}}
.star{{left:{c.get("star_left",1420)}px;top:{c.get("star_top",800)}px}}
.spark1{{left:{c.get("spark_left",840)}px;top:{c.get("spark_top",250)}px}}
.spark2{{left:{c.get("issue_spark_left",880)}px;top:30px}}
</style></head><body>
<div class="abs brand">{FLASK}<b>The Marketing Lab<sup>*</sup></b></div>
<div class="abs tag">IDEAS. EXPERIMENTS. BREAKDOWNS.<br>THAT MOVE THE NEEDLE.</div>
<div class="abs tagline">{underline(300, Y, 4)}</div>
<div class="abs issue"><small>ISSUE</small><strong>{html.escape(c["issue"])}</strong></div>
<div class="abs spark2">{SPARK_Y}</div>
<div class="abs h1">{head_lines}</div>
<div class="abs script">{html.escape(c["script"])}</div>
<div class="abs scriptline">{underline(c.get("script_underline", 640), Y, 5)}</div>
<div class="abs sub">{ARROW_RIGHT}<p>{sub}<br>{sub2}</p></div>
<div class="abs illo">{ILLUSTRATIONS[c["illustration"]]}</div>
<div class="abs spark1">{SPARK}</div>
<div class="abs bubble">{BUBBLE}<p>{bubble_lines}</p></div>
<div class="abs" style="left:1196px;top:186px">{doodle_arrow(80, 70, "M6 6 C 16 38, 34 52, 64 50", "M50 38 L66 50 L52 62")}</div>
<div class="abs note ny"><p>{y_lines}</p></div>
<div class="abs note np"><p>{p_lines}</p></div>
{"" if c.get("parrow_top") is None else f'<div class="abs" style="left:1150px;top:{c["parrow_top"]}px">' + doodle_arrow(90, 90, "M10 70 C 20 40, 40 26, 76 18", "M60 8 L78 18 L64 32") + "</div>"}
<div class="abs footer"></div>
<div class="abs feats">{feats}</div>
<div class="abs book"><h4>{html.escape(c["notebook_title"])}</h4><ul>{checks}</ul></div>
<div class="abs star">{STAR}</div>
</body></html>"""

def render(cfg_path, out_png):
    c = json.loads(pathlib.Path(cfg_path).read_text())
    page_html = HERE / (pathlib.Path(out_png).stem + ".html")
    page_html.write_text(build_html(c))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=2)
        pg.goto(page_html.as_uri()); pg.wait_for_timeout(400)
        pg.screenshot(path=out_png)
        b.close()

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
