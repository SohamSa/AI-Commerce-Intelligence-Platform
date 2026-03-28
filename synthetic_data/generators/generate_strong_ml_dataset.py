import os
import random
from typing import Dict, List

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

OUTPUT_FILE = "synthetic_data/generated/strong_ml_dataset.csv"
N_ROWS = 5000

BUSINESS_CATEGORIES = [
    "Beauty",
    "Crafts",
    "Education",
    "Fashion",
    "Fitness",
    "Food",
    "Home",
    "Pets",
    "Tech_Accessories",
    "Wellness",
]

MICRO_NICHES = [
    "Gym_Beginners",
    "Pet_Lovers",
    "Organic_Beauty",
    "Gadget_Geeks",
    "Home_Decor_Lovers",
    "Streetwear_Fans",
    "Online_Learners",
    "Healthy_Eating",
    "DIY_Crafters",
    "Skincare_Enthusiasts",
]

PLATFORMS = [
    "TikTok",
    "Website_First",
    "Micro_Influencers",
    "Pinterest",
    "Discord",
    "Facebook_Groups",
    "Reddit",
    "Instagram",
    "YouTube_Shorts",
    "Marketplace_First",
]

DENSE_SLICES = [
    "Budget_Shoppers",
    "College_Students",
    "DIY_Creators",
    "Fitness_Enthusiasts",
    "Luxury_Buyers",
    "Pet_Owners",
    "Suburban_Families",
    "Tech_Early_Adopters",
    "Urban_Female_20_30",
    "Young_Professionals",
]

GEOGRAPHIES = [
    "Urban",
    "Suburban",
    "Regional_Hub",
    "Neighborhood_Local",
    "National_Distributed",
    "Family_Suburb_Belt",
    "Wellness_Corridor",
    "Mixed",
]

PRICE_RANGES = ["Low", "Mid", "Premium"]
CONTENT_FORMATS = ["Video_First", "Image_First", "Text_First", "Mixed"]
PURCHASE_FREQUENCIES = ["Low", "Medium", "High"]
DATA_SOURCE_COVERAGE = ["shopify_only", "square_only", "shopify_and_square"]


CATEGORY_TO_NICHE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "Beauty": {
        "Organic_Beauty": 0.23,
        "Skincare_Enthusiasts": 0.23,
        "Healthy_Eating": 0.08,
        "Home_Decor_Lovers": 0.08,
        "Streetwear_Fans": 0.07,
        "Gym_Beginners": 0.07,
        "DIY_Crafters": 0.07,
        "Pet_Lovers": 0.05,
        "Online_Learners": 0.07,
        "Gadget_Geeks": 0.05,
    },
    "Crafts": {
        "DIY_Crafters": 0.25,
        "Home_Decor_Lovers": 0.18,
        "Online_Learners": 0.10,
        "Organic_Beauty": 0.07,
        "Streetwear_Fans": 0.07,
        "Pet_Lovers": 0.07,
        "Gadget_Geeks": 0.06,
        "Healthy_Eating": 0.06,
        "Skincare_Enthusiasts": 0.06,
        "Gym_Beginners": 0.08,
    },
    "Education": {
        "Online_Learners": 0.27,
        "DIY_Crafters": 0.11,
        "Gadget_Geeks": 0.11,
        "Healthy_Eating": 0.08,
        "Gym_Beginners": 0.08,
        "Streetwear_Fans": 0.06,
        "Pet_Lovers": 0.06,
        "Home_Decor_Lovers": 0.06,
        "Organic_Beauty": 0.08,
        "Skincare_Enthusiasts": 0.09,
    },
    "Fashion": {
        "Streetwear_Fans": 0.25,
        "Organic_Beauty": 0.10,
        "Skincare_Enthusiasts": 0.09,
        "Home_Decor_Lovers": 0.08,
        "Gym_Beginners": 0.08,
        "Gadget_Geeks": 0.08,
        "Healthy_Eating": 0.07,
        "DIY_Crafters": 0.07,
        "Pet_Lovers": 0.07,
        "Online_Learners": 0.11,
    },
    "Fitness": {
        "Gym_Beginners": 0.26,
        "Healthy_Eating": 0.18,
        "Streetwear_Fans": 0.09,
        "Online_Learners": 0.08,
        "Skincare_Enthusiasts": 0.07,
        "Organic_Beauty": 0.06,
        "Pet_Lovers": 0.06,
        "DIY_Crafters": 0.06,
        "Gadget_Geeks": 0.07,
        "Home_Decor_Lovers": 0.07,
    },
    "Food": {
        "Healthy_Eating": 0.26,
        "Gym_Beginners": 0.14,
        "Online_Learners": 0.09,
        "Pet_Lovers": 0.08,
        "Organic_Beauty": 0.07,
        "DIY_Crafters": 0.07,
        "Home_Decor_Lovers": 0.07,
        "Streetwear_Fans": 0.07,
        "Gadget_Geeks": 0.07,
        "Skincare_Enthusiasts": 0.08,
    },
    "Home": {
        "Home_Decor_Lovers": 0.26,
        "DIY_Crafters": 0.18,
        "Pet_Lovers": 0.09,
        "Organic_Beauty": 0.07,
        "Skincare_Enthusiasts": 0.06,
        "Streetwear_Fans": 0.06,
        "Healthy_Eating": 0.08,
        "Gym_Beginners": 0.06,
        "Online_Learners": 0.07,
        "Gadget_Geeks": 0.07,
    },
    "Pets": {
        "Pet_Lovers": 0.30,
        "Home_Decor_Lovers": 0.10,
        "Healthy_Eating": 0.09,
        "Online_Learners": 0.08,
        "DIY_Crafters": 0.08,
        "Gym_Beginners": 0.07,
        "Organic_Beauty": 0.06,
        "Streetwear_Fans": 0.06,
        "Skincare_Enthusiasts": 0.06,
        "Gadget_Geeks": 0.10,
    },
    "Tech_Accessories": {
        "Gadget_Geeks": 0.30,
        "Online_Learners": 0.13,
        "Streetwear_Fans": 0.10,
        "Gym_Beginners": 0.07,
        "DIY_Crafters": 0.07,
        "Home_Decor_Lovers": 0.06,
        "Pet_Lovers": 0.06,
        "Healthy_Eating": 0.06,
        "Organic_Beauty": 0.06,
        "Skincare_Enthusiasts": 0.09,
    },
    "Wellness": {
        "Healthy_Eating": 0.17,
        "Organic_Beauty": 0.14,
        "Skincare_Enthusiasts": 0.14,
        "Gym_Beginners": 0.14,
        "Online_Learners": 0.10,
        "Pet_Lovers": 0.07,
        "Home_Decor_Lovers": 0.07,
        "DIY_Crafters": 0.06,
        "Gadget_Geeks": 0.05,
        "Streetwear_Fans": 0.06,
    },
}


