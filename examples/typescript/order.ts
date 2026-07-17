type LineItem = Readonly<{
  sku: string;
  quantity: number;
  unitPriceCents: number;
}>;

function totalCents(items: readonly LineItem[]): number {
  if (items.length === 0) throw new Error("an order needs an item");
  return items.reduce((total, item) => {
    if (!Number.isSafeInteger(item.quantity) || item.quantity <= 0) {
      throw new Error("quantity must be a positive integer");
    }
    if (!Number.isSafeInteger(item.unitPriceCents) || item.unitPriceCents <= 0) {
      throw new Error("unitPriceCents must be a positive integer");
    }
    if (item.sku.trim() === "") throw new Error("sku is required");
    return total + item.quantity * item.unitPriceCents;
  }, 0);
}

const order = { customerId: "customer-1", items: [{ sku: "book", quantity: 2, unitPriceCents: 1250 }] };
const subtotalCents = totalCents(order.items);
console.assert(subtotalCents === 2500);
console.log(JSON.stringify({ ...order, subtotalCents }));

