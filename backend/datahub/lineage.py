class LineageAnalyzer:


    def trace(self, dataset):

        lineage = {
            "dataset":dataset,
            "sources":[
                "raw_transactions"
            ],
            "transformations":[
                "sales_model aggregation"
            ],
            "outputs":[
                "sales dashboard"
            ]
        }


        return lineage