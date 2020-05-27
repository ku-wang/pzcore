import boto3

s3_ac_key = "T2TZH7A6NEO2WDIYPNZC"
s3_se_key = "hIOs9p4fZs9rB5fPXDX138M8PBtztcWdpqwJSpnY"

end_point = "http://10.180.128.101:7480"
bucket_name = "test1"


class S3obj(object):

    def __init__(self, endpoint_url, access_key, secret_key):
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key

    def s3_client(self):
        return boto3.client(service_name="s3", endpoint_url=self.endpoint_url, aws_access_key_id=self.access_key,
                            aws_secret_access_key=self.secret_key)

    def list_buckets(self):
        buckets = []
        responce = self.s3_client().list_buckets()

        for bucket in responce['Buckets']:
            buckets.append(bucket['Name'])

        return buckets

    def list_files_from_bucket(self, bucket):
        files = []

        response = self.s3_client().list_objects_v2(Bucket=bucket)
        for file in response['Contents']:
            files.append(file['Key'])

        return {bucket: files}

    def upload_file(self, source_file_path, bucket_name, upload_as_name):
        self.s3_client().upload_file(source_file_path, bucket_name, upload_as_name)

    def download_file(self, bucket_name, source_file, download_as_name):
        self.s3_client().download_file(bucket_name, source_file, download_as_name)


s3 = S3obj(end_point, s3_ac_key, s3_se_key)

buckets = s3.list_files_from_bucket("test1")

print(buckets)
