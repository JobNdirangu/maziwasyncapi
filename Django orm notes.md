# Django ORM — The `objects` Manager
### Lecture Notes (using our Milk Collection Cooperative models)

These notes explain **how and when to use** the most important Django ORM manager methods, using the real models from our project: `User`, `FarmerProfile`, `PorterProfile`, `MilkCollection`, `Payment`, `Feedback`, and `Notice`.

---

## 1. Introduction

Every Django model automatically gets a manager called **`objects`**. This manager is how our Python code talks to the database.

```
Database
    ↑
Model.objects
    ↑
Our Django Code
```

Our key models for these examples:

```python
class FarmerProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    farm_name = models.CharField(max_length=200, blank=True, null=True)
    number_of_cows = models.IntegerField(default=0)
    total_milk_delivered = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ...

class MilkCollection(BaseModel):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='collections')
    porter = models.ForeignKey(PorterProfile, on_delete=models.CASCADE, related_name='collections')
    liters = models.DecimalField(max_digits=10, decimal_places=2)
    session = models.CharField(max_length=10, choices=SESSION_CHOICES)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

class Payment(BaseModel):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_ref = models.CharField(max_length=100, unique=True)
```

Everything starts with:

```python
FarmerProfile.objects
MilkCollection.objects
Payment.objects
```

---

## 2. `all()` — Get every record

```python
farmers = FarmerProfile.objects.all()
```

**SQL equivalent**
```sql
SELECT * FROM farmerprofile;
```

**Output** — a `QuerySet` containing every `FarmerProfile` object:
```
<QuerySet [<FarmerProfile: John Kamau>, <FarmerProfile: Mary Wanjiru>, ...]>
```

**When to use:** when you want the full list — e.g. "show all farmers" or "list all payments" on an admin dashboard.

---

## 3. `get()` — Get exactly ONE record

```python
farmer = FarmerProfile.objects.get(id=1)
```

**Output** — a single `FarmerProfile` object (NOT a QuerySet):
```
<FarmerProfile: John Kamau>
```

**Exceptions to watch for:**

| Situation | Exception raised |
|---|---|
| No matching row | `FarmerProfile.DoesNotExist` |
| More than one matching row | `FarmerProfile.MultipleObjectsReturned` |

**When to use:** when you expect a unique result — e.g. fetching a farmer by `membership_number`, or a payment by `transaction_ref`.

```python
payment = Payment.objects.get(transaction_ref="TX12345")
```

---

## 4. `filter()` — Get MULTIPLE matching records

```python
completed_payments = Payment.objects.filter(status="COMPLETED")
```

**SQL equivalent**
```sql
SELECT * FROM payment WHERE status='COMPLETED';
```

**Output** — always a `QuerySet`, even if only one row matches:
```
<QuerySet [<Payment: TX12345 - KES 2500.00>, <Payment: TX12346 - KES 1800.00>]>
```

**Real example — a porter's collections for the morning session:**
```python
MilkCollection.objects.filter(porter=porter, session="MORNING")
```

**When to use:** whenever more than one object *could* match your condition.

---

## 5. `exclude()` — Get everything EXCEPT the match

```python
pending_or_failed = Payment.objects.exclude(status="COMPLETED")
```

**SQL equivalent**
```sql
SELECT * FROM payment WHERE status != 'COMPLETED';
```

**Real example — every farmer not attached to a specific porter's route:**
```python
FarmerProfile.objects.exclude(assigned_porters=porter)
```

---

## 6. `create()` — Build AND save in one step

```python
Payment.objects.create(
    farmer=farmer,
    amount=2500,
    payment_method="MPESA",
    transaction_ref="TX12345",
    payment_date=timezone.now()
)
```

This is equivalent to:

```python
payment = Payment(
    farmer=farmer,
    amount=2500,
    payment_method="MPESA",
    transaction_ref="TX12345",
    payment_date=timezone.now()
)
payment.save()
```

**When to use:** whenever you're creating a new row and don't need to modify it before saving (e.g. logging a new `MilkCollection` entry as a porter submits it).

