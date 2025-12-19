import device, lib.keys as keys, machine, network, ntptime, lib.simple as simple, ssl, time, ubinascii

listen_counter = 0

def read_pem(file):
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])
        return ubinascii.a2b_base64(base64_text)

def internet_connect(net):
    print("Connecting to WiFi ...")
    net.active(True)
    net.connect(keys.WIFI_SSID, keys.WIFI_PASSWORD)
    while not net.isconnected():
        time.sleep(1)
    print("Connected to WiFi\n")

def mqtt_callback(topic, msg):
    topic_str = topic.decode()
    msg_str = msg.decode().strip('"')
    print(f"RX: {topic_str}\t{msg_str}")
    if hasattr(device, msg_str):
        getattr(device, msg_str)()

def mqtt_setup():
    mqtt_client = simple.MQTTClient(
        client_id = ubinascii.hexlify(machine.unique_id()),
        server = keys.MQTT_BROKER,
        ssl = True,
        ssl_params = {
            "key": read_pem(keys.MQTT_CLIENT_KEY),
            "cert": read_pem(keys.MQTT_CLIENT_CERT),
            "server_hostname": keys.MQTT_BROKER,
            "cert_reqs": ssl.CERT_REQUIRED,
            "cadata": read_pem(keys.MQTT_BROKER_CA),
        },
    )
    mqtt_client.set_callback(mqtt_callback)
    return mqtt_client

def mqtt_connect(client):
    print("Connecting to MQTT Broker ...")
    client.connect()
    client.subscribe(keys.MQTT_TOPIC)
    print("Connected to MQTT Broker\n")

def mqtt_listen(client):
    global listen_counter

    client.check_msg()
    listen_counter = (listen_counter + 1) % 30
    
    if (listen_counter == 0):
        client.publish(keys.MQTT_TOPIC, "keep_alive")
    
    time.sleep(1)

def mqtt_disconnect(client):
    print("Disconnecting from MQTT Broker ...")
    client.disconnect()
    print("Disconnected from MQTT Broker\n")

wlan = network.WLAN(network.STA_IF)
while True:
    internet_connect(wlan)
    ntptime.settime()
    mqtt_client = mqtt_setup()
    mqtt_connect(mqtt_client)
    print(f"Listening to {keys.MQTT_TOPIC} ...")
    while wlan.isconnected():
        mqtt_listen(mqtt_client)

