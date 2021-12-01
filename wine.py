
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.regression import LabeledPoint
from pyspark.shell import sc
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, StringType, IntegerType


def main():
    spark = SparkSession \
        .builder \
        .appName('wine prediction') \
        .getOrCreate()

    dataframe = (spark.read
          .format("csv")
          .option('header', 'true')
          .load("TrainingDataset.csv", inferSchema='true',header = True ,sep =";"))

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


    data2=[]
    for lp in data:
        temp="["
        for i in lp.features:
            temp+=" "+str(i)+","
        temp+="]"
        data2.append((temp,lp.label,model.predict(lp.features)))

    schema = StructType([
        StructField("features", StringType(), True), \
        StructField("label", FloatType(), True), \
        StructField("prediction", IntegerType(), True) \
        ])

    df2 = spark.createDataFrame(data=data2, schema=schema)
    df2.show(20)
    predictionAndLabel = dataset.map(lambda lp: (float(model.predict(lp.features)), lp.label))
    metrics = MulticlassMetrics(predictionAndLabel)
    f1Score = metrics.weightedFMeasure()
    print("F1 Score = %s" % f1Score)
if __name__ == '__main__':
    main()