from boto3.session import Session

class AwsConfig(object):
    """
    aws configuration.
    """

    def __init__(self, **kwargs):
        self.config_path = kwargs.get('config_path')
        self.access_key = kwargs.get('access_key')
        self.secret_key = kwargs.get('secret_key')
        self.region = kwargs.get('region') or "us-east-1"
        self.profile_name = kwargs.get('profile_name')
        self.pool = {}
        """
        :param config_path: custom credentials file path
        :param access_key: custom aws_access_key_id
        :param secret_key: custom aws_secret_access_key
        :param region: custom region
        :param profile_name: specific profile_name
        """
        if self.config_path:
            with open(self.config_path, 'r') as f:
                content_list = f.readlines()
                self.access_key = content_list[1].strip()
                self.secret_key = content_list[2].strip()
                self.region = content_list[3].strip()

        elif self.access_key and self.secret_key:
            if self.region:
                self.session = Session(aws_access_key_id=self.access_key,
                                       aws_secret_access_key=self.secret_key,
                                       region_name=self.region)
            else:
                self.session = Session(aws_access_key_id=self.access_key,
                                       aws_secret_access_key=self.secret_key)
        elif self.profile_name:
            if self.region:
                self.session = Session(profile_name=self.profile_name,region_name= self.region)
            else:
                self.session = Session(profile_name=self.profile_name)
        else:
            if self.region:
                self.session = Session(region_name= self.region)
            else:
                self.session = Session()




