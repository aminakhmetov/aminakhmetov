import bentoml
from bentoml.io import NumpyNdarray

model_ref = bentoml.sklearn.get("mlzoomcamp_homework:jsi67fslz6txydu5")
model_runner = model_ref.to_runner()

svc = bentoml.Service("mlzoomcamp_homework", runners = [model_runner])

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def predict(input):
    prediction = model_runner.predict.run(input)
    print(prediction)
    return prediction
