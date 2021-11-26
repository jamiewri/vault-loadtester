import logging
import argparse
import base64
import random
import requests
import json

def startLogging(verbosity):
    """
    Initilize logging configuration to correct verbosity
    """

    if verbosity == 1:
      logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s - %(message)s',
                          datefmt='%d-%b-%y %H:%M:%S',
                          level=logging.INFO)
      logging.info('Log level set to INFO')

    elif verbosity == 2:
      logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s - %(message)s',
                          datefmt='%d-%b-%y %H:%M:%S',
                          level=logging.DEBUG)
      logging.debug('Log level set to DEBUG')
    else:
      logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s - %(message)s',
                          datefmt='%d-%b-%y %H:%M:%S',
                          level=logging.WARNING)
      logging.warning('Log level set to WARNING')

def argParser():
    """
    Parse argument passed on the command line, setting default where required.
    """

    parser = argparse.ArgumentParser(description='Non-Function Load Testing of Vault')
  
    parser.add_argument('--threads', 
                        action='store',
                        default=10,
                        help='How many threads should be used.',
                        nargs='?', 
                        type=int,
                        )

    parser.add_argument('--key', 
                        action='store', 
                        default='randomKey',
                        help='What is the name of the encryption key to use.',
                        nargs='?', 
                        type=str, 
                        )

    parser.add_argument('--path', 
                        action='store', 
                        default='transit',
                        help='Transit path',
                        nargs='?', 
                        type=str, 
                        )

    parser.add_argument('--duration', 
                        action='store', 
                        default=10,
                        help="Duration of the test",
                        nargs='?', 
                        type=int, 
                        )


    parser.add_argument('-v',
                        '--verbosity',
                        action='count',
                        default=0,
                        help="Increase logging verbosity with more --vv",
                        )
    return parser

def generateCreditCardNumbers(items):
    """
    Generate sudo credit cards numbers
    """

    data = []

    for x in range(items):
      item = []

      for y in range(4):
        block = random.randint(1000,9999)
        block = str(block)
        item.append(block)

      creditCardNumber = '-'.join(item)
      encodedCreditCardNumber = base64EncodeString(creditCardNumber)
      data.append(encodedCreditCardNumber)

    return data

def base64EncodeString(data):
    """
    Return base64 coded string
    """

    dataBytes = data.encode('ascii')
    base64Bytes = base64.b64encode(dataBytes)
    base64String = base64Bytes.decode('ascii')
  
    return base64String

def checkMount(vaultClient, path):
    """
    Check if there is anything mounted a the supplied path
    """

    url = vaultClient.addr + '/v1/sys/mounts'
    response = requests.get(url=url, headers=vaultClient.vaultHeaders)
    responseJson = response.json()
  
    for i in responseJson['data']:
      if i == path + '/':
        logging.info(path + '/ is already mounted')
        return True
    logging.info('There is nothing mounted at ' + path) 
    return False


def createMount(vaultClient, path, secretsEngine):
    """
    Check if something is already mounted at the supplied path, if not
    mount a secrets engine there
    """

    mountExists = checkMount(vaultClient, path)
    if not mountExists:
      url = vaultClient.addr + '/v1/sys/mounts/' + path
      payload = {'type': secretsEngine}
      response = requests.post(url=url, headers=vaultClient.headers, data=json.dumps(payload))
      logging.info('A ' + secretsEngine + ' secrets engine has been mounted at ' + path)

