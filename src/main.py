"""Module main.py"""
import logging
import os
import sys

import boto3


def main():
    """
    Entry Point

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('EVENTS')

    # Assets
    # src.assets.Assets(s3_parameters=s3_parameters).exc()
    reference = src.data.interface.Interface(s3_parameters=s3_parameters).exc()
    reference.info()

    # src.drift.interface.Interface(reference=reference, arguments=arguments).exc()


    # Delete Cache Points
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.data.interface
    import src.drift.interface
    import src.functions.cache
    import src.preface.interface
    import src.elements.service as sr
    import src.elements.s3_parameters as s3p
    import src.assets

    connector: boto3.session.Session
    s3_parameters: s3p
    service: sr.Service
    arguments: dict
    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc()

    main()
