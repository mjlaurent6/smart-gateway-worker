import random
from paho.mqtt import client as mqtt_client
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
load_dotenv()


def get_database():
    client = MongoClient(os.environ.get("DB_URL"), tlsCAFile=certifi.where())
    return client[os.environ.get("DB_NAME")]


db = get_database()

broker = 'broker.emqx.io'
port = 1883
topic = "gateway/eui/status"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            print(msg.payload)
            message = json.loads(msg.payload.decode())
            doc = db['gateway-status-history'].insert_one(message)
        except:
            db['gateway-status-history'].insert_one(msg.payload)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
