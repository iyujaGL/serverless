import json
import logging
import sys
import ldclient
import os


def flag(event, context):

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    ldclient.set_sdk_key(os.environ['SDKKEY'])

    user = {
      "key": "ivan.yuja@gorillalogic.com",
      "firstName": "Ivan",
      "lastName": "Yuja",
      "custom": {
        "groups": "beta_testers"
      }
    }

    flag_hoisted = ldclient.get().variation("flag-hoisted", user, False)

    if flag_hoisted:
      flag_status = "Hoisted"
    else:
      flag_status = "Lowered"

    ldclient.get().close() # close the client before exiting the program - ensures that all events are delivered


    body = {
        "message": flag_status
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
