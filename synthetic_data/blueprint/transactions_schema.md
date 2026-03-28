# Transactions Schema Blueprint

## Purpose

One row = one transaction

Total rows:
- 250,000

This table represents the behavioral activity layer of the system.

It is generated from `vendor_master` and is used to:
- simulate purchase behavior
- create repeat customer patterns
- generate locality and platform signals
- feed Shopify raw summaries
- feed Square raw summaries

---

## Table: transactions

---

## A. Core Identity Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| transaction_id | INTEGER | Unique integer | 5000001 | Primary key for transaction |
| vendor_id | INTEGER | Must exist in vendor_master | 1001 | Foreign key to vendor_master |
| customer_id | VARCHAR(50) | Synthetic customer ID | CUST_1001_00023 | Customer identifier |
| transaction_timestamp | TIMESTAMP | Valid UTC timestamp | 2024-03-15 14:25:00 | Timestamp of transaction |

---

## B. Commercial Transaction Columns

| Column Name | Type | Allowed Values / Range | Example | Description |
|------------|------|------------------------|--------|-------------|
| order_value_usd | FLOAT | 1.00 to 1000.00+ | 42.75 | Value of the transaction |
| item_count | INTEGER | 1 to 20 | 2 | Number of items in transaction |
| product_category_tag | CATEGORICAL | Beauty, Fitness, Fashion, Food, Home, Wellness, Pets, Tech_Accessories, Crafts, Education | Beauty | Product category aligned to vendor |
| payment_method | CATEGORICAL | card, wallet, cash, subscription, installment | card | Payment type used |
| conversion_flag | INTEGER | 0 or 1 | 1 | Whether transaction converted successfully |

---

## C. Customer Behavior Columns

| Column Name | Type | Allowed Values / Range | Example | Description |
|------------|------|------------------------|--------|-------------|
| is_repeat_customer | INTEGER | 0 or 1 | 1 | Repeat customer flag |
| customer_sequence_number | INTEGER | 1 to 100+ | 3 | Number of purchases made by this customer with the vendor |
| customer_ltv_running_usd | FLOAT | 1.00 to 5000.00+ | 128.50 | Running lifetime value for this customer with vendor |
| days_since_previous_purchase | INTEGER | 0 to 3650 | 21 | Gap since last purchase for same customer |
| return_risk_flag | INTEGER | 0 or 1 | 0 | Optional synthetic churn or return risk marker |

---

## D. Channel and Platform Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| acquisition_channel | CATEGORICAL | Organic_Social, Paid_Social, Referral, Search, Marketplace, Direct, Community, Email_CRM, Influencer, Offline_to_Online | Organic_Social | Channel that drove the purchase |
| platform_touchpoint | CATEGORICAL | Instagram, TikTok, YouTube_Shorts, Pinterest, Reddit, Facebook_Groups, Discord, Website_First, Marketplace_First, Micro_Influencers | Instagram | Platform associated with the transaction |
| session_intent_level | CATEGORICAL | Low, Medium, High | High | Synthetic pre-purchase intent marker |
| visual_engagement_proxy | FLOAT | 0.00 to 1.00 | 0.83 | Proxy for visual/content engagement strength |

---

## E. Geography and Dense Slice Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| geo_zone | CATEGORICAL | Urban, Suburban, Mixed, College_Town, Downtown_CBD, Regional_Hub, Neighborhood_Local, National_Distributed, Wellness_Corridor, Family_Suburb_Belt | Urban | Geographic behavior zone |
| dense_slice_tag | CATEGORICAL | Urban_Female_20_30, Male_18_35_Fitness, Suburban_Families, College_Students, Budget_Households, Young_Professionals, Pet_Owner_Communities, Home_Decor_Clusters, Local_Wellness_Seekers, Upskilling_Professionals | Urban_Female_20_30 | Dense market slice tag |
| locality_score | FLOAT | 0.00 to 1.00 | 0.79 | Strength of local concentration in this transaction |
| merchant_proximity_band | CATEGORICAL | Immediate_Local, Nearby_Local, Same_City, Same_Region, National, Unknown | Same_City | Distance or locality relationship to vendor |

---

## F. Optional Operational Columns

| Column Name | Type | Allowed Values / Range | Example | Description |
|------------|------|------------------------|--------|-------------|
| refund_flag | INTEGER | 0 or 1 | 0 | Whether the transaction was refunded |
| discount_applied_flag | INTEGER | 0 or 1 | 1 | Whether discount was applied |
| discount_amount_usd | FLOAT | 0.00 to 500.00 | 5.00 | Discount amount |
| net_revenue_usd | FLOAT | 0.00 to 1000.00+ | 37.75 | Net revenue after discount/refund logic |

---

## Row Count

- Total rows: 250,000

---

## Distribution Logic

### 1. Vendor-linked distribution
Each transaction must belong to exactly one vendor through:
- `vendor_id`

The number of transactions per vendor is controlled by:
- `target_transaction_count` from `vendor_master`
- `transaction_tier`

---

### 2. Transaction tiers

