import paho.mqtt.client as mqtt



client = mqtt.Client()

client.connect("localhost", 1883, 60)

client.publish("test/a", "hello")
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
