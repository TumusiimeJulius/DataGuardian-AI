from datetime import datetime


agents_activity = [

    {
        "name": "Data Investigator Agent",
        "status": "Idle",
        "task": "Waiting for dataset",
        "health": "Healthy",
        "last_execution": None
    },


    {
        "name": "Data Quality Agent",
        "status": "Idle",
        "task": "Waiting for dataset",
        "health": "Healthy",
        "last_execution": None
    },


    {
        "name": "Anomaly Detection Agent",
        "status": "Idle",
        "task": "Waiting for dataset",
        "health": "Healthy",
        "last_execution": None
    },


    {
        "name": "Repair Agent",
        "status": "Idle",
        "task": "Waiting for dataset",
        "health": "Healthy",
        "last_execution": None
    },


    {
        "name": "Recommendation Agent",
        "status": "Idle",
        "task": "Waiting for dataset",
        "health": "Healthy",
        "last_execution": None
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

            agent["last_execution"] = (
                datetime.now()
                .isoformat()
            )



def get_agents():

    return agents_activity