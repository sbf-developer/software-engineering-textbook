#!/usr/bin/env python3
"""Run dependency-light checks used by the book's example repository."""
from __future__ import annotations

import json
import pathlib
import shutil
import sqlite3
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(cmd: list[str], *, cwd: pathlib.Path = ROOT, input: str | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, input=input, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"command failed: {' '.join(cmd)}")
    return result.stdout


def python_checks() -> None:
    sys.path.insert(0, str(ROOT / "examples" / "python"))
    from ledgerline import ValidationError, create_order, total_cents

    assert total_cents([{"sku": "book", "quantity": 2, "unit_price_cents": 1250}]) == 2500
    order = create_order("customer-1", [{"sku": "book", "quantity": 2, "unit_price_cents": 1250}])
    assert order["total_cents"] == 3125
    try:
        create_order("customer-1", [{"sku": "book", "quantity": 0, "unit_price_cents": 1250}])
    except ValidationError:
        pass
    else:
        raise AssertionError("invalid quantity was accepted")


def sql_checks() -> None:
    schema = (ROOT / "examples" / "sql" / "schema.sql").read_text()
    with sqlite3.connect(":memory:") as db:
        db.executescript(schema)
        db.execute("INSERT INTO orders(id, customer_id, total_cents, status) VALUES (?, ?, ?, ?)", ("o-1", "c-1", 2500, "accepted"))
        db.execute("INSERT INTO order_items(order_id, sku, quantity, unit_price_cents) VALUES (?, ?, ?, ?)", ("o-1", "book", 2, 1250))
        row = db.execute("SELECT total_cents FROM order_totals WHERE order_id = 'o-1'").fetchone()
        assert row == (2500,)


def cpp_checks() -> None:
    compiler = shutil.which("g++")
    if not compiler:
        print("SKIP: g++ not installed")
        return
    with tempfile.TemporaryDirectory() as temp:
        binary = pathlib.Path(temp) / "latency"
        run([compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror", "-pedantic", "examples/cpp/latency_bucket.cpp", "-o", str(binary)])
        output = run([str(binary)])
        assert "p95=180" in output


def node_checks() -> None:
    node = shutil.which("node")
    if not node:
        print("SKIP: node not installed")
        return
    run([node, "examples/typescript/order.ts"])


def java_checks() -> None:
    java = shutil.which("java")
    if not java:
        print("SKIP: java not installed")
        return
    output = run([java, "examples/java/RetryPolicy.java"])
    assert output.strip() == "1000"


def shell_checks() -> None:
    output = run(["env", "HEALTH_URL=mock://ok", "bash", "examples/shell/healthcheck.sh"])
    assert output.strip() == "ok"


def main() -> None:
    python_checks()
    sql_checks()
    cpp_checks()
    node_checks()
    java_checks()
    shell_checks()
    print(json.dumps({"status": "ok", "checks": ["python", "sql", "cpp", "node", "java", "shell"]}))


if __name__ == "__main__":
    main()
