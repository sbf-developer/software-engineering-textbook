PRAGMA foreign_keys = ON;

CREATE TABLE orders (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL CHECK (length(trim(customer_id)) > 0),
    total_cents INTEGER NOT NULL CHECK (total_cents > 0),
    status TEXT NOT NULL CHECK (status IN ('accepted', 'paid', 'cancelled')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sku TEXT NOT NULL CHECK (length(trim(sku)) > 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents > 0),
    PRIMARY KEY (order_id, sku)
);

CREATE VIEW order_totals AS
SELECT order_id, SUM(quantity * unit_price_cents) AS total_cents
FROM order_items
GROUP BY order_id;

