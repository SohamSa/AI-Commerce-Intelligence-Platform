# Vendor Master Schema Blueprint

## Purpose

One row = one vendor

Total rows:
- 2,000

This table represents the **core truth layer** of the system.  
All other datasets (transactions, Shopify raw, Square raw, canonical) are derived from this table.

---

## Table: vendor_master

---

## A. Identity Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| vendor_id | INTEGER | Unique integer | 1001 | Primary key |
| business_name | VARCHAR(150) | Free text | GlowSkin Co | Vendor name |
| business_category | CATEGORICAL | Beauty, Fitness, Fashion, Food, Home, Wellness, Pets, Tech_Accessories, Crafts, Education | Beauty | Business category |
| business_stage | CATEGORICAL | Prototype, Launch, Early_Traction, Revenue_Validation, Growth_Mode, Repeat_Demand, Channel_Fit, Local_Dominance, Scale_Ready, Mature_Niche | Growth_Mode | Business maturity stage |

---

## B. Audience and Positioning Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| top_micro_niche_1 | CATEGORICAL | Skincare_Enthusiasts, Budget_Shoppers, Gym_Beginners, Young_Professionals, Parents, Students, Pet_Owners, Home_Decor_Lovers, Makers_Creators, Lifelong_Learners | Skincare_Enthusiasts | Primary niche |
| top_micro_niche_2 | CATEGORICAL | None, Organic_Beauty, Home_Workout, Deal_Hunters, Career_Builders, Busy_Parents, College_Students, Eco_Conscious_Buyers, Hobby_Crafters, Upskillers | Organic_Beauty | Secondary niche |
| recommended_platform_1 | CATEGORICAL | Instagram, TikTok, YouTube_Shorts, Pinterest, Reddit, Facebook_Groups, Discord, Website_First, Marketplace_First, Micro_Influencers | Instagram | Primary platform |
| recommended_platform_2 | CATEGORICAL | None, Instagram, TikTok, YouTube_Shorts, Pinterest, Reddit, Facebook_Groups, Discord, Website_First, Marketplace_First | TikTok | Secondary platform |
| recommended_dense_slice_1 | CATEGORICAL | Urban_Female_20_30, Male_18_35_Fitness, Suburban_Families, College_Students, Budget_Households, Young_Professionals, Pet_Owner_Communities, Home_Decor_Clusters, Local_Wellness_Seekers, Upskilling_Professionals | Urban_Female_20_30 | Target dense slice |
| geography_signal | CATEGORICAL | Urban, Suburban, Mixed, College_Town, Downtown_CBD, Regional_Hub, Neighborhood_Local, National_Distributed, Wellness_Corridor, Family_Suburb_Belt | Urban | Geographic pattern |

---

## C. Structural & Behavioral Columns

| Column Name | Type | Allowed Values | Example | Description |
|------------|------|----------------|--------|-------------|
| product_affinity_bucket | CATEGORICAL | Very_Low, Low, Low_Medium, Medium, Medium_High, High, Very_High, Premium_Fit, Trend_Fit, Utility_Fit | Very_High | Product demand alignment |
| acquisition_channel_dominance | CATEGORICAL | Organic_Social, Paid_Social, Referral, Search, Marketplace, Direct, Community, Email_CRM, Influencer, Offline_to_Online | Organic_Social | Acquisition type |
| vendor_strength_class | CATEGORICAL | Hero, Moderate, Weak | Hero | Vendor strength |
| transaction_tier | CATEGORICAL | Tier_A_Power, Tier_B_Growth, Tier_C_Steady, Tier_D_Small | Tier_A_Power | Transaction scale |

---

## D. Quantitative Baseline Columns