| Tier | Vendors | Total Transactions | Typical Per-Vendor Range |
|------|--------:|-------------------:|--------------------------|
| Tier_A_Power | 200 | 87,500 | 320 to 650 |
| Tier_B_Growth | 500 | 87,500 | 120 to 260 |
| Tier_C_Steady | 800 | 56,250 | 40 to 95 |
| Tier_D_Small | 500 | 18,750 | 15 to 55 |

---

### 3. Strength-class behavior bias

#### Hero vendors
Bias toward:
- more repeat customers
- higher order values
- stronger locality
- stronger visual engagement
- higher session intent
- lower refund probability

#### Moderate vendors
Bias toward:
- mixed repeat rates
- moderate order values
- balanced locality
- medium visual engagement
- moderate refund probability

#### Weak vendors
Bias toward:
- fewer repeat customers
- lower conversion quality
- lower locality concentration
- lower visual engagement
- more noise
- slightly higher refund probability

---

## Generation Rules

### Rule 1: All transactions inherit vendor identity context
From `vendor_master`, each transaction inherits or is influenced by:
- business_category
- top_micro_niche_1
- recommended_platform_1
- recommended_dense_slice_1
- geography_signal
- vendor_strength_class
- transaction_tier

---

### Rule 2: Repeat behavior must align with baseline
If vendor has:
- `repeat_customer_signal_base = 0.78`

Then the observed proportion of `is_repeat_customer = 1` across that vendor’s transactions should be close to that level, with small random variation.

---

### Rule 3: Order values must align with vendor baseline
If vendor has:
- `avg_order_value_usd_base = 42.50`

Then transaction-level `order_value_usd` values should fluctuate around that baseline, not randomly ignore it.

Suggested variation:
- Normal or log-normal style spread around vendor baseline

---

### Rule 4: Dense slice and geography must align
If vendor has:
- `recommended_dense_slice_1 = Urban_Female_20_30`
- `geography_signal = Urban`

Then most transactions should lean toward:
- `dense_slice_tag = Urban_Female_20_30`
- `geo_zone = Urban`
- higher `locality_score`

---

### Rule 5: Platform touchpoint should reflect recommended platform
If vendor has:
- `recommended_platform_1 = Instagram`

Then a larger proportion of that vendor’s transactions should have:
- `platform_touchpoint = Instagram`

but not necessarily 100%, because secondary platform and channel variation should exist.

---

### Rule 6: Quantitative fields should not be random noise
The following fields must be conditionally generated from vendor context:
- order_value_usd
- is_repeat_customer
- customer_ltv_running_usd
- visual_engagement_proxy
- locality_score
- net_revenue_usd

---

## Value Ranges

### order_value_usd
Recommended broad range:
- 8.00 to 220.00 for most vendors
- can go beyond for premium edge cases

### item_count
Range:
- 1 to 20

Typical:
- 1 to 5 for most vendors

### customer_sequence_number
Range:
- 1 to 100+

Typical:
- 1 to 8 for most synthetic buyers

### customer_ltv_running_usd
Range:
- 1.00 to 5000.00+

Depends on:
- repeat behavior
- order values
- customer history

### days_since_previous_purchase
Range:
- 0 to 3650

Typical:
- 7 to 90 for repeat-heavy businesses
- larger spread for weaker vendors

### visual_engagement_proxy
Range:
- 0.00 to 1.00

### locality_score
Range:
- 0.00 to 1.00

### discount_amount_usd
Range:
- 0.00 to 500.00

### net_revenue_usd
Range:
- 0.00 to 1000.00+

Usually:
- `order_value_usd - discount_amount_usd`
- may be reduced further if refund logic is applied

---

## Example Transaction Row

| Column | Value |
|--------|------|
| transaction_id | 5000001 |
| vendor_id | 1001 |
| customer_id | CUST_1001_00023 |
| transaction_timestamp | 2024-03-15 14:25:00 |
| order_value_usd | 42.75 |
| item_count | 2 |
| product_category_tag | Beauty |
| payment_method | card |
| conversion_flag | 1 |
| is_repeat_customer | 1 |
| customer_sequence_number | 3 |
| customer_ltv_running_usd | 128.50 |
| days_since_previous_purchase | 21 |
| return_risk_flag | 0 |
| acquisition_channel | Organic_Social |
| platform_touchpoint | Instagram |
| session_intent_level | High |
| visual_engagement_proxy | 0.83 |
| geo_zone | Urban |
| dense_slice_tag | Urban_Female_20_30 |
| locality_score | 0.79 |
| merchant_proximity_band | Same_City |
| refund_flag | 0 |
| discount_applied_flag | 1 |
| discount_amount_usd | 5.00 |
| net_revenue_usd | 37.75 |

---

## Layer Connections

### Input source
This table is generated from:
- `vendor_master`

### Output use cases
This table is used to derive:
- Shopify raw summary values
- Square raw summary values
- repeat customer metrics
- conversion signals
- geography and dense-slice patterns
- revenue and LTV signals

---

## Summary

- This is the behavioral layer of the system
- It makes the Shopify and Square raw layers realistic
- It must stay consistent with vendor_master
- It is the main driver of synthetic realism