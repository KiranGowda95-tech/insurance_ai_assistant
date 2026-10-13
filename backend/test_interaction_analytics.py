
import json
from services.interaction_analytics_service import (
    get_interaction_analytics,
)

result = get_interaction_analytics()

print(json.dumps(result, indent=2, default=str))

assert result["total_interactions"] >= 0
assert result["unique_customers"] >= 0

print("\nCustomer interaction analytics test passed.")
