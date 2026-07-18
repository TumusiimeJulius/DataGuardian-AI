try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - allows missing dependency in minimal environments
    requests = None


class DataHubClient:

    def __init__(self):
        # DataHub default API endpoint
        self.base_url = "http://localhost:8080"

    def search_dataset(self, query):

        # Temporary mock response
        # Later replaced with real DataHub API call

        return {
            "dataset": query,
            "owner": "Data Engineering Team",
            "schema": [
                "customer_id",
                "amount",
                "created_at"
            ],
            "lineage": [
                "raw_transactions",
                "sales_model",
                "dashboard"
            ]
        }


datahub_client = DataHubClient()