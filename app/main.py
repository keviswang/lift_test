import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)



if __name__ == '__main__':
    logger = logging.getLogger(__file__)

    logger.info('ssss')