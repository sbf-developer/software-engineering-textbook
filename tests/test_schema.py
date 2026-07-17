import pathlib
import sqlite3
import unittest


class SchemaTests(unittest.TestCase):
    def test_constraints_and_total_view(self):
        schema = (pathlib.Path(__file__).resolve().parents[1] / "examples" / "sql" / "schema.sql").read_text()
        with sqlite3.connect(":memory:") as db:
            db.executescript(schema)
            db.execute("INSERT INTO orders(id, customer_id, total_cents, status) VALUES (?, ?, ?, ?)", ("o-1", "c-1", 2500, "accepted"))
            db.execute("INSERT INTO order_items(order_id, sku, quantity, unit_price_cents) VALUES (?, ?, ?, ?)", ("o-1", "book", 2, 1250))
            self.assertEqual(db.execute("SELECT total_cents FROM order_totals WHERE order_id = 'o-1'").fetchone(), (2500,))
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("INSERT INTO order_items(order_id, sku, quantity, unit_price_cents) VALUES (?, ?, ?, ?)", ("o-1", "bad", 0, 100))


if __name__ == "__main__":
    unittest.main()