---

## 7. `count()` — Count rows

```python
FarmerProfile.objects.count()
```

**Output:**
```
125
```

**Real example — total collections recorded today:**
```python
MilkCollection.objects.filter(collection_date=today).count()
```

---

## 8. `exists()` — Check if any row matches

```python
Feedback.objects.filter(status="PENDING").exists()
```

**Output:** `True` or `False`

**Why prefer this over `count() > 0`?** `exists()` runs a lightweight `SELECT 1 ... LIMIT 1` query instead of counting every row — much faster on large tables.

**Real example — check if a farmer already has an active mpesa number registered:**
```python
FarmerProfile.objects.filter(mpesa_number=number).exists()
```

---

## 9. `first()` and `last()` — Grab one end of the QuerySet

```python
MilkCollection.objects.filter(farmer=farmer).order_by("-collection_date").first()
```

**When to use:** e.g. get a farmer's most recent milk collection, or a porter's very first collection (`.last()` on the same ordering).

---

## 10. `order_by()` — Sort results

```python
# Ascending (lowest first)
FarmerProfile.objects.order_by("total_milk_delivered")

# Descending (highest first)
FarmerProfile.objects.order_by("-total_milk_delivered")
```

**Real example — leaderboard of top milk producers:**
```python
top_farmers = FarmerProfile.objects.order_by("-total_milk_delivered")[:10]
```

---

## 11. `update()` — Bulk update matching rows

```python
Payment.objects.filter(status="PENDING").update(status="COMPLETED")
```

**SQL equivalent**
```sql
UPDATE payment SET status='COMPLETED' WHERE status='PENDING';
```

⚠️ **Important:** `update()` works on a **QuerySet**, not on a single retrieved instance's `.save()`. It skips each object's `save()` method (and any custom logic inside it, like our `MilkCollection.save()` override that calculates `total_amount`), so use it only for simple bulk field changes.

---

## 12. `delete()` — Remove matching rows

```python
Notice.objects.filter(is_important=False, created_at__lt=one_year_ago).delete()
```

**When to use:** cleanup tasks — e.g. purging old, non-important notices.

---

## 13. `values()` — Return dictionaries instead of model instances

```python
Payment.objects.values("amount", "status")
```

**Output:**
```python
[
    {"amount": 2500, "status": "COMPLETED"},
    {"amount": 1800, "status": "PENDING"},
]
```

**When to use:** when you only need specific fields (not full model instances) — e.g. exporting a lightweight report.

---

## 14. `values_list()` — Return tuples instead of dictionaries

```python
Payment.objects.values_list("amount", "status")
```

**Output:**
```python
[(2500, "COMPLETED"), (1800, "PENDING")]
```

**Single column with `flat=True`:**
```python
FarmerProfile.objects.values_list("phone_number", flat=True)
```

**Output:**
```python
["0712345678", "0798765432", "0722111222"]
```

---

## 15. `aggregate()` — Perform calculations across a QuerySet

```python
from django.db.models import Sum, Avg, Max, Min, Count

Payment.objects.aggregate(total=Sum("amount"))
```

**Output:**
```python
{"total": 254300.00}
```

**Real example — total liters collected by a porter:**
```python
PorterProfile.objects.filter(id=porter.id).aggregate(
    total_liters=Sum("collections__liters")
)
```

**Other aggregate functions:** `Avg()`, `Max()`, `Min()`, `Count()`

---

## 16. `latest()` and `earliest()` — Newest / oldest by a date field

```python
Payment.objects.latest("payment_date")   # most recent payment
Payment.objects.earliest("payment_date") # oldest payment
```

---

## 17. `get_or_create()` — Fetch if it exists, otherwise create it

```python
notice, created = Notice.objects.get_or_create(
    title="System Maintenance",
    defaults={
        "message": "The system will be down for maintenance on Sunday.",
        "target": "ALL",
        "created_by": admin_user,
    }
)
```

