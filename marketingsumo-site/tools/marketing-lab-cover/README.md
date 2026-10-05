# The Marketing Lab cover generator

Renders blog covers in the Marketing Lab house style (cream grid paper, "ISSUE 0XX" stamp,
black headline + yellow handwritten line, sticky notes, playbook notebook, torn dark footer)
to a 1600x900 image. Text is real type, so it never comes out garbled.

## Make a new cover

1. Copy `issues/issue011.json` to `issues/issue012.json` and edit the text:
   `issue`, `headline` (2 lines), `script` (the yellow handwritten line), `sub_*` (the arrow line;
   `sub_mark` is highlighted), `bubble`, `note_yellow`, `note_purple`, `notebook_title`,
   `notebook_items` (4), `footer` (4 x [icon, line 1, line 2]) and `illustration`
   (`profile` or `pricetag`; add more in `ILLUSTRATIONS` in make_cover.py).
   Icons: search, users, clipboard, target, chart, scale, receipt, calendar.
2. Render (needs Python with Playwright: `pip install playwright && playwright install chromium`):

       cd tools/marketing-lab-cover
       python make_cover.py issues/issue012.json issue012.png

3. Check the PNG for overlaps (long headlines may need a smaller `h1_size` or moving
   `illo_left`), then save it as a JPEG in `static/images/` and set `image:` on the post.

Fonts (Archivo Black, Archivo Narrow, Caveat, Courier Prime, Kalam, Inter) are from Google Fonts, SIL Open Font License.
