# PMM_WeaponSkins — сборка GAMEPOINT

Форк [RRimmer/PMM_WeaponSkins](https://github.com/RRimmer/PMM_WeaponSkins) (GPL-3.0), коммит `7acef5f`,
перекрашенный под дизайн-систему GAMEPOINT. Шрифт не менялся (Stratum2 из CS2).

## Что изменено
- `tools/pmm_ws.base.css` — нейтральные цвета и статусы переведены на токены:
  Текст/Основной `#F6F7F9`, Текст/Вторичный `#AEB4BF`, Фон/Поверхность `#12151C`, Фон/Приподнятый `#181C24`,
  Граница/Обычная `#303641`, Статус/Успех `#22C55E`, Статус/Ошибка `#EF4444`, VIP/GCOIN `#FBBF24`.
- Бейджи — капсулы по Badge: S 20 px / M 24 px / L 28 px (команда на герое — L, «Надето» — M,
  редкость в шапке скина — M, слот наклейки и счётчики вкладок — S).
- `tools/gen_layout.py` — в палитру добавлены `gp-ct #009BED`, `gp-t #F59E0B`, `gp-pink`, `gp-violet`, `gp-cyan`;
  фон меню: Поверхность → Сторона·фон (`#0D2232` для CT, `#2E200D` для T). Переключатели берут цвет стороны.
- Тема по умолчанию (`Plugin.Theme.cs`, конфиг): CT = `gp-ct`, T = `gp-t`.
- Не тронуто: цвета редкости и износа (стандарт CS2).

## После правки стилей
`pmm_ws.css` и `Layout.g.cs` генерируются — правьте `tools/pmm_ws.base.css` / `tools/gen_layout.py`, затем:

```
python3 tools/gen_layout.py PMM_WeaponSkins
```

CI (`.github/workflows/build-plugins.yml`, job `pmm-weaponskins`) делает это сам и выкладывает архив
`Server-plugins/` + `Content-addonmanager/`. Клиентский аддон всё равно нужно пересобрать в CS2 Workshop Tools.
