from ml_models.inference.decision_engine import run_decision_engine_by_vendor_id


def build_execution_plan(result: dict) -> dict:
    niche = result["recommended_combination"]["niche"]
    platform = result["recommended_combination"]["platform"]
    dense = result["recommended_combination"]["dense_slice"]
    stage = result["business_recommendation"]["business_stage"]
    product_style = result["business_recommendation"]["product_style"]

    execution_plan = {}

    # 🎯 Niche execution
    niche_actions = {
        "DIY_Crafters": [
            "Create tutorial-based content",
            "Focus on before-after transformations",
            "Encourage user-generated content",
        ],
        "Pet_Lovers": [
            "Use emotional storytelling",
            "Promote repeat purchase bundles",
            "Highlight pet happiness and trust",
        ],
        "Healthy_Eating": [
            "Focus on routines and habits",
            "Highlight health benefits clearly",
            "Build trust via testimonials",
        ],
    }

    # 📱 Platform execution
    platform_actions = {
        "Instagram": [
            "Post high-quality visual content daily",
            "Use reels for short-form engagement",
            "Leverage influencer collaborations",
        ],
        "TikTok": [
            "Post 3–5 short videos daily",
            "Use trends and hooks",
            "Focus on viral-style content",
        ],
        "YouTube_Shorts": [
            "Create educational short videos",
            "Use quick demonstrations",
            "Optimize for retention",
        ],
    }

    # 🎯 Dense slice execution
    dense_actions = {
        "Young_Professionals": [
            "Focus on convenience and time-saving",
            "Highlight productivity benefits",
            "Use modern and clean branding",
        ],
        "College_Students": [
            "Keep pricing affordable",
            "Use fun and energetic content",
            "Focus on social sharing",
        ],
        "Luxury_Buyers": [
            "Use premium branding",
            "Highlight exclusivity",
            "Focus on quality storytelling",
        ],
    }

    execution_plan["niche_strategy"] = niche_actions.get(niche, ["General niche strategy"])
    execution_plan["platform_strategy"] = platform_actions.get(platform, ["General platform strategy"])
    execution_plan["audience_strategy"] = dense_actions.get(dense, ["General audience targeting strategy"])

    # 🧠 Stage-based execution
    if stage == "Early Stage":
        execution_plan["growth_strategy"] = [
            "Focus on awareness",
            "Test multiple creatives",
            "Optimize for engagement",
        ]
    elif stage == "Growth Stage":
        execution_plan["growth_strategy"] = [
            "Scale winning creatives",
            "Improve conversion funnel",
            "Focus on retention",
        ]
    else:
        execution_plan["growth_strategy"] = [
            "Optimize lifetime value",
            "Focus on brand loyalty",
            "Expand product lines",
        ]

    return execution_plan


def print_execution_plan(plan: dict):
    print("\n" + "=" * 100)
    print("AI EXECUTION PLAN")
    print("=" * 100)

    for section, actions in plan.items():
        print(f"\n{section.upper()}:")
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")

    print("\n" + "=" * 100)


def main():
    vendor_id = input("Enter vendor_id: ").strip()

    result = run_decision_engine_by_vendor_id(vendor_id)

    plan = build_execution_plan(result)

    print_execution_plan(plan)


if __name__ == "__main__":
    main()