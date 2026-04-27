import json
import botocore


class Check:
    def __init__(self, bucket, **kwargs):
        self.bucket = bucket
        self.options = kwargs

    def perform(self):
        pass

    def fix(self, options):
        pass


class AclCheck(Check):
    name = 'ACL'
    pass_message = 'not open to public'
    fail_message = 'open to public'
    bad_grantees = [
        'http://acs.amazonaws.com/groups/global/AllUsers',
        'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'
    ]

    def _passed(self):
        pass


class PolicyCheck(Check):
    name = 'Policy'
    pass_message = 'not open to public'
    fail_message = 'open to public'

    def _passed(self):
        pass


class PublicAccessCheck(Check):
    name = 'Public access'
    pass_message = 'blocked'
    fail_message = 'not explicitly blocked'

    def _passed(self):
        pass

    def _fix(self, options):
        pass


class LoggingCheck(Check):
    name = 'Logging'
    pass_message = 'enabled'
    fail_message = 'disabled'

    def _passed(self):
        pass

    def _fix(self, options):
        pass


class VersioningCheck(Check):
    name = 'Versioning'
    pass_message = 'enabled'
    fail_message = 'disabled'

    def _passed(self):
        pass

    def _fix(self, options):
        pass


class EncryptionCheck(Check):
    name = 'Default encryption'
    pass_message = 'enabled'
    fail_message = 'disabled'

    def _passed(self):
        pass

    def _fix(self, options):
        pass


class ObjectLoggingCheck(Check):
    name = 'CloudTrail object-level logging'
    pass_message = 'enabled'
    fail_message = 'disabled'

    def _passed(self):
        pass
