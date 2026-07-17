import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "examples" / "python"))

from ledgerline import ValidationError, create_order, tax_cents, total_cents


class LedgerlineTests(unittest.TestCase):
    def test_total_is_exact_integer_money(self):
        self.assertEqual(total_cents([{"sku": "book", "quantity": 2, "unit_price_cents": 1250}]), 2500)

    def test_tax_uses_decimal_rounding(self):
        self.assertEqual(tax_cents(101, "0.25"), 25)

    def test_invalid_quantity_is_rejected(self):
        with self.assertRaises(ValidationError):
            create_order("customer-1", [{"sku": "book", "quantity": 0, "unit_price_cents": 1250}])


if __name__ == "__main__":
    unittest.main()