def clamp(x: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, x))


def noisy(value: float, sd: float = 0.08) -> float:
    return clamp(np.random.normal(value, sd))


def weighted_choice(weight_map: Dict[str, float]) -> str:
    items = list(weight_map.keys())
    weights = list(weight_map.values())
    return random.choices(items, weights=weights, k=1)[0]


def softmax_sample(score_map: Dict[str, float], temperature: float = 0.65) -> str:
    labels = list(score_map.keys())
    raw_scores = np.array([score_map[k] for k in labels], dtype=float)

    scaled = raw_scores / temperature
    scaled = scaled - np.max(scaled)
    probs = np.exp(scaled)
    probs = probs / probs.sum()

    return np.random.choice(labels, p=probs)


def rank_top_two(score_map: Dict[str, float]) -> List[str]:
    ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)
    return [ranked[0][0], ranked[1][0]]


def choose_base_niche(category: str) -> str:
    return weighted_choice(CATEGORY_TO_NICHE_WEIGHTS[category])


def create_hidden_factors(category: str, niche_seed: str) -> Dict[str, float]:
    factors = {
        "creator_instinct_hidden": noisy(0.50, 0.18),
        "community_gravity_hidden": noisy(0.50, 0.18),
        "search_discipline_hidden": noisy(0.50, 0.18),
        "premium_identity_hidden": noisy(0.50, 0.18),
        "identity_expression_hidden": noisy(0.50, 0.18),
        "local_habit_hidden": noisy(0.50, 0.18),
        "pet_affinity_hidden": np.random.uniform(0.0, 1.0),
        "trend_hidden": np.random.uniform(0.0, 1.0),
        "research_hidden": np.random.uniform(0.0, 1.0)
    }

    if niche_seed in ["Streetwear_Fans", "Gym_Beginners"]:
        factors["creator_instinct_hidden"] = noisy(0.78, 0.10)
        factors["identity_expression_hidden"] = noisy(0.76, 0.10)

    if niche_seed in ["DIY_Crafters", "Pet_Lovers"]:
        factors["community_gravity_hidden"] = noisy(0.78, 0.10)

    if niche_seed in ["Gadget_Geeks", "Online_Learners", "Home_Decor_Lovers"]:
        factors["search_discipline_hidden"] = noisy(0.76, 0.10)

    if niche_seed in ["Organic_Beauty", "Skincare_Enthusiasts", "Home_Decor_Lovers"]:
        factors["premium_identity_hidden"] = noisy(0.75, 0.10)

    if category in ["Pets", "Food", "Home"]:
        factors["local_habit_hidden"] = noisy(0.72, 0.12)

    return factors


def create_base_profile(category: str, niche_seed: str) -> Dict[str, float]:
    profile = {
        "is_visual_product": 0.50,
        "is_utility_product": 0.50,
        "brand_loyalty_score": 0.50,
        "impulse_buy_score": 0.50,
        "research_time_score": 0.50,
        "video_consumption_score": 0.50,
        "image_engagement_score": 0.50,
        "text_engagement_score": 0.50,
        "ugc_score": 0.50,
        "influencer_dependency_score": 0.50,
        "repeat_purchase_rate": 0.50,
        "price_sensitivity_score": 0.50,
        "premium_affinity_score": 0.50,
        "trend_sensitivity_score": 0.50,
        "community_engagement_score": 0.50,
        "local_discovery_score": 0.50,
        "education_content_affinity": 0.50,
        "short_form_video_affinity": 0.50,
        "search_intent_score": 0.50,
        "conversion_readiness_score": 0.50,
        "ingredient_awareness_score": 0.50,
        "routine_complexity_score": 0.50,
        "platform_fit_score": 0.50
    }

    category_adj = {
        "Beauty": {"is_visual_product": 0.75, "image_engagement_score": 0.76, "premium_affinity_score": 0.64},
        "Crafts": {"ugc_score": 0.72, "education_content_affinity": 0.68, "community_engagement_score": 0.65},
        "Education": {"text_engagement_score": 0.72, "research_time_score": 0.74, "education_content_affinity": 0.82},
        "Fashion": {"is_visual_product": 0.78, "trend_sensitivity_score": 0.78, "image_engagement_score": 0.76},
        "Fitness": {"short_form_video_affinity": 0.70, "video_consumption_score": 0.74, "conversion_readiness_score": 0.66},
        "Food": {"impulse_buy_score": 0.68, "ugc_score": 0.66, "repeat_purchase_rate": 0.65},
        "Home": {"search_intent_score": 0.68, "image_engagement_score": 0.72, "research_time_score": 0.64},
        "Pets": {"brand_loyalty_score": 0.70, "repeat_purchase_rate": 0.72, "community_engagement_score": 0.68},
        "Tech_Accessories": {"research_time_score": 0.78, "search_intent_score": 0.72, "is_utility_product": 0.72},
        "Wellness": {"brand_loyalty_score": 0.66, "education_content_affinity": 0.70, "premium_affinity_score": 0.60},
    }

    niche_adj = {
        "Gym_Beginners": {"short_form_video_affinity": 0.76, "video_consumption_score": 0.74, "conversion_readiness_score": 0.64},
        "Pet_Lovers": {"brand_loyalty_score": 0.78, "repeat_purchase_rate": 0.76, "community_engagement_score": 0.72},
        "Organic_Beauty": {
            "premium_affinity_score": 0.74,
            "research_time_score": 0.66,
            "image_engagement_score": 0.72,
            "ingredient_awareness_score": 0.72,
            "routine_complexity_score": 0.52,
        },
        "Gadget_Geeks": {"research_time_score": 0.80, "search_intent_score": 0.76, "text_engagement_score": 0.66},
        "Home_Decor_Lovers": {
            "image_engagement_score": 0.87,
            "local_discovery_score": 0.68,
            "text_engagement_score": 0.22,
        },
        "Streetwear_Fans": {
            "short_form_video_affinity": 0.85,
            "image_engagement_score": 0.72,
            "trend_sensitivity_score": 0.88,
            "text_engagement_score": 0.25,
        },
        "Online_Learners": {
            "text_engagement_score": 0.82,
            "education_content_affinity": 0.88,
            "short_form_video_affinity": 0.25,
        },
        "Healthy_Eating": {"education_content_affinity": 0.70, "repeat_purchase_rate": 0.68, "brand_loyalty_score": 0.64},
        "DIY_Crafters": {"ugc_score": 0.80, "community_engagement_score": 0.72, "education_content_affinity": 0.74},
        "Skincare_Enthusiasts": {
            "image_engagement_score": 0.74,
            "research_time_score": 0.68,
            "premium_affinity_score": 0.70,
            "ingredient_awareness_score": 0.86,
            "routine_complexity_score": 0.82,
        }
    }

    for k, v in category_adj[category].items():
        profile[k] = v
    for k, v in niche_adj[niche_seed].items():
        profile[k] = v

    return {k: noisy(v, 0.09) for k, v in profile.items()}


