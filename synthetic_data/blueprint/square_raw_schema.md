# Square Raw Schema Blueprint

## Purpose

One row = one vendor (Square representation)

Total rows:
- 2,000

This table represents a **Square-like API output layer** derived from:
- vendor_master
- transactions

It simulates how Square would expose:
- merchant and payment behavior
- transaction intensity
- locality signals
- repeat behavior
- confidence signals

This is a **source system view**, not the final truth.

---

## Table: square_raw

---

## A. Identity Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| vendor_id | INTEGER | Must match vendor_master | 1001 | Join key to canonical layer |
| merchant_name | VARCHAR(150) | Free text | GlowSkin Co | Vendor name in Square |
| merchant_category_code | VARCHAR(10) | Synthetic MCC-like code | 5977 | Merchant category code |
| transaction_created_at | TIMESTAMP | Valid datetime | 2024-03-15 14:25:00 | Latest transaction anchor timestamp |

---

## B. Customer & Transaction Behavior Signals

| Column Name | Type | Allowed Values / Range | Example | Description |
|------------|------|------------------------|--------|-------------|
| repeat_customer_flag | INTEGER | 0 or 1 | 1 | Whether repeat behavior is present strongly enough |
| product_mix_score | FLOAT | 0.00 to 1.00 | 0.79 | Breadth and alignment of product mix |
| transaction_volume_score | FLOAT | 0.00 to 1.00 | 0.82 | Relative transaction strength |
| conversion_rate_estimate | FLOAT | 0.00 to 1.00 | 0.54 | Estimated conversion strength |
| receipt_visual_score | FLOAT | 0.00 to 1.00 | 0.68 | Visual quality proxy inferred from business context |

---

## C. Niche and Recommendation Signals

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| predicted_micro_niche_1 | CATEGORICAL | Same as vendor_master niches | Skincare_Enthusiasts | Primary niche prediction |
| predicted_micro_niche_2 | CATEGORICAL | Same as vendor_master niches + None | Organic_Beauty | Secondary niche prediction |
| recommended_platform_primary | CATEGORICAL | Instagram, TikTok, YouTube_Shorts, Pinterest, Reddit, Facebook_Groups, Discord, Website_First, Marketplace_First, Micro_Influencers | Instagram | Primary platform recommendation |
| recommended_platform_secondary | CATEGORICAL | Same as above + None | TikTok | Secondary platform recommendation |
| platform_fit_score_raw | FLOAT | 0.00 to 1.00 | 0.84 | Raw platform fit score |

---

## D. Dense Slice & Geography Signals

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| dense_slice_prediction_1 | CATEGORICAL | Same as vendor_master dense slices | Urban_Female_20_30 | Primary dense-slice prediction |
| dense_slice_prediction_2 | CATEGORICAL | Same as vendor_master dense slices + None | Young_Professionals | Secondary dense-slice prediction |
| location_type | CATEGORICAL | Urban, Suburban, Mixed, College_Town, Downtown_CBD, Regional_Hub, Neighborhood_Local, National_Distributed, Wellness_Corridor, Family_Suburb_Belt | Urban | Primary locality type |
| confidence_score | FLOAT | 0.00 to 1.00 | 0.80 | Confidence in recommendation bundle |

---

## E. Payment & Revenue Summary Signals

| Column Name | Type | Allowed Values / Range | Example | Description |
|------------|------|------------------------|--------|-------------|
| avg_ticket_size_estimate | FLOAT | 1.00 to 500.00+ | 41.20 | Average payment size |
| monthly_payment_volume_estimate | FLOAT | 100 to 200000+ | 17600 | Monthly transaction volume estimate |
| payment_locality_score | FLOAT | 0.00 to 1.00 | 0.83 | Strength of local transaction concentration |
| repeat_payment_revenue_ratio | FLOAT | 0.00 to 1.00 | 0.61 | Share of payment volume from repeat customers |
| merchant_stability_score | FLOAT | 0.00 to 1.00 | 0.74 | Stability of merchant transaction profile |

---

## Row Count

- Total rows: 2,000

---

## Generation Logic

