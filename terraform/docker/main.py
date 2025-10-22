import boto3
import os
from datetime import datetime
from utils import (extract_text_from_file,
                   generate_word_list,
                   convert_word_list_to_csv)


s3 = boto3.client("s3")
bucket = os.environ["BUCKET_NAME"]
input_key = os.environ["INPUT_KEY"]

local_input = "/tmp/input.txt"
local_output = "/tmp/output.csv"

s3.download_file(bucket, input_key, local_input)

text = extract_text_from_file(local_input)

word_list = generate_word_list(text)

convert_word_list_to_csv(word_list, local_output)

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
output_key = f"output/wordlist_{timestamp}.csv"

s3.upload_file(local_output, bucket, output_key)