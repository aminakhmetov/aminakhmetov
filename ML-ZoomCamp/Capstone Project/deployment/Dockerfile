FROM public.ecr.aws/lambda/python:3.9

RUN pip install keras-image-helper
RUN pip install tflite-runtime==2.7.0

COPY cutlery-prod.tflite .
COPY lambda_function.py .

CMD [ "lambda_function.lambda_handler" ]