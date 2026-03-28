import json
from ml_models.inference.niche_inference import predict_niche
from ml_models.inference.platform_inference import predict_platform
from ml_models.inference.dense_slice_inference import predict_dense_slice


def build_micro_niche_agent_output(niche_result):
    niche = niche_result["top_predicted_niche"]
    confidence = niche_result["confidence"]

    return {
        "agent_name": "MicroNicheStrategyAgent",
        "primary_recommendation": niche,
        "confidence": confidence,
        "strategy": niche_result["decision_intelligence"]["recommended_strategy"]
    }


def build_platform_agent_output(platform_result):
    platform = platform_result["top_predicted_platform"]
    confidence = platform_result["confidence"]

    return {
        "agent_name": "PlatformExecutionAgent",
        "primary_recommendation": platform,
        "confidence": confidence,
        "strategy": platform_result["decision_intelligence"]["recommended_strategy"]
    }


def build_dense_slice_agent_output(dense_result):
    dense_slice = dense_result["top_predicted_dense_slice"]
    confidence = dense_result["confidence"]

    return {
        "agent_name": "LocalDominationAgent",
        "primary_recommendation": dense_slice,
        "confidence": confidence,
        "strategy": dense_result["decision_intelligence"]["recommended_strategy"]
    }


def orchestrate_business_strategy(vendor_id):
    niche_result = predict_niche(vendor_id)
    platform_result = predict_platform(vendor_id)
    dense_result = predict_dense_slice(vendor_id)

    niche_agent = build_micro_niche_agent_output(niche_result)
    platform_agent = build_platform_agent_output(platform_result)
    dense_agent = build_dense_slice_agent_output(dense_result)

    final_result = {
        "vendor_id": vendor_id,
        "business_name": niche_result["business_name"],
        "business_category": niche_result["business_category"],
        "geography_signal": niche_result["geography_signal"],
        "ml_predictions": {
            "micro_niche": niche_result,
            "platform": platform_result,
            "dense_slice": dense_result
        },
        "ai_agents": {
            "micro_niche_agent": niche_agent,
            "platform_agent": platform_agent,
            "dense_slice_agent": dense_agent
        },
        "executive_summary": (
            f"{niche_result['business_name']} should prioritize the niche "
            f"{niche_result['top_predicted_niche']}, execute primarily through "
            f"{platform_result['top_predicted_platform']}, and focus initial traction on "
            f"{dense_result['top_predicted_dense_slice']}."
        ),
        "action_plan": [
            niche_agent["strategy"],
            platform_agent["strategy"],
            dense_agent["strategy"]
        ]
    }

    return final_result


if __name__ == "__main__":
    vendor_id = 1001
    result = orchestrate_business_strategy(vendor_id)
    print(json.dumps(result, indent=2))