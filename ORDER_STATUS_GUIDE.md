# Order Status Management Guide

## Order Statuses

Wyatt Collection uses 6 order statuses to track the lifecycle of each order:

| Status | Description | Icon |
|--------|---|---|
| **Pending** | Order received but not yet confirmed | ⏳ |
| **Confirmed** | Order confirmed and ready for processing | ✓ |
| **Processing** | Order is being prepared for shipment | 📦 |
| **Shipped** | Order has been sent to customer | 🚚 |
| **Delivered** | Order received by customer | ✅ |
| **Cancelled** | Order was cancelled (no refund) | ✗ |

## Status Transitions

With the updated system, **any status can transition to any other status** (with the exception that you cannot transition to the same status). This provides maximum flexibility for:

- **Correcting mistakes** - Move an order back to an earlier status if incorrectly advanced
- **Handling exceptions** - Move a delivered order back to processing if customer reports issues
- **Cancellations** - Cancel orders at any stage
- **Reprocessing** - Move shipped orders back to processing if reshipment needed

### Valid Transitions (Updated)

```
pending      → confirmed, processing, shipped, delivered, cancelled
confirmed    → pending, processing, shipped, delivered, cancelled
processing   → pending, confirmed, shipped, delivered, cancelled
shipped      → pending, confirmed, processing, delivered, cancelled
delivered    → pending, confirmed, processing, shipped, cancelled
cancelled    → pending, confirmed, processing, shipped, delivered
```

## How to Update Order Status

### Single Order Update

1. Go to **Admin → Orders**
2. Click on the order number to open order details
3. Use the **Status** dropdown to select a new status
4. Click **Update Status**
5. Confirm the change

### Bulk Status Updates

1. Go to **Admin → Orders**
2. Check the checkboxes next to orders you want to update
3. In the **Actions** dropdown, select the target status (e.g., "Set to Processing")
4. Click **Apply**
5. The system will:
   - ✅ Update all valid transitions
   - ⚠️ Skip any orders that cannot transition
   - Show you how many were updated and how many were skipped

### Why Orders Get Skipped

Orders are skipped during bulk updates if:
- The transition rule doesn't allow it (rare with new flexible system)
- The order is already in that status
- There's a database or permission error (uncommon)

## Best Practices

### Order Flow (Recommended)
```
Pending → Confirmed → Processing → Shipped → Delivered
```

### When to Use Each Status

| Status | When to Set |
|--------|---|
| **Pending** | Right after order is received (auto-set by system) |
| **Confirmed** | After customer confirms and payment verified |
| **Processing** | When order is being packed/prepared |
| **Shipped** | When order leaves warehouse with tracking number |
| **Delivered** | When customer confirms receipt or after ~3 days |
| **Cancelled** | Order is no longer needed (any stage) |

### Managing Common Scenarios

#### Scenario: Customer Wants to Cancel
- Set status to **Cancelled** immediately
- Regardless of current status (pending, confirmed, processing, or shipped)
- No further transitions needed

#### Scenario: Wrong Status Set
- Move back to the correct status using the dropdown
- No penalties for status changes

#### Scenario: Customer Reports Non-Delivery
- Move from **Delivered** back to **Shipped**
- Investigate with customer
- Return to **Delivered** once resolved

#### Scenario: Need to Reprocess an Order
- Move from **Shipped** back to **Processing**
- Re-pack if needed
- Re-ship with new tracking

## Bulk Status Update Example

**Scenario:** You have 5 orders ready to ship

1. ✓ Go to Orders page
2. ✓ Check all 5 orders
3. ✓ Select "Set to Shipped" from Actions
4. ✓ Click Apply
5. ✓ All 5 should update successfully
6. ✓ You'll see: "5 order(s) updated to 'shipped'"

If any skip (rare), check:
- Is the order already in that status?
- Does the order have a different current status than expected?

## Status Update History

✅ **Recent Improvements:**
- Removed rigid linear transition rules
- All statuses now can transition to any other status
- Better error handling for bulk updates
- Clearer skip messages when transitions aren't allowed

## Notes

- Status changes are logged in the database (updated_at timestamp)
- Admin users can update order statuses at any time
- Customers cannot change order status (admin only)
- Changing status does NOT affect order items, pricing, or payment
- Status updates happen immediately (no undo, but you can change back)

---

**Need Help?** Check the order details page for the current status and use the dropdown to select any valid transition.
