# jRandomSkills — Panorama HUD GAMEPOINT

Здесь только **клиентский HUD**. Сам плагин [Juzlus/jRandomSkills](https://github.com/Juzlus/jRandomSkills) (GPL-3.0)
не изменён: исходники, конфиги и переводы лежат в том виде, что в оригинале (коммит `d953628`), и нужны только
генератору стилей как список цветов навыков. DLL отсюда не собирается — на сервере остаётся оригинальный плагин.

## Наше
- `VPK Addon/Content/panorama/layout/custom_game/gamepoint/jrs_hud.xml` — разметка на основе `simple_skills.xml`
  (id те же, добавлены только декоративные панели `js-track`, `js-div`).
- `VPK Addon/tools/build_css.py` — база стилей `BASE` в цветах дизайн-системы и правило полосы цветом навыка.
- `VPK Addon/Content/panorama/styles/custom_game/gamepoint/jrs_hud.css` — сгенерирован (CI, job `jrandomskills-hud`).

## Включить на сервере (только конфиг, `configs/config.json` плагина)
```json
"HtmlHudCustomisation": { ... "HeaderLineSize": "sm", ... },
"PanoramaHud": {
  "Enabled": true,
  "Layout": "panorama/layout/custom_game/gamepoint/jrs_hud.xml",
  "Font": "stratum",
  "FontSize": 100
}
```
`HeaderLineSize` — штатная настройка плагина; без неё не показывается бейдж «Ваш текущий навык».
