#!/usr/bin/env python
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
import nupic_anomaly_output as nupic_output
from model_params import model_params

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
# '2015-10-17 21:06:02.551394'

def createModel():
    model = ModelFactory.create(model_params.MODEL_PARAMS)
    model.enableInference({
        "predictedField": "value"
    })
    return model

def runModel(model):
    inputFilePath = "disease_person1.csv"
    inputFile = open(inputFilePath,"rb")
    csvReader = csv.reader(inputFile)
    #skip header rows
    csvReader.next()
    csvReader.next()
    csvReader.next()
    shifter = InferenceShifter()
    output = nupic_output.NuPICPlotOutput("ECG")
    counter = 0
    for row in csvReader:
        counter += 1
        if(counter % 100 == 0):
            print "Read %i lines..." % counter
        timestamp = datetime.datetime.strptime(row[0],DATE_FORMAT)
        #timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-6]

        value = int(row[1])
        result = model.run({
            "timestamp": timestamp,
            "value": value
        })

        result = shifter.shift(result)

        prediction = result.inferences["multiStepBestPredictions"][1]
        anomalyScore = result.inferences["anomalyScore"]
        output.write(timestamp, value,prediction, anomalyScore)
    inputFile.close()
    output.close()

def runECG():
    model = createModel()
    runModel(model)

if __name__ == "__main__":
    runECG()
