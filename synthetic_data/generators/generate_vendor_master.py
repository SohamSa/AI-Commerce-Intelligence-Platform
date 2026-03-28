import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()
np.random.seed(42)
random.seed(42)

TOTAL_VENDORS = 2000

# -----------------------------
# Distributions
# -----------------------------

strength_distribution = (
    ["A"] * 200 +
    ["B"] * 400 +
    ["C"] * 800 +
    ["D"] * 600
)

random.shuffle(strength_distribution)

transaction_tier_map = {
    "A": "high",
    "B": "medium_high",
    "C": "medium",
    "D": "low"
}

categories = [
    "Beauty", "Fitness", "Fashion", "Food", "Home",
    "Wellness", "Pets", "Tech_Accessories", "Crafts", "Education"
]

platforms = [
    "Instagram", "TikTok", "YouTube_Shorts", "Pinterest",
    "Reddit", "Facebook_Groups", "Discord",
    "Website_First", "Marketplace_First", "Micro_Influencers"
]

dense_slices = [
    "Urban_Female_20_30", "Young_Professionals", "College_Students",
    "Suburban_Families", "Fitness_Enthusiasts", "Pet_Owners",
    "Tech_Early_Adopters", "Budget_Shoppers", "Luxury_Buyers", "DIY_Creators"
]

geo_clusters = [
    "Urban", "Suburban", "Mixed", "College_Town",
    "Downtown_CBD", "Regional_Hub", "Neighborhood_Local",
    "National_Distributed", "Wellness_Corridor", "Family_Suburb_Belt"
]

micro_niches = [
    "Skincare_Enthusiasts", "Organic_Beauty", "Gym_Beginners",
    "Streetwear_Fans", "Home_Decor_Lovers", "Healthy_Eating",
    "Pet_Lovers", "Gadget_Geeks", "DIY_Crafters", "Online_Learners"
]

# -----------------------------
# Helper functions
# -----------------------------

def generate_signal(base_low, base_high, strength):
    if strength == "A":
        return np.random.uniform(0.75, 0.95)
    elif strength == "B":
        return np.random.uniform(0.6, 0.8)
    elif strength == "C":
        return np.random.uniform(0.4, 0.65)
    else:
        return np.random.uniform(0.2, 0.5)

# -----------------------------
# Generate data
# -----------------------------

data = []

for i in range(TOTAL_VENDORS):
    vendor_id = 1000 + i
    strength = strength_distribution[i]
    category = random.choice(categories)

    niche_1 = random.choice(micro_niches)
    niche_2 = random.choice(micro_niches)

    platform_1 = random.choice(platforms)
    platform_2 = random.choice(platforms)

    dense_1 = random.choice(dense_slices)
    dense_2 = random.choice(dense_slices)

    geo = random.choice(geo_clusters)

    row = {
        "vendor_id": vendor_id,
        "business_name": fake.company(),
        "business_category": category,
        "business_stage": random.choice(["early", "growth", "mature"]),

        "top_micro_niche_1": niche_1,
        "top_micro_niche_2": niche_2,

        "recommended_platform_1": platform_1,
        "recommended_platform_2": platform_2,

        "recommended_dense_slice_1": dense_1,
        "recommended_dense_slice_2": dense_2,

        "geography_signal": geo,

        "niche_signal_score_base": generate_signal(0, 1, strength),
        "visual_content_signal_base": generate_signal(0, 1, strength),
        "transaction_conversion_signal_base": generate_signal(0, 1, strength),
        "platform_fit_score_base": generate_signal(0, 1, strength),
        "dense_slice_confidence_base": generate_signal(0, 1, strength),

        "strength_class": strength,
        "transaction_tier": transaction_tier_map[strength]
    }

    data.append(row)

df = pd.DataFrame(data)

# -----------------------------
# Save
# -----------------------------

output_path = "synthetic_data/generated/vendor_master.csv"
df.to_csv(output_path, index=False)

print(f"Vendor master generated: {output_path}")