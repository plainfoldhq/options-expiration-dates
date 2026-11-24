"""Recompute every row with QuantLib (NYSE calendar + date functions), independent of exchange_calendars,
which generated the file.

    pip install QuantLib
    python -m unittest discover -s tests -v
"""
import csv
import os
import unittest

import QuantLib as ql

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "expirations_2000_2050.csv")
NYSE = ql.UnitedStates(ql.UnitedStates.NYSE)


def iso(d):
    return f"{d.year():04d}-{d.month():02d}-{d.dayOfMonth():02d}"


def prev_session(d):
    return NYSE.adjust(d, ql.Preceding)


def expected(kind, y, m):
    if kind == "monthly_options_last_trading_day":
        return prev_session(ql.Date.nthWeekday(3, ql.Friday, m, y))
    if kind == "imm_date":
        return ql.IMM.nextDate(ql.Date(1, m, y), False)
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    return prev_session(prev_session(ql.Date.nthWeekday(3, ql.Friday, nm, ny)) - 30)


class Data(unittest.TestCase):
    def test_rows(self):
        with open(DATA, newline="") as f:
            rs = list(csv.DictReader(f))
        kinds = {}
        for r in rs:
            y, m = map(int, r["contract_month"].split("-"))
            self.assertEqual(iso(expected(r["type"], y, m)), r["date"], r)
            kinds[r["type"]] = kinds.get(r["type"], 0) + 1
        self.assertEqual(kinds, {"monthly_options_last_trading_day": 612, "imm_date": 204, "vix_settlement": 552})

    def test_known(self):
        with open(DATA, newline="") as f:
            d = {(r["type"], r["contract_month"]): r["date"] for r in csv.DictReader(f)}
        self.assertEqual(d[("monthly_options_last_trading_day", "2025-04")], "2025-04-17")  # Good Friday
        self.assertEqual(d[("monthly_options_last_trading_day", "2026-06")], "2026-06-18")  # Juneteenth
        self.assertEqual(d[("vix_settlement", "2024-06")], "2024-06-18")  # Juneteenth Wednesday
        self.assertEqual(d[("vix_settlement", "2025-03")], "2025-03-18")  # Good Friday Apr 18, 2025
        self.assertEqual(d[("monthly_options_last_trading_day", "2027-06")], "2027-06-17")


if __name__ == "__main__":
    unittest.main()