def generate_demographics(category: str, niche_seed: str) -> Dict[str, float]:
    age_18_24 = 0.22
    age_25_34 = 0.30
    age_35_50 = 0.30
    age_50_plus = 0.18

    female_ratio = 0.50
    male_ratio = 0.50

    income_low = 0.28
    income_mid = 0.44
    income_high = 0.28

    if niche_seed in ["Streetwear_Fans", "Gym_Beginners"]:
        age_18_24 = 0.30
        age_25_34 = 0.36
        age_35_50 = 0.22
        age_50_plus = 0.12

    if niche_seed in ["Organic_Beauty", "Skincare_Enthusiasts", "Home_Decor_Lovers"]:
        female_ratio = 0.66
        male_ratio = 0.34

    if niche_seed == "Gadget_Geeks":
        female_ratio = 0.34
        male_ratio = 0.66

    if niche_seed in ["Organic_Beauty", "Home_Decor_Lovers", "Skincare_Enthusiasts"]:
        income_high = 0.34
        income_mid = 0.42
        income_low = 0.24

    if niche_seed in ["DIY_Crafters", "Online_Learners"]:
        age_35_50 += 0.05
        age_50_plus += 0.03

    ages = np.array([age_18_24, age_25_34, age_35_50, age_50_plus], dtype=float)
    ages = ages / ages.sum()

    incomes = np.array([income_low, income_mid, income_high], dtype=float)
    incomes = incomes / incomes.sum()

    return {
        "age_18_24_ratio": noisy(ages[0], 0.04),
        "age_25_34_ratio": noisy(ages[1], 0.04),
        "age_35_50_ratio": noisy(ages[2], 0.04),
        "age_50_plus_ratio": noisy(ages[3], 0.04),
        "female_ratio": noisy(female_ratio, 0.05),
        "male_ratio": noisy(male_ratio, 0.05),
        "income_low_ratio": noisy(incomes[0], 0.04),
        "income_mid_ratio": noisy(incomes[1], 0.04),
        "income_high_ratio": noisy(incomes[2], 0.04),
    }


