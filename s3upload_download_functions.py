def download_file(s3_path: str, local_path: str,
                  bucket: str = DEFAULT_BUCKET, region: str = DEFAULT_REGION):
    """
        Download a file to a local directory from s3 # TODO: Add example usage
        Args:
            s3_path (str): s3 path to file (relative to bucket name)
            local_path (str): path of the local machine to save downloaded file # TODO: this is wrong
            bucket (str): bucket name #TODO: Explain / at the end
            region (str): Region in which the bucket is located
        Returns:
             returns file to given local path
    """
    logger = logging.getLogger(__name__)
    s3 = boto3.resource("s3", region_name=region)
    f = f'{PROJECT_DIR}/{local_path}'
    if os.path.isfile(f):
        logger.info("File already exists. Skipping download")
        return f
    s3.Bucket(bucket).download_file(s3_path, f)
    return f


def download_directory(s3_path: str, local_dir: str,
                       bucket: str = DEFAULT_BUCKET, region: str = DEFAULT_REGION):
    """
            Download a folder to a local directory from s3 # TODO: Add example usage
            Args:
                s3_path (str): s3 path to folder (relative to bucket name)
                local_dir (str): path of the local machine to save downloaded file
                bucket (str): bucket name
                region (str): location
    """
    logger = logging.getLogger(__name__)
    s3_resource = boto3.resource('s3', region_name=region)
    bucket = s3_resource.Bucket(bucket)
    local_abs_path = PROJECT_DIR / local_dir

    logger.info(f"Downloading {s3_path} to {local_abs_path}")
    for obj in tqdm(bucket.objects.filter(Prefix=s3_path)):
        f = f'{local_abs_path}/{obj.key}'
        if not os.path.exists(os.path.dirname(f)):
            os.makedirs(os.path.dirname(f))
        if obj.key == s3_path or os.path.isfile(f):
            continue
        bucket.download_file(obj.key, f)
    logger.info(f"Downloaded {s3_path} to {local_abs_path}")


def upload_to_s3(local_path: str, s3_path: str, bucket: str):
    """
    Upload a file to s3 from a local directory # TODO: Add example usage
    Args:
        bucket (str): bucket name
        s3_path (str): s3 path to file (relative to bucket name)
        local_path (str): path of the local for upload # TODO: is this an absolute path?
    Returns:
        (str) remote path to file
    """
    client = boto3.client("s3")
    client.upload_file(local_path, bucket, s3_path)
    return f"s3://{bucket}/{s3_path}"
