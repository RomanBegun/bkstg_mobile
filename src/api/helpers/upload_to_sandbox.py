import os.path
import mimetypes
import time

import botocore.session

from setuptools.compat import unicode
from uuid import uuid4


class Upload:

    @staticmethod
    def upload_to_sandbox(path):

        print('File \'%s\' uploading started...' % path.replace('api/test/../../', ''))

        start_time = str(int(time.time()))

        session = botocore.session.get_session()
        session.set_credentials(access_key="AKIAIA5IPHVWBGQSSBBA",
                                secret_key="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")

        client = session.create_client('s3', region_name='us-west-2')
        f = open(path, 'rb')

        key = '/'.join(unicode(uuid4()).split('-') + [os.path.basename(path)])

        response = client.put_object(
            Body=f.read(),
            Bucket='bkstg-sandbox',
            Key=key,
            ContentType=mimetypes.guess_type(path)[0]
        )

        end_time = str(int(time.time()))
        print('File was uploaded in %s seconds.\n' % (int(end_time) - int(start_time)))

        return key

# if __name__ == '__main__':
#     Upload.upload_to_sandbox(path=TestData.image_path)