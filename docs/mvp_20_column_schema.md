# MVP 20-Column Canonical Schema

## Purpose

This is the final canonical dataset for the MVP of the Commerce Intelligence Platform.

It is designed to:
- Stay source-agnostic (Shopify + Square both feed into it)
- Solve 3 core business problems:
  1. Best Micro-Niches
  2. Best Platforms
  3. Best Dense Slices
- Be compact (20 columns) but powerful
- Expand later into the 100-column system

---

# A. 5 Mandatory Backbone Columns

| Column Name | Type | Allowed Values | Description |
|------------|------|----------------|------------|
| business_id | INTEGER | Positive integer (1001+) | Unique business identifier |
| business_name | TEXT | Free text | Business name |
| business_category | CATEGORICAL | Beauty, Fitness, Fashion, Food, Home, Wellness, Pets, Tech Accessories, Crafts, Education, Other | Business type |
| event_timestamp | DATETIME | Valid UTC timestamp | Latest data timestamp |
| data_source_coverage | CATEGORICAL | Shopify_only, Square_only, Shopify_and_Square, Unknown | Data source availability |

---

# B. Problem 1: Best Micro-Niches (5 Columns)

| Column Name | Type | Allowed Values | Description |
|------------|------|----------------|------------|
| top_micro_niche_1 | CATEGORICAL | Gen_Z_Beauty, Budget_Shoppers, Skincare_Beginners, Premium_Beauty_Buyers, Local_Wellness_Seekers, Fitness_Professionals, Convenience_Buyers, Gift_Buyers, Students, Young_Professionals, Parents, Other | Primary niche |
| top_micro_niche_2 | CATEGORICAL | Same as above + None | Secondary niche |
| niche_signal_score | FLOAT | 0.00 - 1.00 | Strength of niche signal |
| repeat_customer_signal | FLOAT | 0.00 - 1.00 | Repeat purchase behavior |
| product_category_affinity | CATEGORICAL | Very_Low, Low, Medium, High, Very_High | Product-niche fit |

---

# C. Problem 2: Best Platforms (5 Columns)

| Column Name | Type | Allowed Values | Description |
|------------|------|----------------|------------|
| recommended_platform_1 | CATEGORICAL | TikTok, Instagram, Reddit, YouTube_Shorts, Pinterest, Facebook_Groups, Discord, Micro_Influencers, Website_First, Marketplace_First | Primary platform |
| recommended_platform_2 | CATEGORICAL | Same as above + None | Secondary platform |
| platform_fit_score | FLOAT | 0.00 - 1.00 | Platform fit strength |
| visual_content_signal | FLOAT | 0.00 - 1.00 | Visual appeal score |
| transaction_conversion_signal | FLOAT | 0.00 - 1.00 | Conversion efficiency |

---

# D. Problem 3: Best Dense Slices (5 Columns)

| Column Name | Type | Allowed Values | Description |
|------------|------|----------------|------------|
| recommended_dense_slice_1 | CATEGORICAL | Bay_Area_Young_Professionals, College_Campus_Students, Downtown_Fitness_Community, Local_Beauty_Enthusiasts, Suburban_Parents, Wellness_Seekers, Budget_Shopping_Clusters, Boutique_Shoppers, Office_Workers, Neighborhood_Repeat_Customers, Other | Primary dense slice |
| recommended_dense_slice_2 | CATEGORICAL | Same as above + None | Secondary dense slice |
| geography_signal | CATEGORICAL | Hyper_Local, Local, Regional, National, Mixed, Unknown | Geographic pattern |
| payment_locality_signal | FLOAT | 0.00 - 1.00 | Local payment strength |
| dense_slice_confidence | FLOAT | 0.00 - 1.00 | Confidence score |

---

# Score Interpretation (All FLOAT columns)

| Range | Meaning |
|------|--------|
| 0.00 - 0.30 | Weak |
| 0.31 - 0.50 | Low |
| 0.51 - 0.70 | Moderate |
| 0.71 - 0.85 | Strong |
| 0.86 - 1.00 | Very Strong |

---

# Key Design Rules

- All score columns use 0.00 to 1.00 scale
- All categorical fields use controlled values (no free text except business_name)
- Final table is source-agnostic (NOT Shopify vs Square split)
- Shopify + Square both feed into same columns
- This is the SOURCE OF TRUTH for MVP schema

---

# Source Contribution Overview

## Shopify contributes mainly to:
- business_name
- business_category
- product_category_affinity
- visual_content_signal
- micro-niche signals

## Square contributes mainly to:
- repeat_customer_signal
- payment_locality_signal

## Both contribute to:
- transaction_conversion_signal
- geography_signal
- event_timestamp

## Derived in system:
- platform recommendations
- niche scoring
- dense slice recommendations
- confidence scores

---

# Next Steps

1. Create mapping files:
   - config/mappings/shopify_to_mvp_20.json
   - config/mappings/square_to_mvp_20.json

2. Build staging layer
3. Map to canonical table
4. Build API outputs

---

# Final Note

This is the MVP schema.

It is intentionally:
- compact
- decision-focused
- scalable to 100 columns later