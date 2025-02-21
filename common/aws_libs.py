from botocore.exceptions import ClientError
from common.aws_config import AwsConfig
from boto3.dynamodb.conditions import Key, Attr
from common.logger import logger
import json
import time


class Aws(AwsConfig):
    def __init__(self, **kwargs):
        super(Aws, self).__init__(**kwargs)
        self.s3_client = self.session.client("s3")
        self.db_client = self.session.client("dynamodb")
        self.db_resource = self.session.resource('dynamodb')
        self.lambda_client = self.session.client("lambda")
        self.log_client = self.session.client('logs')
        self.sqs_client = self.session.client('sqs')

    def get_account_settings(self):
        response = self.lambda_client.get_account_settings()
        return response

    def s3_list_buckets(self):
        """show all s3 buckets"""
        response = self.s3_client.list_buckets()
        logger.info('Existing buckets:')
        for bucket in response['Buckets']:
            logger.info(f'bucket name:{bucket["Name"]}')

    def s3_upload_file(self, file_name, upload_key, bucket):
        """
        :param file_name: x_src.zip
        :param upload_key: test/x_src.zip
        :param bucket: a250212-qa-upload-snapshot-files
        """
        self.s3_client.upload_file(Filename=file_name, Key=upload_key, Bucket=bucket)

    def s3_download_file(self, file_name, download_key, bucket):
        """
        :param file_name: save to local pc. such as g:/test.zip
        :param download_key: test/x_src.zip
        :param bucket: a250212-qa-upload-snapshot-files
        :return:
        """
        self.s3_client.download_file(Filename=file_name, Key=download_key, Bucket=bucket)

    def s3_delete_object(self, key_name, bucket):
        """
        :param key_name: test/x_src.zip
        :param bucket: a250212-qa-upload-snapshot-files
        """
        self.s3_client.delete_object(Key=key_name, Bucket=bucket)

    def s3_get_object(self, key_name, bucket_name):
        """
        :param bucket_name: a250212-qa-upload-snapshot-files
        :param key_name: test/x_src.zip
        :return: boolean
        """
        rsp = None
        try:
            rsp = self.s3_client.get_object(Bucket=bucket_name, Key=key_name)
            logger.debug(rsp)
        except ClientError as e:
            logger.error(e)
        return rsp

    def s3_key_exists(self, key_name, bucket_name):
        """
        :param bucket_name: a250212-qa-upload-snapshot-files
        :param key_name: test/x_src.zip
        :return: boolean
        """
        rsp = self.s3_get_object(key_name, bucket_name)
        if rsp:
            return True
        else:
            return False

    def retrieving_bucket_subfolders(self, bucket, prefix, max_keys=100):

        response = self.s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_keys)
        return response["Contents"]

    def db_list_tables(self):
        response = self.db_client.list_tables(
            # ExclusiveStartTableName='string',
            # Limit=123
        )
        logger.debug(response)
        return response

    def db_get_table(self, table_name):
        response = self.db_client.describe_table(
            TableName=table_name
        )
        return response

    def db_get_item(self, table, partition, sort=None):
        """
        :param table: target table
        :param partition: partition key of the given table
        :param sort: sort key of the given table
        """
        item_data = None
        # get key and value from partition
        partition_items_list = list(partition.items())
        partition_key, partition_value = partition_items_list[0]
        # query with the given dict
        tbl = self.db_resource.Table(table)
        try:
            if sort:
                # get key and value from sort
                sort_items_list = list(sort.items())
                sort_key, sort_value = sort_items_list[0]
                get_response = tbl.query(
                    KeyConditionExpression=Key(partition_key).eq(partition_value) & Key(
                        sort_key).eq(sort_value)
                )
            else:
                get_response = tbl.query(
                    KeyConditionExpression=Key(partition_key).eq(partition_value)
                )

            if get_response['Items']:
                item_data = get_response['Items']
        except Exception as e:
            logger.error(e)
        return item_data

    def db_get_range_item(self, table, partition_list, sort=None):
        """
        :param table: target table
        :param partition_list: list which contains partition key of the given table
        :param sort: sort key of the given table
        """
        for key, values in partition_list[0].items():
            hash_key = key
            hash_value = values
        for key, values in partition_list[1].items():
            range_key = key
            range_value = values

        # query with the given dict
        tbl = self.db_resource.Table(table)
        if sort:
            # get key and value from sort
            sort_items_list = list(sort.items())
            sort_key, sort_value = sort_items_list[0]
            get_response = tbl.query(
                KeyConditionExpression=Key(hash_key).eq(hash_value) & Key(range_key).eq(range_value) & Key(sort_key).eq(
                    sort_value)
            )
        else:
            get_response = tbl.query(
                KeyConditionExpression=Key(hash_key).eq(hash_value) & Key(range_key).eq(range_value)
            )
        if get_response['Items']:
            item_data = get_response['Items']
        else:
            item_data = None
        return item_data

    def db_scan_items(self, table, filter_value, count=0):
        """
        :param table: target table
        :param filter_value: format shall be ['relation',{'key':'value'}],
        :param count: stop scan when count reaches
        :return: item list
        """
        item_data = list()
        tbl = self.db_resource.Table(table)
        partition_items_list = list(filter_value[1].items())
        partition_key, partition_value = partition_items_list[0]
        if filter_value[0] == 'eq':
            filter_expression = Attr(partition_key).eq(partition_value)
        last_evaluated_key = None
        while True:
            if last_evaluated_key:
                response = tbl.scan(
                    FilterExpression=filter_expression,
                    ExclusiveStartKey=last_evaluated_key
                )
            else:
                response = tbl.scan(
                    FilterExpression=filter_expression
                )
            last_evaluated_key = response.get('LastEvaluatedKey')
            item_data.extend(response['Items'])
            if count:
                if len(item_data) >= count:
                    break
            if not last_evaluated_key:
                break
        return item_data

    def query_items_by_sourceid(self, table, filter_value):
        item_list = self.db_scan_items(table, filter_value)
        partition_items_list = list(filter_value[1].items())
        event_id = partition_items_list[0][1]
        partition_list = {"id": event_id}
        item = self.db_get_item(table, partition_list)
        if item:
            item_list.append(item[0])
        return item_list

    def get_queue_url(self, queue_name):
        response = self.sqs_client.get_queue_url(QueueName=queue_name)
        queue_url = response['QueueUrl']
        return queue_url

    def send_sqs(self, queue_url, message_body, queue_name=None, message_attributes=None):
        if not queue_url:
            if queue_name:
                queue_url = self.get_queue_url(queue_name)
        if not queue_url:
            raise Exception(f"queue url is none,queue_name:{queue_name},queue_url:{queue_url}")
        if isinstance(message_body, dict):
            message_body = json.dumps(message_body)
        if message_attributes is None:
            message_attributes = {}
        response = self.sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        return response


    def query_logs_insights(self,log_groupname,query_string,start_time,end_time):
        response = self.log_client.start_query(
            logGroupName=log_groupname,
            startTime=start_time,  # 1 hour ago in milliseconds
            endTime=end_time,
            queryString=query_string
        )
        query_id = response['queryId']
        response = None
        # Wait for the query to complete
        while response == None or response['status'] == 'Running':
            print('Waiting for query to complete ...')
            time.sleep(1)
            response = self.log_client.get_query_results(
                queryId=query_id
            )

        # Process and print the results
        return response['results']


    def query_log_stream(self,log_groupname, log_streamname, start_time, end_time):
        response = self.log_client.get_log_events(
            logGroupName=log_groupname,
            logStreamName=log_streamname,
            startTime=start_time,
            endTime=end_time,
        )

        while response == None:
            time.sleep(1)
            response = self.query_log_stream(log_groupname, log_streamname, start_time, end_time)

        return response["events"]