def choose_dense_slice(features: Dict[str, float], hidden: Dict[str, float]) -> Dict[str, float]:
    scores = {k: 0.0 for k in DENSE_SLICES}

    scores["College_Students"] += (
        0.45 * features["age_18_24_ratio"]
        + 0.28 * features["price_sensitivity_score"]
        + 0.22 * features["short_form_video_affinity"]
        - 0.18 * features["income_high_ratio"]
        + 0.70 * features["dense_anchor_college"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Young_Professionals"] += (
        0.42 * features["age_25_34_ratio"]
        + 0.30 * features["conversion_readiness_score"]
        + 0.24 * features["income_mid_ratio"]
        - 0.24 * features["age_18_24_ratio"]
        + 0.80 * features["dense_anchor_young_professional"]
        + np.random.uniform(-0.06, 0.06)
    )

    scores["Luxury_Buyers"] += (
        0.46 * features["income_high_ratio"]
        + 0.36 * features["premium_affinity_score"]
        - 0.30 * features["price_sensitivity_score"]
        + 0.95 * features["dense_anchor_luxury"]
        + np.random.uniform(-0.06, 0.06)
    )

    scores["Fitness_Enthusiasts"] += (
        0.34 * features["short_form_video_affinity"]
        + 0.30 * features["video_consumption_score"]
        + 0.26 * features["trend_sensitivity_score"]
        - 0.12 * features["income_high_ratio"]
        + 0.70 * features["dense_anchor_fitness"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Pet_Owners"] += (
         0.28 * features["community_engagement_score"]
        - 0.05 * features["ugc_score"] 
        + 0.22 * features["repeat_purchase_rate"]
        - 0.10 * features["search_intent_score"]
        + 0.70 * features["dense_anchor_pet"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Suburban_Families"] += (
        0.30 * features["local_discovery_score"]
        + 0.28 * features["repeat_purchase_rate"]
        + 0.24 * features["age_35_50_ratio"]
        - 0.18 * features["age_18_24_ratio"]
        + 0.70 * features["dense_anchor_suburban"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Tech_Early_Adopters"] += (
         0.30 * features["research_time_score"]
        - 0.05 * features["search_intent_score"]
        + 0.24 * features["trend_sensitivity_score"]
        - 0.12 * features["price_sensitivity_score"]
        + 0.70 * features["dense_anchor_tech"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Urban_Female_20_30"] += (
        0.34 * features["female_ratio"]
        + 0.28 * features["age_25_34_ratio"]
        + 0.22 * features["image_engagement_score"]
        - 0.12 * features["age_35_50_ratio"]
        + 0.70 * features["dense_anchor_urban_female"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Budget_Shoppers"] += (
        0.42 * features["price_sensitivity_score"]
        + 0.30 * features["income_low_ratio"]
        - 0.20 * features["premium_affinity_score"]
        + 0.70 * features["dense_anchor_budget"]
        + np.random.uniform(-0.02, 0.02)
    )
    
    scores["DIY_Creators"] += (
        0.32 * features["ugc_score"]
        + 0.22 * features["education_content_affinity"]
        + 0.18 * hidden["community_gravity_hidden"]
        + np.random.uniform(-0.06, 0.06)
    )

    return scores


def choose_platform(features: Dict[str, float], hidden: Dict[str, float], dense_slice: str) -> Dict[str, float]:
    scores = {k: 0.0 for k in PLATFORMS}

    scores["TikTok"] += (
        0.58 * features["short_form_video_affinity"]
        + 0.46 * features["trend_sensitivity_score"]
        + 0.38 * features["impulse_buy_score"]
        - 0.22 * features["research_time_score"]
        + 0.40 * features["platform_anchor_tiktok"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Instagram"] += (
        0.62 * features["image_engagement_score"]
        + 0.42 * features["influencer_dependency_score"]
        + 0.22 * hidden["identity_expression_hidden"]
        + 0.18 * features["female_ratio"]
        + 0.42 * features["platform_anchor_instagram"]
        - 0.18 * features["text_engagement_score"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Pinterest"] += (
        0.64 * features["is_visual_product"]
        + 0.44 * features["image_engagement_score"]
        + 0.36 * features["search_intent_score"]
        + 0.20 * hidden["premium_identity_hidden"]
        + 0.42 * features["platform_anchor_pinterest"]
        - 0.18 * features["text_engagement_score"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["YouTube_Shorts"] += (
        0.62 * features["video_consumption_score"]
        + 0.50 * features["short_form_video_affinity"]
        + 0.30 * features["education_content_affinity"]
        + 0.42 * features["platform_anchor_youtube_shorts"]
        - 0.14 * features["text_engagement_score"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Website_First"] += (
        0.70 * features["conversion_readiness_score"]
        + 0.54 * features["search_intent_score"]
        + 0.30 * features["repeat_purchase_rate"]
        + 0.42 * features["platform_anchor_website_first"]
        - 0.18 * features["trend_sensitivity_score"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Marketplace_First"] += (
        0.66 * features["conversion_readiness_score"]
        + 0.46 * features["price_sensitivity_score"]
        + 0.30 * features["repeat_purchase_rate"]
        + 0.42 * features["platform_anchor_marketplace_first"]
        - 0.16 * features["brand_loyalty_score"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Facebook_Groups"] += (
        0.62 * features["community_engagement_score"]
        + 0.46 * features["local_discovery_score"]
        + 0.28 * features["repeat_purchase_rate"]
        + 0.42 * features["platform_anchor_facebook_groups"]
        - 0.16 * features["short_form_video_affinity"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Discord"] += (
        0.60 * features["community_engagement_score"]
        + 0.42 * features["text_engagement_score"]
        + 0.26 * features["video_consumption_score"]
        + 0.42 * features["platform_anchor_discord"]
        - 0.14 * features["search_intent_score"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Reddit"] += (
        0.66 * features["text_engagement_score"]
        + 0.58 * features["research_time_score"]
        + 0.28 * features["education_content_affinity"]
        + 0.42 * features["platform_anchor_reddit"]
        - 0.24 * features["impulse_buy_score"]
        - 0.20 * features["short_form_video_affinity"]
        + np.random.uniform(-0.03, 0.03)
    )

    scores["Micro_Influencers"] += (
        0.64 * features["ugc_score"]
        + 0.52 * features["influencer_dependency_score"]
        + 0.28 * features["community_engagement_score"]
        + 0.42 * features["platform_anchor_micro_influencers"]
        - 0.18 * features["search_intent_score"]
        + np.random.uniform(-0.03, 0.03)
    )

    if dense_slice == "College_Students":
        scores["TikTok"] += 0.06
        scores["Instagram"] += 0.05

    if dense_slice == "Luxury_Buyers":
        scores["Instagram"] += 0.05
        scores["Micro_Influencers"] += 0.05
        scores["Pinterest"] += 0.04

    if dense_slice == "DIY_Creators":
        scores["Pinterest"] += 0.05
        scores["YouTube_Shorts"] += 0.05
        scores["Facebook_Groups"] += 0.03

    if dense_slice == "Tech_Early_Adopters":
        scores["Reddit"] += 0.06
        scores["Website_First"] += 0.05
        scores["Discord"] += 0.03

    return scores


def choose_micro_niche(category: str, features: Dict[str, float], hidden: Dict[str, float], dense_slice: str, platform_primary: str = "") -> Dict[str, float]:
    base = CATEGORY_TO_NICHE_WEIGHTS[category]
    scores = {k: base[k] for k in MICRO_NICHES}

    scores["DIY_Crafters"] += (
        0.60 * features["ugc_score"]
        + 0.50 * features["education_content_affinity"]
        + 0.28 * features["community_engagement_score"]
        + 0.18 * hidden["community_gravity_hidden"]
        + 0.60 * features["niche_anchor_diy"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Gadget_Geeks"] += (
        0.62 * features["search_intent_score"]
        + 0.52 * features["research_time_score"]
        + 0.30 * features["text_engagement_score"]
        + 0.24 * features["is_utility_product"]
        + 0.60 * features["niche_anchor_gadget"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Gym_Beginners"] += (
        0.60 * features["short_form_video_affinity"]
        + 0.50 * features["video_consumption_score"]
        + 0.28 * features["impulse_buy_score"]
        + 0.20 * features["trend_sensitivity_score"]
        + 0.60 * features["niche_anchor_gym"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Healthy_Eating"] += (
        0.70 * features["repeat_purchase_rate"]
        + 0.60 * features["brand_loyalty_score"]
        + 0.22 * features["research_time_score"]
        + 0.18 * features["premium_affinity_score"]
        + 0.60 * features["niche_anchor_healthy"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Home_Decor_Lovers"] += (
        0.60 * features["image_engagement_score"]
        + 0.48 * features["product_category_affinity"]
        + 0.28 * features["premium_affinity_score"]
        + 0.18 * hidden["identity_expression_hidden"]
        + 0.60 * features["niche_anchor_home"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Online_Learners"] += (
        0.62 * features["education_content_affinity"]
        + 0.48 * features["research_time_score"]
        + 0.26 * features["search_intent_score"]
        + 0.24 * features["text_engagement_score"]
        + 0.18 * hidden["search_discipline_hidden"]
        + 0.60 * features["niche_anchor_learning"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Organic_Beauty"] += (
        0.72 * features["premium_affinity_score"]
        + 0.58 * features["brand_loyalty_score"]
        + 0.48 * features["ingredient_awareness_score"]
        + 0.20 * features["education_content_affinity"]
        - 0.25 * features["routine_complexity_score"]   # reduced
        - 0.10 * features["search_intent_score"]        # reduced
        + 0.60 * features["niche_anchor_organic"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Pet_Lovers"] += (
        0.68 * features["repeat_purchase_rate"]
        + 0.58 * features["community_engagement_score"]
        + 0.34 * features["ugc_score"]
        + 0.18 * features["brand_loyalty_score"]
        + 0.26 * hidden["pet_affinity_hidden"]
        + 0.65 * features["niche_anchor_pet"]
        - 0.60 * features["search_intent_score"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Skincare_Enthusiasts"] += (
        0.60 * features["research_time_score"]
        + 0.50 * features["search_intent_score"]
        + 0.45 * features["routine_complexity_score"]
        + 0.35 * features["ingredient_awareness_score"]
        - 0.20 * features["brand_loyalty_score"]   # 🔥 separation
        + 0.60 * features["niche_anchor_skincare"]
        + np.random.uniform(-0.02, 0.02)
    )

    scores["Streetwear_Fans"] += (
        0.62 * features["trend_sensitivity_score"]
        + 0.50 * features["impulse_buy_score"]
        + 0.26 * features["short_form_video_affinity"]
        + 0.22 * features["image_engagement_score"]
        + 0.18 * hidden["trend_hidden"]
        + 0.60 * features["niche_anchor_streetwear"]
        + np.random.uniform(-0.02, 0.02)
    )
    
    if dense_slice == "Fitness_Enthusiasts":
        scores["Gym_Beginners"] += 0.10
        scores["Healthy_Eating"] += 0.08

    if dense_slice == "DIY_Creators":
        scores["DIY_Crafters"] += 0.10
        scores["Home_Decor_Lovers"] += 0.06

    if dense_slice == "Pet_Owners":
        scores["Pet_Lovers"] += 0.12

    if dense_slice == "Tech_Early_Adopters":
        scores["Gadget_Geeks"] += 0.10
        scores["Online_Learners"] += 0.05

    if dense_slice == "Urban_Female_20_30":
        scores["Skincare_Enthusiasts"] += 0.08
        scores["Organic_Beauty"] += 0.08
        scores["Streetwear_Fans"] += 0.05
        
    if platform_primary == "TikTok":
        scores["Streetwear_Fans"] += 0.08
        scores["Gym_Beginners"] += 0.06

    if platform_primary == "Pinterest":
        scores["Home_Decor_Lovers"] += 0.08
        scores["Organic_Beauty"] += 0.06
        scores["DIY_Crafters"] += 0.05

    if platform_primary == "Instagram":
        scores["Skincare_Enthusiasts"] += 0.06
        scores["Streetwear_Fans"] += 0.06
        scores["Organic_Beauty"] += 0.05

    if platform_primary == "Reddit":
        scores["Gadget_Geeks"] += 0.08
        scores["Online_Learners"] += 0.06

    if platform_primary == "Facebook_Groups":
        scores["Pet_Lovers"] += 0.08
        scores["DIY_Crafters"] += 0.05
        
    scores["DIY_Crafters"] *= 1.08
    scores["Gadget_Geeks"] *= 1.08
    scores["Gym_Beginners"] *= 1.08
    scores["Healthy_Eating"] *= 1.08
    scores["Home_Decor_Lovers"] *= 1.06
    scores["Online_Learners"] *= 1.06
    scores["Organic_Beauty"] *= 1.06
    scores["Pet_Lovers"] *= 1.06
    scores["Skincare_Enthusiasts"] *= 1.06
    scores["Streetwear_Fans"] *= 1.06

    return scores


def choose_secondary_label(primary: str, universe: List[str]) -> str:
    others = [x for x in universe if x != primary]
    return random.choice(others)


def business_name(category: str, idx: int) -> str:
    return f"{category}_Brand_{idx:05d}"


def generate_auxiliary_features(category: str, dense_slice_seed: str, hidden: Dict[str, float], base: Dict[str, float], demo: Dict[str, float]) -> Dict[str, float]:
    geography = random.choice(GEOGRAPHIES)
    data_source = random.choice(DATA_SOURCE_COVERAGE)

    price_range = random.choices(
        PRICE_RANGES,
        weights=[
            0.38 if base["price_sensitivity_score"] > 0.60 else 0.22,
            0.46,
            0.32 if base["premium_affinity_score"] > 0.65 else 0.18,
        ],
        k=1,
    )[0]

    format_scores = {
        "Video_First": base["video_consumption_score"] + base["short_form_video_affinity"] + hidden["creator_instinct_hidden"] * 0.4,
        "Image_First": base["image_engagement_score"] + base["is_visual_product"] + hidden["identity_expression_hidden"] * 0.3,
        "Text_First": base["text_engagement_score"] + base["education_content_affinity"] + hidden["search_discipline_hidden"] * 0.3,
        "Mixed": 1.15 + np.random.uniform(-0.08, 0.08),
    }
    content_format = max(format_scores, key=format_scores.get)

    purchase_frequency = random.choices(
        PURCHASE_FREQUENCIES,
        weights=[
            0.30 if base["repeat_purchase_rate"] < 0.52 else 0.18,
            0.42,
            0.36 if base["repeat_purchase_rate"] > 0.65 else 0.20,
        ],
        k=1,
    )[0]

    foot_traffic_score = noisy(
        0.40
        + 0.16 * hidden["local_habit_hidden"]
        + 0.12 * base["local_discovery_score"]
        + (0.12 if geography in ["Urban", "Regional_Hub"] else 0.0),
        0.10,
    )

    population_density_score = noisy(
        0.68 if geography in ["Urban", "Regional_Hub"] else 0.45 if geography in ["Suburban", "Family_Suburb_Belt"] else 0.35,
        0.10,
    )

    college_presence_score = noisy(
        0.72 if dense_slice_seed == "College_Students" else 0.38,
        0.11,
    )

    competition_density_score = noisy(
        0.42 + 0.20 * base["trend_sensitivity_score"],
        0.12,
    )

    market_saturation_score = noisy(
        0.38 + 0.18 * competition_density_score,
        0.12,
    )

    demand_score = noisy(
        0.40
        + 0.22 * base["conversion_readiness_score"]
        + 0.10 * base["brand_loyalty_score"],
        0.10,
    )

    trend_score = noisy(
        0.36
        + 0.24 * base["trend_sensitivity_score"]
        + 0.12 * hidden["identity_expression_hidden"],
        0.10,
    )

    repeat_customer_signal = noisy(
        0.30 + 0.42 * base["repeat_purchase_rate"] + 0.08 * base["brand_loyalty_score"],
        0.09,
    )

    product_category_affinity = noisy(
        0.26 + 0.24 * base["is_visual_product"] + 0.22 * base["is_utility_product"] + 0.08 * base["search_intent_score"],
        0.09,
    )

    niche_signal_score = noisy(
        0.34
        + 0.14 * base["education_content_affinity"]
        + 0.14 * base["trend_sensitivity_score"]
        + 0.10 * hidden["identity_expression_hidden"]
        + 0.08 * hidden["community_gravity_hidden"],
        0.10,
    )

    visual_content_signal = noisy(
        0.28 + 0.34 * base["image_engagement_score"] + 0.18 * base["video_consumption_score"],
        0.09,
    )

    transaction_conversion_signal = noisy(
        0.30 + 0.34 * base["conversion_readiness_score"] + 0.16 * base["repeat_purchase_rate"],
        0.09,
    )

    platform_fit_score = noisy(
        0.32
        + 0.18 * base["video_consumption_score"]
        + 0.16 * base["image_engagement_score"]
        + 0.12 * base["text_engagement_score"]
        + 0.08 * hidden["creator_instinct_hidden"]
        + 0.08 * hidden["search_discipline_hidden"],
        0.10,
    )

    dense_slice_confidence = noisy(
        0.30
        + 0.18 * demo["age_25_34_ratio"]
        + 0.16 * demo["income_mid_ratio"]
        + 0.12 * foot_traffic_score
        + 0.10 * population_density_score
        + 0.08 * college_presence_score,
        0.10,
    )

    return {
        "price_range": price_range,
        "content_format": content_format,
        "purchase_frequency": purchase_frequency,
        "geography_signal": geography,
        "data_source_coverage": data_source,
        "avg_session_time_minutes": round(np.random.uniform(2.5, 12.0), 2),
        "foot_traffic_score": round(foot_traffic_score, 4),
        "population_density_score": round(population_density_score, 4),
        "college_presence_score": round(college_presence_score, 4),
        "competition_density_score": round(competition_density_score, 4),
        "market_saturation_score": round(market_saturation_score, 4),
        "demand_score": round(demand_score, 4),
        "trend_score": round(trend_score, 4),
        "repeat_customer_signal": round(repeat_customer_signal, 4),
        "product_category_affinity": round(product_category_affinity, 4),
        "niche_signal_score": round(niche_signal_score, 4),
        "visual_content_signal": round(visual_content_signal, 4),
        "transaction_conversion_signal": round(transaction_conversion_signal, 4),
        "platform_fit_score": round(platform_fit_score, 4),
        "dense_slice_confidence": round(dense_slice_confidence, 4)
        
    }


def generate_row(i: int) -> Dict[str, object]:
        
    category = random.choice(BUSINESS_CATEGORIES)
    niche_seed = choose_base_niche(category)

    hidden = create_hidden_factors(category, niche_seed)
    base = create_base_profile(category, niche_seed)
    demo = generate_demographics(category, niche_seed)

    anchor_features = {
        "dense_anchor_college": 0.0,
        "dense_anchor_young_professional": 0.0,
        "dense_anchor_luxury": 0.0,
        "dense_anchor_fitness": 0.0,
        "dense_anchor_pet": 0.0,
        "dense_anchor_suburban": 0.0,
        "dense_anchor_tech": 0.0,
        "dense_anchor_urban_female": 0.0,
        "dense_anchor_budget": 0.0,

        "platform_anchor_tiktok": 0.0,
        "platform_anchor_reddit": 0.0,
        "platform_anchor_instagram": 0.0,
        "platform_anchor_pinterest": 0.0,
        "platform_anchor_website_first": 0.0,
        "platform_anchor_discord": 0.0,
        "platform_anchor_youtube_shorts": 0.0,
        "platform_anchor_micro_influencers": 0.0,
        "platform_anchor_marketplace_first": 0.0,
        "platform_anchor_facebook_groups": 0.0,

        "niche_anchor_skincare": 0.0,
        "niche_anchor_pet": 0.0,
        "niche_anchor_streetwear": 0.0,
        "niche_anchor_learning": 0.0,
        "niche_anchor_home": 0.0,
        "niche_anchor_organic": 0.0,
        "niche_anchor_diy": 0.0,
        "niche_anchor_gadget": 0.0,
        "niche_anchor_gym": 0.0,
        "niche_anchor_healthy": 0.0,
    }
    
    anchor_features["dense_anchor_college"] = (
        0.80 * demo["age_18_24_ratio"]
        + 0.50 * base["price_sensitivity_score"]
        + 0.30 * base["short_form_video_affinity"]
    )

    anchor_features["dense_anchor_young_professional"] = (
        0.75 * demo["age_25_34_ratio"]
        + 0.55 * base["conversion_readiness_score"]
        + 0.35 * demo["income_mid_ratio"]
    )

    anchor_features["dense_anchor_luxury"] = (
        0.80 * demo["income_high_ratio"]
        + 0.65 * base["premium_affinity_score"]
        - 0.35 * base["price_sensitivity_score"]
    )

    anchor_features["dense_anchor_fitness"] = (
        0.70 * base["video_consumption_score"]
        + 0.55 * base["short_form_video_affinity"]
    )

    anchor_features["dense_anchor_pet"] = (
        0.75 * base["ugc_score"]
        + 0.45 * base["community_engagement_score"]
        + 0.35 * base["repeat_purchase_rate"]
    )

    anchor_features["dense_anchor_suburban"] = (
        0.60 * base["local_discovery_score"]
        + 0.55 * base["repeat_purchase_rate"]
        + 0.35 * demo["age_35_50_ratio"]
        + 0.25 * demo["income_mid_ratio"]
    )

    anchor_features["dense_anchor_tech"] = (
        0.75 * base["search_intent_score"]
        + 0.60 * base["research_time_score"]
    )

    anchor_features["dense_anchor_urban_female"] = (
        0.75 * demo["female_ratio"]
        + 0.60 * demo["age_25_34_ratio"]
        + 0.40 * base["image_engagement_score"]
    )

    anchor_features["dense_anchor_budget"] = (
        0.80 * base["price_sensitivity_score"]
        + 0.55 * demo["income_low_ratio"]
    )

     # first get dense slice from fields that already exist
    dense_seed_scores = choose_dense_slice(
        {**base, **demo, **anchor_features},
        hidden
    )
    
    sorted_dense_scores = sorted(dense_seed_scores.items(), key=lambda x: x[1], reverse=True)
    top_dense_label, top_dense_score = sorted_dense_scores[0]
    second_dense_score = sorted_dense_scores[1][1]

    if top_dense_score - second_dense_score > 0.08:
        dense_slice_primary = top_dense_label
    else:
        dense_slice_primary = softmax_sample(dense_seed_scores, temperature=0.28)
    
    dense_slice_top2 = rank_top_two(dense_seed_scores)

    # now aux can be created because dense_slice_primary exists
    aux = generate_auxiliary_features(category, dense_slice_primary, hidden, base, demo)
    
    if niche_seed == "Skincare_Enthusiasts":
        anchor_features["niche_anchor_skincare"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Pet_Lovers":
        anchor_features["niche_anchor_pet"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Streetwear_Fans":
        anchor_features["niche_anchor_streetwear"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Online_Learners":
        anchor_features["niche_anchor_learning"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Home_Decor_Lovers":
        anchor_features["niche_anchor_home"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Organic_Beauty":
        anchor_features["niche_anchor_organic"] = np.random.uniform(0.7, 1.0)
        
    if niche_seed == "DIY_Crafters":
        anchor_features["niche_anchor_diy"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Gadget_Geeks":
        anchor_features["niche_anchor_gadget"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Gym_Beginners":
        anchor_features["niche_anchor_gym"] = np.random.uniform(0.7, 1.0)

    if niche_seed == "Healthy_Eating":
        anchor_features["niche_anchor_healthy"] = np.random.uniform(0.7, 1.0)
        
    for key in anchor_features:
        if anchor_features[key] == 0:
            anchor_features[key] = np.random.uniform(0.0, 0.15)
            
    # =========================
    # PLATFORM ANCHOR VALUES
    # =========================

    anchor_features["platform_anchor_tiktok"] = (
        0.8 * base["short_form_video_affinity"]
        + 0.7 * base["trend_sensitivity_score"]
        + 0.6 * base["impulse_buy_score"]
    )

    anchor_features["platform_anchor_instagram"] = (
        0.8 * base["image_engagement_score"]
        + 0.6 * base["brand_loyalty_score"]
        + 0.5 * base["influencer_dependency_score"]
    )

    anchor_features["platform_anchor_reddit"] = (
        0.85 * base["text_engagement_score"]
        + 0.75 * base["research_time_score"]
        - 0.4 * base["impulse_buy_score"]
    )
    
    
            
    platform_scores = choose_platform(
        {**base, **demo, **aux, **anchor_features},
        hidden,
        dense_slice_primary
    )
    
    sorted_platform_scores = sorted(platform_scores.items(), key=lambda x: x[1], reverse=True)
    top_platform_label, top_platform_score = sorted_platform_scores[0]
    second_platform_score = sorted_platform_scores[1][1]

    if top_platform_score - second_platform_score > 0.12:
        platform_primary = top_platform_label
    else:
        platform_primary = softmax_sample(platform_scores, temperature=0.35)
    
    platform_top2 = rank_top_two(platform_scores)

    niche_scores = choose_micro_niche(
        category,
        {**base, **demo, **aux, **anchor_features},
        hidden,
        dense_slice_primary,
        platform_primary
    )
    sorted_scores = sorted(niche_scores.items(), key=lambda x: x[1], reverse=True)

    top_label, top_score = sorted_scores[0]
    second_score = sorted_scores[1][1]

    if top_score - second_score > 0.18:
        niche_primary = top_label
    else:
        niche_primary = softmax_sample(niche_scores, temperature=0.72)

    niche_top2 = rank_top_two(niche_scores)

    if niche_primary == niche_top2[0]:
        niche_secondary = niche_top2[1]
    else:
        niche_secondary = niche_top2[0]

    if platform_primary == platform_top2[0]:
        platform_secondary = platform_top2[1]
    else:
        platform_secondary = platform_top2[0]

    if dense_slice_primary == dense_slice_top2[0]:
        dense_secondary = dense_slice_top2[1]
    else:
        dense_secondary = dense_slice_top2[0]

    row = {
        "vendor_id": 100000 + i,
        "business_name": business_name(category, i),
        "business_category": category,

        "price_range": aux["price_range"],
        "content_format": aux["content_format"],
        "purchase_frequency": aux["purchase_frequency"],
        "geography_signal": aux["geography_signal"],
        "data_source_coverage": aux["data_source_coverage"],

        "is_visual_product": round(base["is_visual_product"], 4),
        "is_utility_product": round(base["is_utility_product"], 4),
        "brand_loyalty_score": round(base["brand_loyalty_score"], 4),
        "impulse_buy_score": round(base["impulse_buy_score"], 4),
        "research_time_score": round(base["research_time_score"], 4),
        "video_consumption_score": round(base["video_consumption_score"], 4),
        "image_engagement_score": round(base["image_engagement_score"], 4),
        "text_engagement_score": round(base["text_engagement_score"], 4),
        "ugc_score": round(base["ugc_score"], 4),
        "influencer_dependency_score": round(base["influencer_dependency_score"], 4),
        "repeat_purchase_rate": round(base["repeat_purchase_rate"], 4),
        "price_sensitivity_score": round(base["price_sensitivity_score"], 4),
        "premium_affinity_score": round(base["premium_affinity_score"], 4),
        "trend_sensitivity_score": round(base["trend_sensitivity_score"], 4),
        "community_engagement_score": round(base["community_engagement_score"], 4),
        "local_discovery_score": round(base["local_discovery_score"], 4),
        "education_content_affinity": round(base["education_content_affinity"], 4),
        "short_form_video_affinity": round(base["short_form_video_affinity"], 4),
        "search_intent_score": round(base["search_intent_score"], 4),
        "conversion_readiness_score": round(base["conversion_readiness_score"], 4),
        "ingredient_awareness_score": round(base["ingredient_awareness_score"], 4),
        "routine_complexity_score": round(base["routine_complexity_score"], 4),

        "age_18_24_ratio": round(demo["age_18_24_ratio"], 4),
        "age_25_34_ratio": round(demo["age_25_34_ratio"], 4),
        "age_35_50_ratio": round(demo["age_35_50_ratio"], 4),
        "age_50_plus_ratio": round(demo["age_50_plus_ratio"], 4),
        "female_ratio": round(demo["female_ratio"], 4),
        "male_ratio": round(demo["male_ratio"], 4),
        "income_low_ratio": round(demo["income_low_ratio"], 4),
        "income_mid_ratio": round(demo["income_mid_ratio"], 4),
        "income_high_ratio": round(demo["income_high_ratio"], 4),
        
        "niche_anchor_skincare": round(anchor_features["niche_anchor_skincare"], 4),
        "niche_anchor_pet": round(anchor_features["niche_anchor_pet"], 4),
        "niche_anchor_streetwear": round(anchor_features["niche_anchor_streetwear"], 4),
        "niche_anchor_learning": round(anchor_features["niche_anchor_learning"], 4),
        "niche_anchor_home": round(anchor_features["niche_anchor_home"], 4),
        "niche_anchor_organic": round(anchor_features["niche_anchor_organic"], 4),
        
        "platform_anchor_tiktok": round(anchor_features["platform_anchor_tiktok"], 4),
        "platform_anchor_reddit": round(anchor_features["platform_anchor_reddit"], 4),
        "platform_anchor_instagram": round(anchor_features["platform_anchor_instagram"], 4),
        "platform_anchor_pinterest": round(anchor_features["platform_anchor_pinterest"], 4),
        "platform_anchor_website_first": round(anchor_features["platform_anchor_website_first"], 4),
        "platform_anchor_discord": round(anchor_features["platform_anchor_discord"], 4),
        "platform_anchor_youtube_shorts": round(anchor_features["platform_anchor_youtube_shorts"], 4),
        "platform_anchor_micro_influencers": round(anchor_features["platform_anchor_micro_influencers"], 4),
        "platform_anchor_marketplace_first": round(anchor_features["platform_anchor_marketplace_first"], 4),
        "platform_anchor_facebook_groups": round(anchor_features["platform_anchor_facebook_groups"], 4),

        "niche_anchor_diy": round(anchor_features["niche_anchor_diy"], 4),
        "niche_anchor_gadget": round(anchor_features["niche_anchor_gadget"], 4),
        "niche_anchor_gym": round(anchor_features["niche_anchor_gym"], 4),
        "niche_anchor_healthy": round(anchor_features["niche_anchor_healthy"], 4),
        
        "dense_anchor_college": round(anchor_features["dense_anchor_college"], 4),
        "dense_anchor_young_professional": round(anchor_features["dense_anchor_young_professional"], 4),
        "dense_anchor_luxury": round(anchor_features["dense_anchor_luxury"], 4),
        "dense_anchor_fitness": round(anchor_features["dense_anchor_fitness"], 4),
        "dense_anchor_pet": round(anchor_features["dense_anchor_pet"], 4),
        "dense_anchor_suburban": round(anchor_features["dense_anchor_suburban"], 4),
        "dense_anchor_tech": round(anchor_features["dense_anchor_tech"], 4),
        "dense_anchor_urban_female": round(anchor_features["dense_anchor_urban_female"], 4),
        "dense_anchor_budget": round(anchor_features["dense_anchor_budget"], 4),

        "avg_session_time_minutes": aux["avg_session_time_minutes"],
        "foot_traffic_score": aux["foot_traffic_score"],
        "population_density_score": aux["population_density_score"],
        "college_presence_score": aux["college_presence_score"],
        "competition_density_score": aux["competition_density_score"],
        "market_saturation_score": aux["market_saturation_score"],
        "demand_score": aux["demand_score"],
        "trend_score": aux["trend_score"],

        "repeat_customer_signal": aux["repeat_customer_signal"],
        "product_category_affinity": aux["product_category_affinity"],
        "niche_signal_score": aux["niche_signal_score"],
        "visual_content_signal": aux["visual_content_signal"],
        "transaction_conversion_signal": aux["transaction_conversion_signal"],
        "platform_fit_score": aux["platform_fit_score"],
        "dense_slice_confidence": aux["dense_slice_confidence"],

        "top_micro_niche_1": niche_primary,
        "top_micro_niche_2": niche_secondary,
        "recommended_platform_1": platform_primary,
        "recommended_platform_2": platform_secondary,
        "recommended_dense_slice_1": dense_slice_primary,
        "recommended_dense_slice_2": dense_secondary,
    }

    return row


def main() -> None:
    rows: List[Dict[str, object]] = [generate_row(i) for i in range(1, N_ROWS + 1)]
    df = pd.DataFrame(rows)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Dataset saved to: {OUTPUT_FILE}")
    print(f"Rows written: {len(df)}")
    print(f"Columns written: {len(df.columns)}")

    print("\nMicro niche distribution:")
    print(df["top_micro_niche_1"].value_counts())

    print("\nPlatform distribution:")
    print(df["recommended_platform_1"].value_counts())

    print("\nDense slice distribution:")
    print(df["recommended_dense_slice_1"].value_counts())
    


if __name__ == "__main__":
    main()