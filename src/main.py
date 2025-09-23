"""Module main.py"""
import datetime
import logging
import os
import sys

import boto3
import geopandas


def main():
    """
    Entry Point

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    # Investigate Warnings
    frame: geopandas.GeoDataFrame = src.cartography.interface.Interface(
        connector=connector, arguments=arguments, s3_parameters=s3_parameters).exc()

    # Update the warnings data library
    state: bool = src.updating.Updating(
        service=service, s3_parameters=s3_parameters).exc(frame=frame)

    # Hence, orchestrate and launch a system
    if state:
        src.compute.interface.Interface(
            connector=connector, arguments=arguments).exc(
            starting=frame['starting'].min(), ending=frame['ending'].max())

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
    import src.elements.service as sr
    import src.elements.s3_parameters as s3p
    import src.compute.interface
    import src.functions.cache
    import src.preface.interface
    import src.cartography.interface
    import src.updating

    connector: boto3.session.Session
    s3_parameters: s3p
    service: sr.Service
    arguments: dict
    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc()

    main()
