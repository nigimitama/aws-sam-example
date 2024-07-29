FROM public.ecr.aws/lambda/python:3.12
COPY app.py requirements.txt ./
RUN python3.12 -m pip install -r requirements.txt -t .
CMD ["app.lambda_handler"]
