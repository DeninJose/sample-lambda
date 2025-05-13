FROM public.ecr.aws/lambda/python:3.11

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add function code
COPY app/ .

# Set the Lambda function handler
CMD ["lambda_function.lambda_handler"]