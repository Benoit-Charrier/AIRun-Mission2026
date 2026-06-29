---
kata: 4.W.4
artefact: integration-contract
integration: POS Client → Apollo Gateway — cartMerge operation
date: 2026-06-26
---

# Integration Contract — POS Cart-Bridge

## Contract: `cartMerge` (POS Client → Apollo Gateway)

**API style:** GraphQL over HTTPS (POST to `/graphql`)
**Auth method:** Bearer token in `Authorization` header — issued by Identity Service after loyalty QR validation; JWT signed by Auth0, validated locally by Identity Service

### Request

```graphql
mutation CartMerge($loyaltyQR: String!, $storeId: ID!) {
  cartMerge(loyaltyQR: $loyaltyQR, storeId: $storeId) {
    cart {
      id
      customerId
      lineItems {
        sku
        name
        quantity
        unitPrice { amount currency }
        availability {
          state          # in_stock | likely | uncertain | not_available | cannot_confirm
          confidence     # 0.0–1.0
          freshnessMin   # minutes since last SAP sync
        }
      }
      totalPrice { amount currency }
    }
    errors {
      code    # CART_NOT_FOUND | STORE_INVALID | AUTH_FAILED | INVENTORY_UNAVAILABLE
      message
    }
  }
}
```

### Response — happy path (HTTP 200)

```json
{
  "data": {
    "cartMerge": {
      "cart": {
        "id": "cart-8a3f...",
        "customerId": "cust-00042",
        "lineItems": [
          {
            "sku": "SKU-001",
            "name": "Meridian Canvas Backpack",
            "quantity": 1,
            "unitPrice": { "amount": 4999, "currency": "GBP" },
            "availability": {
              "state": "in_stock",
              "confidence": 0.88,
              "freshnessMin": 8
            }
          }
        ],
        "totalPrice": { "amount": 4999, "currency": "GBP" }
      },
      "errors": []
    }
  }
}
```

### Error — inventory cache miss with SAP timeout (HTTP 200, partial data)

**Trigger:** `Inventory Cache` returns no record for a SKU AND SAP ECC RFC call exceeds 1000ms timeout.

```json
{
  "data": {
    "cartMerge": {
      "cart": {
        "id": "cart-8a3f...",
        "lineItems": [
          {
            "sku": "SKU-042",
            "availability": {
              "state": "cannot_confirm",
              "confidence": null,
              "freshnessMin": null
            }
          }
        ]
      },
      "errors": [
        {
          "code": "INVENTORY_UNAVAILABLE",
          "message": "Stock data unavailable for SKU-042 at store MER-LON-03. Confirm availability with floor staff."
        }
      ]
    }
  }
}
```

**Expected POS behaviour on `INVENTORY_UNAVAILABLE`:** render the line item with `cannot_confirm` badge and a "Check with staff" inline note. DO NOT block the cart from proceeding to payment.

### Other error codes

| Code | HTTP status | Trigger | POS action |
|------|-------------|---------|-----------|
| `AUTH_FAILED` | 401 | Invalid or expired loyalty QR token | Re-prompt QR scan |
| `CART_NOT_FOUND` | 200 (partial) | Customer has no active online cart | Show empty cart state; allow manual item entry |
| `STORE_INVALID` | 400 | `storeId` not found in platform | Log error; escalate to tech support |

### SLA

- **p95 latency target (happy path, all cache hits):** < 200ms gateway response
- **p95 latency target (with SAP inline fallback, 1 cache miss):** < 1500ms
- **Timeout:** Gateway returns partial `cannot_confirm` result after 1000ms SAP wait; does not hold the POS connection beyond 1500ms total
