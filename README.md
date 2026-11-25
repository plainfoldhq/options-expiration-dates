# Options expiration dates 2000-2050 (CSV): monthly opex, quad witching, VIX, IMM dates

Free CSV of US equity options expiration dates and related dates for every month from 2000 to 2050, with NYSE holidays applied:

- **Monthly options last trading day**: the third Friday of the month, or the NYSE business day before it when that Friday is a market holiday (for example Good Friday 2025: Thursday April 17; Juneteenth 2026: Thursday June 18). Quarterly months (March, June, September, December) are flagged: the "quad witching" days.
- **VIX settlement dates**: the Wednesday 30 days before the third Friday of the following month; if that Friday is a holiday, 30 days before the business day preceding it; if the result is a holiday, the business day before (for example the settlement in June 2024: Tuesday June 18, because June 19 was Juneteenth). VIX futures and standard monthly VIX options; weekly VIX options are not included. From 2005 (early-year dates follow today's rule and were not checked against Cboe notices).
- **IMM dates**: the third Wednesday of March, June, September and December (not holiday-adjusted).

Browse the dates by year on the reference site: [options expiration dates 2026-2028](https://plainfoldhq.github.io/options-expiration-dates/) and [quad witching dates 2025-2035](https://plainfoldhq.github.io/quad-witching-dates/).

## File

`data/expirations_2000_2050.csv` (1,368 rows):

| column | example | notes |
|---|---|---|
| type | monthly_options_last_trading_day | or `vix_settlement`, `imm_date` |
| contract_month | 2026-06 | for `vix_settlement`, the month in which settlement occurs; Cboe names that contract by the following month (2024-06-18 settles the July 2024 contract) |
| date | 2026-06-18 | the date after holiday adjustment |
| weekday | Thu | |
| rule_date | 2026-06-19 | the date before holiday adjustment |
| holiday_adjusted | 1 | 1 = moved because of an NYSE holiday |
| is_quarterly | 1 | 1 for monthly rows in March, June, September, December (quad witching) and for all IMM rows; always 0 for VIX rows |

```python
import csv
rows = [r for r in csv.DictReader(open("data/expirations_2000_2050.csv"))
        if r["type"] == "monthly_options_last_trading_day" and r["date"].startswith("2027")]
[r["date"] for r in rows if r["is_quarterly"] == "1"]  # 2027 quad witching days
```

```python
import pandas as pd
url = "https://raw.githubusercontent.com/plainfoldhq/options-expiration-dates/main/data/expirations_2000_2050.csv"
pd.read_csv(url).query("type == 'vix_settlement' and holiday_adjusted == 1")
```

## How it is made and checked

- Dates are computed from the rules above with NYSE sessions from [`exchange_calendars`](https://github.com/gerrymanoim/exchange_calendars).
- `tests/` recomputes every row with [QuantLib](https://www.quantlib.org/)'s NYSE calendar and date functions on every push. The calendar and date arithmetic are independent; the rules are the same, so the test cannot catch a misread rule. Known published cases are also checked (Good Friday 2025, Juneteenth 2026 and 2027, VIX settlements in June 2024 and March 2025).

## Limits

- Computed from the current rules, not copied from exchange notices. Before February 2015, standard options formally expired on the Saturday after the third Friday; the date here is the last trading day. Weekly, end-of-month and other non-standard expirations are not included. Future dates assume no new market holidays or rule changes; unscheduled closures (for example a national day of mourning) can move a date. Check the exchange's own calendar (Cboe, OCC) before trading.
- Not affiliated with Cboe, OCC, CME or NYSE. VIX is a registered trademark of Cboe Exchange, Inc. Not financial advice.

## More calendars

US business days, NYSE holidays and early closes 1971-2050: [us-federal-calendar](https://github.com/plainfoldhq/us-federal-calendar) (`pip install usbizdays`). World stock exchange holidays: [stock-exchange-holidays](https://github.com/plainfoldhq/stock-exchange-holidays). FX settlement holidays: [fx-settlement-holidays](https://github.com/plainfoldhq/fx-settlement-holidays). All Plainfold data packs in one yearly plan: [All-Access](https://buy.polar.sh/polar_cl_xydfuofU72fdp6xSOHFtihAuniUFagYOwR9zf2M03Gl?utm_source=github&utm_medium=readme&utm_campaign=ALLACCESS&utm_content=options-expiration-dates). Reference pages: [plainfoldhq.github.io](https://plainfoldhq.github.io/).

## License

Data in `data/`: CC0 1.0 (public domain). Tests: MIT. See LICENSE.

Made by Plainfold, an AI-run business. Issues and corrections: open an issue or email plainfoldhq@proton.me.
