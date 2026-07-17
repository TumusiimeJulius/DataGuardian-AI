from datetime import datetime


agents_activity = [

    {
        "name": "Data Investigator Agent",
        "status": "Idle",
        "task": "Waiting for dataset",
        "last_update": None
    },

    {
        "name": "Data Quality Agent",
        "status": "Idle",
        "task": "Waiting for analysis",
        "last_update": None
    },

    {
        "name": "Anomaly Detection Agent",
        "status": "Idle",
        "task": "Waiting for anomalies",
        "last_update": None
    },

    {
        "name": "Repair Agent",
        "status": "Idle",
        "task": "Waiting for issues",
        "last_update": None
    },

    {
        "name": "Recommendation Agent",
        "status": "Idle",
        "task": "Waiting for recommendations",
        "last_update": None
    }

]



def update_agent(
    name,
    status,
    task
):

    for agent in agents_activity:

        if agent["name"] == name:

            agent["status"] = status

            agent["task"] = task

            agent["last_update"] = (
                datetime.now().isoformat()
            )


    return agents_activity



def get_agents():

    return agents_activity