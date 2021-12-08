import jetson.inference
import jetson.utils
import asyncio
from bleak import BleakClient
from bleak import discover
from neosensory_python import NeoDevice
from time import sleep

net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold=0.8)
camera = jetson.utils.gstCamera(1280, 720, '/dev/video0')
display = jetson.utils.glDisplay()

# For haptic link debugging
# def notification_handler(sender, data):
#     print("{0}: {1}".format(sender, data))


async def run(loop):
    buzz_addr = "C7:6D:2E:06:83:39"
    devices = await discover()
    async with BleakClient(buzz_addr,loop=loop) as client:
        my_buzz = NeoDevice(client)
        await asyncio.sleep(1)
        x = await client.is_connected()
        print("Connection State: {0}\r\n".format(x))
#             await my_buzz.enable_notifications(notification_handler)
        await asyncio.sleep(1)
        await my_buzz.request_developer_authorization()
        await my_buzz.accept_developer_api_terms()
        await my_buzz.pause_device_algorithm()
        motor_vibrate_frame = [0, 0, 0, 0]
        motor_pattern_index = 0
        motor_pattern_value = 0
        intensity = 255
        light_intensity = 51
        delay = 0.01
        qdelay = 0.002


        async def motor_vehicle_pattern():
            await my_buzz.vibrate_motors([intensity, 0, 0, intensity])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)


        async def busy_intersection_pattern():
            await my_buzz.vibrate_motors([intensity, intensity, intensity, intensity])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, intensity, intensity, 0])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
          
          
        async def person_pattern():
            await my_buzz.vibrate_motors([intensity, intensity, 0, 0])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, 0, intensity, intensity])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
        
        
        async def toilet_pattern():
            await my_buzz.vibrate_motors([light_intensity, 0, light_intensity, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, light_intensity, 0, light_intensity])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)


        async def computer_pattern():
            await my_buzz.vibrate_motors([intensity, 0, 0, intensity])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)


        async def kitchen_utensils_pattern():
            await my_buzz.vibrate_motors([intensity, intensity, intensity, intensity])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, intensity, intensity, 0])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
        
        
        async def diningware_pattern():
            await my_buzz.vibrate_motors([intensity, intensity, 0, 0])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, 0, intensity, intensity])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)


        async def rest_place_pattern():
            await my_buzz.vibrate_motors([light_intensity, 0, light_intensity, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, light_intensity, 0, light_intensity])
            sleep(qdelay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            sleep(qdelay)
            
        async def cell_phone_pattern():
            await my_buzz.vibrate_motors([light_intensity,light_intensity,light_intensity,light_intensity])
            await my_buzz.vibrate_motors([light_intensity,light_intensity,light_intensity,light_intensity])
            sleep(delay)
            await my_buzz.vibrate_motors([0, 0, 0, 0])
            await my_buzz.vibrate_motors([0, 0, 0, 0])


        try:
            while True:
                await asyncio.sleep(0.1)
                while display.IsOpen():
                    img, width, height = camera.CaptureRGBA()
                    detections = net.Detect(img, width, height)
                    display.RenderOnce(img, width, height)
                    display.SetTitle("Object Detection | NEtwork {:0f} FPS".format(net.GetNetworkFPS()))
#                       Frame rate limiter to avoid excessive haptic feedback triggering
                    sleep(0.5)
#                       Similar objects are grouped together until the user's brain has adapted,
#                       upon which more distinct, specific groupings can be made
                    for detection in detections:
                        if detection.ClassID == 1:
                            print('human')
                            await person_pattern()
                        elif detection.ClassID == 3:
                            print('car')
                            await motor_vehicle_pattern()
                        elif detection.ClassID == 4:
                            print('motorcycle')
                            await motor_vehicle_pattern()
                        elif detection.ClassID == 6:
                            print('bus')
                            await motor_vehicle_pattern()
                        elif detection.ClassID == 8:
                            print('truck')
                            await motor_vehicle_pattern()
                            
                        elif detection.ClassID == 10:
                            print('traffic light')
                            await busy_intersection_pattern()
                        elif detection.ClassID == 13:
                            print('stop sign')
                            await busy_intersection_pattern()
                            
                        elif detection.ClassID == 72:
                            print('monitor')
                            await computer_pattern()
                        elif detection.ClassID == 73:
                            print('laptop')
                            await computer_pattern()
                        elif detection.ClassID == 74:
                            print('mouse')
                            await computer_pattern()
                        elif detection.ClassID == 76:
                            print('keyboard')
                            await computer_pattern()
                        elif detection.ClassID == 77:
                            print('cell phone')
                            await cell_phone_pattern()
                            
                        elif detection.ClassID == 48:
                            print('fork')
                            await kitchen_utensils_pattern()
                        elif detection.ClassID == 49:
                            print('knife')
                            await kitchen_utensils_pattern()
                        elif detection.ClassID == 50:
                            print('spoon')
                            await kitchen_utensils_pattern()
                            
                        elif detection.ClassID == 45:
                            print('plate')
                            await diningware_pattern()
                        elif detection.ClassID == 47:
                            print('cup')
                            await diningware_pattern()
                        elif detection.ClassID == 51:
                            print('bowl')
                            await diningware_pattern()

                        elif detection.ClassID == 15:
                            print('bench')
                            await rest_place_pattern()
                        elif detection.ClassID == 62:
                            print('chair')
                            await rest_place_pattern()
                        elif detection.ClassID == 63:
                            print('couch')
                            await rest_place_pattern()
                        elif detection.ClassID == 65:
                            print('bed')
                            await rest_place_pattern()
                        
                        elif detection.ClassID == 70:
                            print('toilet')
                            await toilet_pattern()
            
        except KeyboardInterrupt:
            await my_buzz.resume_device_algorithm()
            pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))