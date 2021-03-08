import boto3
import datetime
import pytz
import json

from cache import file_cache
from prescriptions.config import settings

from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger

logger = Logger(child=True)


class CacheHandler:

    def __init__(self, cache_key, max_age=None):
        self.cache_key = cache_key
        self.max_age = max_age

    @property
    def dynamodb(self):
        return boto3.client('dynamodb')

    def _get_cache_from_file(self):
        cached_item = file_cache.get(self.cache_key, expire_time=True)
        if cached_item[1]:
            logger.info({'info': 'cache_found_in_file', 'attr': {'key': self.cache_key, 'value': {'value': cached_item[0], 'expires_on': cached_item[1]}}})
            self._get_cache_max_age(cached_item[1])
        return cached_item[0]

    def _get_cache_from_dynamo(self):
        try:
            item = self.dynamodb.get_item(
                TableName=settings.cache_table,
                Key={
                    'key': {
                        'S': self.cache_key
                    }
                }
            )
            logger.info({'info': 'cache_found_in_dynamo', 'attr': {'key': self.cache_key, 'value': item['Item']}})
            self._get_cache_max_age(item['Item']['expires_on']['N'])
            return item['Item']['value']['S']
        except (ClientError, KeyError):
            return None

    def _get_expiration_time(self, dt):
        dt_incremented = dt + datetime.timedelta(seconds=(self.cache_ttl))
        return int(dt_incremented.timestamp())

    def _save_cache_dynamo(self, value):
        item = {
            'key': {'S': self.cache_key},
            'value': {'S': value},
            'expires_on': {'N': str(self._get_expiration_time(datetime.datetime.now()))}
        }
        self._get_cache_max_age(item['expires_on']['N'])
        return self.dynamodb.put_item(
            TableName=settings.cache_table,
            Item=item
        )

    def _save_cache_file(self, value):
        logger.info({'info': 'saved_cache_in_file', 'attr': {'key': self.cache_key}})
        file_cache.set(key=self.cache_key, value=value, expire=self.max_age)

    def _get_cache_max_age(self, dynamo_ttl):
        ttl_datetime = datetime.datetime.fromtimestamp(int(dynamo_ttl), tz=pytz.utc)
        now = datetime.datetime.now(tz=pytz.utc)
        self.max_age = round((ttl_datetime - now).total_seconds())

    def get_cache(self):
        value = self._get_cache_from_file()

        if not value:
            value = self._get_cache_from_dynamo()

        self._save_cache_file(value)
        return json.loads(value) if value else value

    def save_cache(self, value, cache_ttl):
        value = json.dumps(value)
        self.cache_ttl = cache_ttl
        self._save_cache_dynamo(value)
        logger.info({'info': 'saved_cache_in_dynamo', 'attr': {'key': self.cache_key}})

        self._save_cache_file(value)
        return True
