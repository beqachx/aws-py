from botocore.exceptions import ClientError
from datetime import datetime, timedelta
from auth import init_client
import logging
import argparse
"""
დაწერეთ cli script - ი რომელიც შეამოწმებს პარამეტრად გადაცემული ფაილების ვერსიებს, რის შემდეგაც წაშლის ყველა ვერსიას რომელიც შექმნილია 6 თვის წინ.
"""

parser = argparse.ArgumentParser(
  description='Delete files older than 6 months from an AWS S3 bucket'
)

parser.add_argument(
  'bucket',
  metavar='bucket',
  type=str,
  help='the name of the AWS S3 bucket to delete files from'
)

parser.add_argument(
  'files',
  metavar='file',
  type=str,
  nargs='+',
  help='a list of file names to delete'
)

current_date = datetime.now()
six_months_ago = current_date - timedelta(days=180)

def main():
  s3_client = init_client()
  args = parser.parse_args()

  for file in args.files:
    try:
        response = s3_client.head_object(Bucket=args.bucket, Key=file)
    except ClientError as e:
        print(f"Error getting {file}: {e}")
        continue
        
    last_modified = response.get('LastModified')
    if last_modified is not None and last_modified < six_months_ago:
        try:
            s3_client.delete_object(Bucket=args.bucket, Key=file)
            print(f"Deleted {file} from {args.bucket}")
        except ClientError as e:
            print(f"Error deleting {file}: {e}")


if __name__ == "__main__":
  try:
    main()
  except ClientError as e:
    logging.error(e)