### Rule 1: Derived from vendor_master
These fields map directly or near-directly:
- vendor_id
- merchant_name ← business_name
- predicted_micro_niche_1 ← top_micro_niche_1
- predicted_micro_niche_2 ← top_micro_niche_2
- recommended_platform_primary ← recommended_platform_1
- recommended_platform_secondary ← recommended_platform_2
- dense_slice_prediction_1 ← recommended_dense_slice_1
- location_type ← geography_signal

### Rule 2: merchant_category_code is mapped from business_category
Use synthetic MCC-like mapping, for example:
- Beauty → 5977
- Fitness → 5941
- Fashion → 5651
- Food → 5411
- Home → 5712
- Wellness → 8099
- Pets → 5995
- Tech_Accessories → 5732
- Crafts → 5945
- Education → 8299

This does not need to be perfectly real-world exact. It just needs to be internally consistent.

### Rule 3: Derived from transactions aggregation
These should be computed from transaction behavior:
- repeat_customer_flag
- transaction_volume_score
- conversion_rate_estimate
- avg_ticket_size_estimate
- monthly_payment_volume_estimate
- payment_locality_score
- repeat_payment_revenue_ratio
- merchant_stability_score

### Rule 4: Derived from vendor baseline + noise
These come from vendor_master with slight variation:
- product_mix_score
- receipt_visual_score
- platform_fit_score_raw
- confidence_score

### Rule 5: Hero vs Weak differentiation

#### Hero vendors
Bias toward:
- higher transaction_volume_score
- higher payment_locality_score
- higher repeat_payment_revenue_ratio
- higher merchant_stability_score

#### Moderate vendors
Bias toward:
- mid-range values
- moderate variability

#### Weak vendors
Bias toward:
- lower repeat indicators
- lower locality concentration
- lower stability
- more noise

### Rule 6: Geography consistency
If:
- location_type = Urban
- dense_slice_prediction_1 = Urban_Female_20_30

Then:
- payment_locality_score should be higher
- confidence_score should tend to be higher

---

## Value Ranges

| Field | Range |
|------|------|
| product_mix_score | 0.00 to 1.00 |
| transaction_volume_score | 0.00 to 1.00 |
| conversion_rate_estimate | 0.00 to 1.00 |
| receipt_visual_score | 0.00 to 1.00 |
| platform_fit_score_raw | 0.00 to 1.00 |
| confidence_score | 0.00 to 1.00 |
| avg_ticket_size_estimate | 8.00 to 220.00 typical |
| monthly_payment_volume_estimate | 500 to 120000 typical |
| payment_locality_score | 0.00 to 1.00 |
| repeat_payment_revenue_ratio | 0.00 to 1.00 |
| merchant_stability_score | 0.00 to 1.00 |

---

## Example Row

| Column | Value |
|--------|------|
| vendor_id | 1001 |
| merchant_name | GlowSkin Co |
| merchant_category_code | 5977 |
| transaction_created_at | 2024-03-15 14:25:00 |
| repeat_customer_flag | 1 |
| product_mix_score | 0.79 |
| transaction_volume_score | 0.82 |
| conversion_rate_estimate | 0.54 |
| receipt_visual_score | 0.68 |
| predicted_micro_niche_1 | Skincare_Enthusiasts |
| predicted_micro_niche_2 | Organic_Beauty |
| recommended_platform_primary | Instagram |
| recommended_platform_secondary | TikTok |
| platform_fit_score_raw | 0.84 |
| dense_slice_prediction_1 | Urban_Female_20_30 |
| dense_slice_prediction_2 | Young_Professionals |
| location_type | Urban |
| confidence_score | 0.80 |
| avg_ticket_size_estimate | 41.20 |
| monthly_payment_volume_estimate | 17600 |
| payment_locality_score | 0.83 |
| repeat_payment_revenue_ratio | 0.61 |
| merchant_stability_score | 0.74 |

---

## Layer Connections

### Input
- vendor_master
- transactions

### Output feeds into
- square_staging_pipeline
- canonical merge layer

---

## Summary

- Represents Square-style summarized merchant and payment signals
- Derived from vendor truth + transaction behavior
- Strongest for locality, repeat, and payment-driven signals
- Complements Shopify’s niche, platform, and content emphasis