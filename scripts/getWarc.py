import boto3
import os

def list_warc_files(s3 : boto3, bucket_name : str, prefix : str) -> list:
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        warc_files = [file['Key'] for file in response['Contents']]
        print(f"Found {len(warc_files)} WARC files in {prefix}")
        return warc_files
    else:
        print("No files found.")
        return []

def get_needed_warc_file(s3 : boto3, bucket_name : str, warc_file : str) -> None:
    local_filename = f"warc_store/{os.path.basename(warc_file)}"
    
    print(f"Downloading {warc_file}...")
    
    s3.download_file(bucket_name, warc_file, local_filename)
    
    print(f"Download complete: {local_filename}")
    return local_filename

def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = "commoncrawl"
    prefix = "crawl-data/CC-NEWS/2025/01"
    warc_files = list_warc_files(s3, bucket_name, prefix)
    get_needed_warc_file(s3, bucket_name, warc_files[0])


if __name__ == "__main__":
    main()