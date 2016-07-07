SWARM_DESCRIPTION = {
 "includedFields" : [
        {
            "fieldName": "timestamp",
            "fieldType": "datetime"
        },
        {
            "fieldName": "value",
            "fieldType": "int"
        }
    ],
    "streamDef": {
        "info": "ecg",
        "version": 1,
        "streams": [
            {
                "info": "ecg",
                "source": "file://disease_person1.csv",
                "columns": [
                    "*"
                ]
            }
        ]
    },

    "inferenceType": "TemporalAnomaly",
    "inferenceArgs": {
        "predictionSteps": [
            1
        ],
        "predictedField": "value"
    },
    "iterationCount": -1,
    "swarmSize": "small"
}
