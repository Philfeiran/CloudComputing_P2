
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.regression import LabeledPoint
from pyspark.shell import sc
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType,StringType


def main():
    spark = SparkSession \
        .builder \
        .appName('wine prediction') \
        .getOrCreate()

    dataframe = (spark.read
          .format("csv")
          .option('header', 'true')
          .load("TrainingDataset.csv", inferSchema='true',header = True ,sep =";"))


    testdataframe = (spark.read
                 .format("csv")
                 .option('header', 'true')
                 .load("TestDataset.csv", inferSchema='true', header=True, sep=";"))
    data=[]

    for row in dataframe.rdd.collect():
        feature=[row['"""""fixed acidity""""'],row['""""volatile acidity""""'],
                  row['""""citric acid""""'],row['""""residual sugar""""'],
                  row['""""chlorides""""'],row['""""free sulfur dioxide""""'],
                  row['""""total sulfur dioxide""""'],row['""""density""""'],
                  row['""""pH""""'],row['""""sulphates""""'],row['""""alcohol""""']]
        label=row['""""quality"""""']
        data.append(LabeledPoint(label,feature))
    dataset=sc.parallelize(data)
    model = LogisticRegressionWithLBFGS.train(dataset,numClasses=10)
    ##dataframe.show(1)
   ## testdataframe.show(1)
    data2=[]
    for row in testdataframe.rdd.collect():
        feature = [row['"fixed acidity"'], row['"volatile acidity"'],
                   row['"citric acid"'], row['"residual sugar"'],
                   row['"chlorides"'], row['"free sulfur dioxide"'],
                   row['"total sulfur dioxide"'], row['"density"'] ,
                   row['"pH"'], row['"sulphates"'], row['"alcohol"']]
        label = row['"quality"']
        data2.append([str(feature),label,model.predict(feature)])

    schema = StructType([
        StructField("features", StringType(), True), \
        StructField("label", IntegerType(), True), \
        StructField("prediction", IntegerType(), True) \
        ])

    df2 = spark.createDataFrame(data=data2, schema=schema)
    df2.show(20)


    dataset2 = sc.parallelize(data2)
    predictionAndLabel = dataset2.map(lambda row: (float(row[2]), float(row[1])))
    metrics = MulticlassMetrics(predictionAndLabel)
    f1Score = metrics.weightedFMeasure()
    print("F1 Score = %s" % f1Score)
if __name__ == '__main__':
    main()