- If found → returns the existing object, `created = False`
- If not found → creates it, `created = True`

**Real example — avoid duplicate farmer records during data import:**
```python
farmer, created = FarmerProfile.objects.get_or_create(
    national_id="12345678",
    defaults={"user": user, "first_name": "John", "last_name": "Kamau"}
)
```

---

## 18. `update_or_create()` — Update if it exists, otherwise create it

```python
Payment.objects.update_or_create(
    transaction_ref="TX12345",
    defaults={"status": "COMPLETED", "amount": 2500}
)
```

**When to use:** great for webhook/callback handlers — e.g. an M-Pesa payment confirmation callback that should update the existing `Payment` record (matched by `originator_conversation_id`) rather than create a duplicate.

---

## 19. Understanding QuerySet vs. Single Object

This is the single most common source of bugs for beginners.

### Example 1 — `all()` / `filter()` → QuerySet (many objects)

```python
collections = MilkCollection.objects.filter(session="MORNING")
```

```
collections
│
├── MilkCollection
├── MilkCollection
└── MilkCollection
```

### Example 2 — `get()` → Single Object

```python
collection = MilkCollection.objects.get(id=1)
```

```
collection
│
└── MilkCollection
```

---

## 20. Common DRF Mistake: forgetting `many=True`

Suppose we have:

```python
farmers = FarmerProfile.objects.all()
```

**❌ Wrong:**
```python
serializer = FarmerProfileSerializer(farmers)
```

**Error:**
```
AttributeError: 'QuerySet' object has no attribute 'first_name'
```

**Why?** DRF is trying to read `farmers.first_name` — but `farmers` is a `QuerySet` of many objects, not a single `FarmerProfile`.

**✅ Correct:**
```python
serializer = FarmerProfileSerializer(farmers, many=True)
```

**Single object — no `many=True` needed:**
```python
farmer = FarmerProfile.objects.get(id=1)
serializer = FarmerProfileSerializer(farmer)
```

---

## 21. Summary Table

| Method | Returns | Serializer needs `many=True`? |
|---|---|---|
| `all()` | QuerySet | ✅ Yes |
| `filter()` | QuerySet | ✅ Yes |
| `exclude()` | QuerySet | ✅ Yes |
| `values()` / `values_list()` | QuerySet (of dicts/tuples) | N/A — not model instances |
| `get()` | Single Object | ❌ No |
| `first()` / `last()` | Single Object (or `None`) | ❌ No |
| `create()` | Single Object | ❌ No |
| `latest()` / `earliest()` | Single Object | ❌ No |
| `get_or_create()` / `update_or_create()` | Tuple: (Single Object, bool) | ❌ No |

---

## 22. Best Practices

- Use `get()` only when you're certain exactly one row matches (e.g. by a unique field like `transaction_ref`, `national_id`, or `membership_number`).
- Use `filter()` whenever multiple rows could match — this is the safer default.
- Always add `many=True` when serializing a QuerySet in DRF.
- Use `exists()` instead of `count() > 0` for existence checks — it's faster.
- Use `select_related()` for `ForeignKey` / `OneToOneField` lookups (e.g. `MilkCollection.objects.select_related("farmer", "porter")`) and `prefetch_related()` for `ManyToManyField` / reverse FK lookups (e.g. `PorterProfile.objects.prefetch_related("assigned_farmers")`) to avoid the N+1 query problem.
- Be careful with `update()` and `delete()` on QuerySets — they operate directly on the database and **bypass each instance's `save()`/`delete()` method**, so custom logic (like our `MilkCollection.save()` that auto-calculates `total_amount`) won't run.
- Use `get_or_create()` / `update_or_create()` for idempotent operations like webhook handlers, imports, or "first login" setup logic.

---

*These notes map every core ORM concept directly onto our Milk Collection Cooperative models — `User`, `FarmerProfile`, `PorterProfile`, `MilkCollection`, `Payment`, `Feedback`, and `Notice` — so students can see exactly how these patterns apply to a real, working schema.*