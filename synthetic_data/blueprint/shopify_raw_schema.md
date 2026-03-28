# Shopify Raw Schema Blueprint

## Purpose

One row = one vendor (Shopify representation)

Total rows:
- 2,000

This table represents a **Shopify-like API output layer** derived from:
- vendor_master
- transactions

It simulates how Shopify would expose:
- customer behavior summaries
- niche signals
- platform signals
- content signals

This is a **source system view**, not the final truth.

---

## Table: shopify_raw

---

## A. Identity Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| vendor_id | INTEGER | Must match vendor_master | 1001 | Join key to canonical layer |
| shop_name | VARCHAR(150) | Free text | GlowSkin Co | Vendor name in Shopify |
| primary_category | CATEGORICAL | Beauty, Fitness, Fashion, Food, Home, Wellness, Pets, Tech_Accessories, Crafts, Education | Beauty | Primary category |
| created_at | TIMESTAMP | Valid datetime | 2023-06-15 10:00:00 | Store creation timestamp |

---

## B. Customer & Niche Signals

| Column Name | Type | Range / Values | Example | Description |
|------------|------|----------------|--------|-------------|
| customer_repeat_rate | FLOAT | 0.00 to 1.00 | 0.76 | Observed repeat customer rate |
| product_niche_fit_score | FLOAT | 0.00 to 1.00 | 0.84 | Alignment between product and niche |
| predicted_micro_niche_1 | CATEGORICAL | Same as vendor_master niches | Skincare_Enthusiasts | Primary predicted niche |
| predicted_micro_niche_2 | CATEGORICAL | Same as vendor_master niches + None | Organic_Beauty | Secondary predicted niche |
| niche_signal_raw | FLOAT | 0.00 to 1.00 | 0.82 | Raw niche clarity score |

---

## C. Content & Conversion Signals

| Column Name | Type | Range / Values | Example | Description |
|------------|------|----------------|--------|-------------|
| visual_score | FLOAT | 0.00 to 1.00 | 0.91 | Visual content strength proxy |
| conversion_efficiency_raw | FLOAT | 0.00 to 1.00 | 0.52 | Conversion efficiency |
| engagement_to_conversion_ratio | FLOAT | 0.00 to 10.00 | 2.40 | Engagement vs conversion ratio |
| content_consistency_score | FLOAT | 0.00 to 1.00 | 0.78 | Consistency of content output |

---

## D. Platform Signals

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| primary_platform_prediction | CATEGORICAL | Instagram, TikTok, YouTube_Shorts, Pinterest, Reddit, Facebook_Groups, Discord, Website_First, Marketplace_First, Micro_Influencers | Instagram | Primary platform |
| secondary_platform_prediction | CATEGORICAL | Same as above + None | TikTok | Secondary platform |
| platform_fit_raw | FLOAT | 0.00 to 1.00 | 0.88 | Platform alignment score |
| platform_dependency_score | FLOAT | 0.00 to 1.00 | 0.67 | Reliance on main platform |

---

## E. Geography & Dense Slice Signals

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| dense_slice_prediction_1 | CATEGORICAL | Same as vendor_master dense slices | Urban_Female_20_30 | Primary dense slice |
| dense_slice_prediction_2 | CATEGORICAL | Same as vendor_master dense slices + None | Young_Professionals | Secondary slice |
| geo_cluster_type | CATEGORICAL | Urban, Suburban, Mixed, College_Town, Downtown_CBD, Regional_Hub, Neighborhood_Local, National_Distributed, Wellness_Corridor, Family_Suburb_Belt | Urban | Geography cluster |
| dense_slice_confidence_raw | FLOAT | 0.00 to 1.00 | 0.81 | Confidence in slice prediction |

---

## F. Commerce Summary Signals

| Column Name | Type | Range / Values | Example | Description |
|------------|------|----------------|--------|-------------|
| avg_order_value_estimate | FLOAT | 1.00 to 500.00+ | 42.50 | Estimated AOV |
| monthly_revenue_estimate | FLOAT | 100 to 200000+ | 18500 | Estimated monthly revenue |
| returning_customer_revenue_ratio | FLOAT | 0.00 to 1.00 | 0.64 | Revenue from repeat customers |
| product_category_depth_score | FLOAT | 0.00 to 1.00 | 0.72 | Depth of product catalog |

