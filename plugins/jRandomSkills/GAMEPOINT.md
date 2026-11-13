# jRandomSkills — сборка GAMEPOINT

Форк [Juzlus/jRandomSkills](https://github.com/Juzlus/jRandomSkills) (GPL-3.0), коммит `d953628`,
с Panorama HUD в стиле дизайн-системы GAMEPOINT. Шрифт не менялся (Stratum2).

## Что изменено
- **HUD** — `VPK Addon/Content/panorama/layout/custom_game/gamepoint/jrs_hud.xml` (разметка на основе
  `simple_skills.xml`, все id плагина те же) и `VPK Addon/tools/build_css.py` (стили, база `BASE`):
  поверхность `#12151C`, рамка `#303641`, полоса слева цветом навыка, бейдж «Ваш текущий навык»,
  перезарядка градиентом `#009BED → #F3009A`, меню с выделением `#0D2232` / `#009BED`, эффекты слева с полосой `#EF4444`.
  Путь `custom_game/gamepoint/…` выбран, чтобы не конфликтовать с аддоном автора (`3833386255`).
- **Розыгрыш навыка в начале раунда** — `PanoramaHud.ShowSkill` ставит класс `is-draw`: синяя полоса, синий бейдж
  «Получение навыка» и бегущий индикатор.
- **Конфиг** (`config.json` и значения по умолчанию в `Config.cs`): `PanoramaHud.Enabled = true`, `Layout` → наш HUD,
  `HeaderLineSize = "sm"` (без него бейдж «Ваш текущий навык» не показывается), цвета HTML-HUD — токены дизайн-системы.

## Сборка
CI (`.github/workflows/build-plugins.yml`, job `jrandomskills`) генерирует `jrs_hud.css`, собирает плагин и выкладывает
`Server-plugins/` + `Content-addonmanager/`. Если поменяли цвета навыков в `skillsInfo.json` — CSS нужно пересобрать.

В репозитории нет `packages/GeoLite2-Country.mmdb` (9 МБ) — он уже есть на сервере из оригинальной установки.
