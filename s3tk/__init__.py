import sys
import json
import fnmatch
from collections import Counter, OrderedDict
import warnings
import boto3
import botocore
import click
from joblib import Parallel, delayed
from .checks import AclCheck, PolicyCheck, PublicAccessCheck, LoggingCheck, VersioningCheck, EncryptionCheck, ObjectLoggingCheck

# fix for https://github.com/kennethreitz-archive/clint/issues/185
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from clint.textui import colored, puts, indent

__version__ = '0.5.0'

canned_acls = [
    {
        'acl': 'private',
        'grants': []
    },
    {
        'acl': 'public-read',
        'grants': [
            {'Grantee': {'Type': 'Group', 'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'}, 'Permission': 'READ'}
        ]
    },
    {
        'acl': 'public-read-write',
        'grants': [
            {'Grantee': {'Type': 'Group', 'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'}, 'Permission': 'READ'},
            {'Grantee': {u'Type': 'Group', u'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'}, 'Permission': 'WRITE'}
        ]
    },
    {
        'acl': 'authenticated-read',
        'grants': [
            {'Grantee': {'Type': 'Group', 'URI': 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'}, 'Permission': 'READ'}
        ]
    },
    {
        'acl': 'aws-exec-read',
        'grants': [
            {'Grantee': {'Type': 'CanonicalUser', 'DisplayName': 'za-team', 'ID': '6aa5a366c34c1cbe25dc49211496e913e0351eb0e8c37aa3477e40942ec6b97c'}, 'Permission': 'READ'}
        ]
    }
]

cached_s3 = None


def s3():
    # memoize
    pass


def notice(message):
    pass


def abort(message):
    pass


def unicode_key(key):
    pass


def perform(check):
    pass


def fetch_buckets(buckets):
    pass


def fix_check(klass, buckets, dry_run, fix_args={}):
    pass


def encrypt_object(bucket_name, key, dry_run, kms_key_id, customer_key):
    pass


def determine_mode(acl):
    pass


def scan_object(bucket_name, key):
    pass


def reset_object(bucket_name, key, dry_run, acl):
    pass


def delete_unencrypted_version(bucket_name, key, id, dry_run):
    pass


def object_matches(key, only, _except):
    pass


def parallelize(bucket, only, _except, fn, args=(), versions=False):
    pass


def public_statement(bucket):
    pass


def no_object_acl_statement(bucket):
    pass


def public_uploads_statement(bucket):
    pass


def no_uploads_statement(bucket):
    pass


def encryption_statement(bucket):
    pass


def statement_matches(s1, s2):
    pass


def fetch_policy(bucket):
    pass


def print_dns_bucket(name, buckets, found_buckets):
    pass


def print_policy(policy):
    pass


def summarize(values):
    pass


def fetch_event_selectors():
    # TODO get trails across all regions
    # even regions without buckets may have multi-region trails
    pass


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.argument('buckets', nargs=-1)
@click.option('--log-bucket', multiple=True, help='Check log bucket(s)')
@click.option('--log-prefix', help='Check log prefix')
@click.option('--skip-logging', is_flag=True, help='Skip logging check')
@click.option('--skip-versioning', is_flag=True, help='Skip versioning check')
@click.option('--skip-default-encryption', is_flag=True, help='Skip default encryption check')
@click.option('--default-encryption', is_flag=True)  # no op, can't hide from help until click 7 released
@click.option('--object-level-logging', is_flag=True)
@click.option('--sns-topic', help='Send SNS notification for failures')
def scan(buckets, log_bucket=None, log_prefix=None, skip_logging=False, skip_versioning=False, skip_default_encryption=False, default_encryption=True, object_level_logging=False, sns_topic=None):
    pass


@cli.command(name='scan-dns')
def scan_dns():
    pass


@cli.command(name='block-public-access')
@click.argument('buckets', nargs=-1)
@click.option('--dry-run', is_flag=True, help='Dry run')
def block_public_access(buckets, dry_run=False):
    pass


@cli.command(name='enable-logging')
@click.argument('buckets', nargs=-1)
@click.option('--dry-run', is_flag=True, help='Dry run')
@click.option('--log-bucket', required=True, help='Bucket to store logs')
@click.option('--log-prefix', help='Log prefix')
def enable_logging(buckets, log_bucket=None, log_prefix=None, dry_run=False):
    pass


@cli.command(name='enable-versioning')
@click.argument('buckets', nargs=-1)
@click.option('--dry-run', is_flag=True, help='Dry run')
def enable_versioning(buckets, dry_run=False):
    pass


@cli.command(name='enable-default-encryption')
@click.argument('buckets', nargs=-1)
@click.option('--dry-run', is_flag=True, help='Dry run')
def enable_default_encryption(buckets, dry_run=False):
    pass


@cli.command()
@click.argument('bucket')
@click.option('--only', help='Only certain objects')
@click.option('--except', '_except', help='Except certain objects')
@click.option('--dry-run', is_flag=True, help='Dry run')
@click.option('--kms-key-id', help='KMS key id')
@click.option('--customer-key', help='Customer key')
def encrypt(bucket, only=None, _except=None, dry_run=False, kms_key_id=None, customer_key=None):
    pass


@cli.command(name='scan-object-acl')
@click.argument('bucket')
@click.option('--only', help='Only certain objects')
@click.option('--except', '_except', help='Except certain objects')
def scan_object_acl(bucket, only=None, _except=None):
    pass


@cli.command(name='reset-object-acl')
@click.argument('bucket')
@click.option('--only', help='Only certain objects')
@click.option('--except', '_except', help='Except certain objects')
@click.option('--acl', default='private', help='ACL to use')
@click.option('--dry-run', is_flag=True, help='Dry run')
def reset_object_acl(bucket, only=None, _except=None, acl=None, dry_run=False):
    pass


@cli.command(name='delete-unencrypted-versions')
@click.argument('bucket')
@click.option('--only', help='Only certain objects')
@click.option('--except', '_except', help='Except certain objects')
@click.option('--dry-run', is_flag=True, help='Dry run')
def delete_unencrypted_versions(bucket, only=None, _except=None, dry_run=False):
    pass


@cli.command(name='list-policy')
@click.argument('buckets', nargs=-1)
@click.option('--named', is_flag=True, help='Print named statements')
def list_policy(buckets, named=False):
    pass


@cli.command(name='set-policy')
@click.argument('bucket')
@click.option('--public', is_flag=True, help='Make all objects public')
@click.option('--no-object-acl', is_flag=True, help='Prevent object ACL')
@click.option('--public-uploads', is_flag=True, help='Only public uploads')
@click.option('--no-uploads', is_flag=True, help='Prevent new uploads')
@click.option('--encryption', is_flag=True, help='Require encryption')
@click.option('--dry-run', is_flag=True, help='Dry run')
def set_policy(bucket, public=False, no_object_acl=False, public_uploads=False, no_uploads=False, encryption=False, dry_run=False):
    pass


# experimental
@cli.command(name='update-policy')
@click.argument('bucket')
@click.option('--encryption/--no-encryption', default=None, help='Require encryption')
@click.option('--dry-run', is_flag=True, help='Dry run')
def update_policy(bucket, encryption=None, dry_run=False):
    pass


@cli.command(name='delete-policy')
@click.argument('bucket')
def delete_policy(bucket):
    pass


def main():
    pass