| Column Name | Type | Range | Example | Description |
|------------|------|--------|--------|-------------|
| repeat_customer_signal_base | FLOAT | 0.00 to 0.95 | 0.78 | Repeat behavior baseline |
| niche_signal_score_base | FLOAT | 0.05 to 0.95 | 0.84 | Niche clarity |
| visual_content_signal_base | FLOAT | 0.05 to 0.98 | 0.91 | Content strength |
| transaction_conversion_signal_base | FLOAT | 0.02 to 0.85 | 0.52 | Conversion efficiency |
| platform_fit_score_base | FLOAT | 0.05 to 0.95 | 0.88 | Platform alignment |
| dense_slice_confidence_base | FLOAT | 0.05 to 0.95 | 0.81 | Dense slice confidence |
| avg_order_value_usd_base | FLOAT | 8.00 to 220.00 | 42.50 | Average order value |
| monthly_revenue_usd_base | FLOAT | 500 to 120000 | 18500 | Monthly revenue |
| customer_ltv_proxy_usd_base | FLOAT | 20 to 1500 | 210 | Customer lifetime value |
| target_transaction_count | INTEGER | Tier-based | 430 | Target transactions |

---

## Distribution Rules

### Vendor Strength

| Class | Count |
|------|------|
| Hero | 600 |
| Moderate | 900 |
| Weak | 500 |

---

### Transaction Tiers

| Tier | Vendors | Total Transactions |
|------|--------|-------------------|
| Tier_A_Power | 200 | 87,500 |
| Tier_B_Growth | 500 | 87,500 |
| Tier_C_Steady | 800 | 56,250 |
| Tier_D_Small | 500 | 18,750 |

Total:
- Vendors = 2,000
- Transactions = 250,000

---

## Generation Rules

### Rule 1: Assign categorical columns first

Order:
1. business_category  
2. business_stage  
3. top_micro_niche_1  
4. top_micro_niche_2  
5. recommended_platform_1  
6. recommended_platform_2  
7. recommended_dense_slice_1  
8. geography_signal  
9. product_affinity_bucket  
10. acquisition_channel_dominance  
11. vendor_strength_class  
12. transaction_tier  

---

### Rule 2: Quantitative values are conditional

Examples:

Strong (Hero):
- Higher repeat
- Higher niche score
- Higher platform fit

Weak:
- Lower niche clarity
- Lower repeat
- Lower conversion

---

### Rule 3: Transactions per tier

| Tier | Range per Vendor |
|------|----------------|
| Tier_A_Power | 320 to 650 |
| Tier_B_Growth | 120 to 260 |
| Tier_C_Steady | 40 to 95 |
| Tier_D_Small | 15 to 55 |

---

### Rule 4: Strength impacts metrics

Hero:
- High repeat
- High conversion
- Strong niche

Moderate:
- Mixed signals

Weak:
- Low repeat
- Weak niche
- Poor conversion

---

## Example Row

| Column | Value |
|--------|------|
| vendor_id | 1001 |
| business_name | GlowSkin Co |
| business_category | Beauty |
| business_stage | Growth_Mode |
| top_micro_niche_1 | Skincare_Enthusiasts |
| top_micro_niche_2 | Organic_Beauty |
| recommended_platform_1 | Instagram |
| recommended_platform_2 | TikTok |
| recommended_dense_slice_1 | Urban_Female_20_30 |
| geography_signal | Urban |
| product_affinity_bucket | Very_High |
| acquisition_channel_dominance | Organic_Social |
| vendor_strength_class | Hero |
| transaction_tier | Tier_A_Power |
| repeat_customer_signal_base | 0.78 |
| niche_signal_score_base | 0.84 |
| visual_content_signal_base | 0.91 |
| transaction_conversion_signal_base | 0.52 |
| platform_fit_score_base | 0.88 |
| dense_slice_confidence_base | 0.81 |
| avg_order_value_usd_base | 42.50 |
| monthly_revenue_usd_base | 18500 |
| customer_ltv_proxy_usd_base | 210 |
| target_transaction_count | 430 |

---

## Layer Connections

### Drives Transactions
- vendor_id
- transaction_tier
- repeat_customer_signal_base
- avg_order_value_usd_base
- geography_signal

### Drives Shopify Raw
- business_name
- niche signals
- platform signals
- visual signals

### Drives Square Raw
- transaction behavior
- locality signals
- conversion signals

---

## Summary

- This is the **single source of truth**
- Everything else is derived from this table
- Must be frozen before coding