---

## Row Count

- Total rows: 2,000

---

## Generation Logic

### Rule 1: Derived from vendor_master
These fields map directly:
- vendor_id
- shop_name ← business_name
- primary_category ← business_category
- predicted_micro_niche_1 ← top_micro_niche_1
- predicted_micro_niche_2 ← top_micro_niche_2
- primary_platform_prediction ← recommended_platform_1
- secondary_platform_prediction ← recommended_platform_2
- dense_slice_prediction_1 ← recommended_dense_slice_1
- geo_cluster_type ← geography_signal

---

### Rule 2: Derived from transactions aggregation

These must be computed using transaction data:

- customer_repeat_rate → ratio of repeat customers
- avg_order_value_estimate → avg(order_value_usd)
- monthly_revenue_estimate → sum(order_value_usd) normalized monthly
- returning_customer_revenue_ratio → repeat revenue / total revenue
- engagement_to_conversion_ratio → proxy using visual + conversion signals

---

### Rule 3: Derived from vendor baseline + noise

These come from vendor_master with slight variation:

- product_niche_fit_score ← niche_signal_score_base ± noise
- niche_signal_raw ← niche_signal_score_base ± noise
- visual_score ← visual_content_signal_base ± noise
- conversion_efficiency_raw ← transaction_conversion_signal_base ± noise
- platform_fit_raw ← platform_fit_score_base ± noise
- dense_slice_confidence_raw ← dense_slice_confidence_base ± noise

---

### Rule 4: Hero vs Weak differentiation

#### Hero vendors
- high visual_score
- high platform_fit_raw
- high repeat rate
- high niche_signal_raw

#### Moderate vendors
- mid-range signals

#### Weak vendors
- lower niche clarity
- lower repeat rate
- lower platform fit
- more variability

---

### Rule 5: Platform consistency

If:
- primary_platform_prediction = Instagram

Then:
- platform_fit_raw should be high
- visual_score should generally be higher
- engagement_to_conversion_ratio should reflect content-driven model

---

## Value Ranges

| Field | Range |
|------|------|
| customer_repeat_rate | 0.00 to 1.00 |
| product_niche_fit_score | 0.00 to 1.00 |
| visual_score | 0.00 to 1.00 |
| conversion_efficiency_raw | 0.00 to 1.00 |
| platform_fit_raw | 0.00 to 1.00 |
| dense_slice_confidence_raw | 0.00 to 1.00 |
| avg_order_value_estimate | 8.00 to 220.00 typical |
| monthly_revenue_estimate | 500 to 120000 typical |

---

## Example Row

| Column | Value |
|--------|------|
| vendor_id | 1001 |
| shop_name | GlowSkin Co |
| primary_category | Beauty |
| created_at | 2023-06-15 10:00:00 |
| customer_repeat_rate | 0.76 |
| product_niche_fit_score | 0.84 |
| predicted_micro_niche_1 | Skincare_Enthusiasts |
| predicted_micro_niche_2 | Organic_Beauty |
| niche_signal_raw | 0.82 |
| visual_score | 0.91 |
| conversion_efficiency_raw | 0.52 |
| engagement_to_conversion_ratio | 2.40 |
| content_consistency_score | 0.78 |
| primary_platform_prediction | Instagram |
| secondary_platform_prediction | TikTok |
| platform_fit_raw | 0.88 |
| platform_dependency_score | 0.67 |
| dense_slice_prediction_1 | Urban_Female_20_30 |
| dense_slice_prediction_2 | Young_Professionals |
| geo_cluster_type | Urban |
| dense_slice_confidence_raw | 0.81 |
| avg_order_value_estimate | 42.50 |
| monthly_revenue_estimate | 18500 |
| returning_customer_revenue_ratio | 0.64 |
| product_category_depth_score | 0.72 |

---

## Layer Connections

### Input
- vendor_master
- transactions

### Output feeds into
- shopify_staging_pipeline
- canonical merge layer

---

## Summary

- Represents Shopify-style summarized business signals
- Derived from vendor truth + transaction behavior
- Not raw truth, but structured source system output
- Critical for platform, niche, and content signals