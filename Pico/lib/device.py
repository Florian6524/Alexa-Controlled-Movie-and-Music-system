import machine
import time
import urequests

led = machine.Pin("LED", machine.Pin.OUT)
led2 = machine.Pin(2, machine.Pin.OUT)

url1 = "http://andreistefanescu.com:3000/movie"
url2 = "http://andreistefanescu.com:3000/music"

def TurnOnIntent():
    led.on()
    
def TurnOffLedIntent():
    led.off()
    
def PlayMovieIntent():
    led2.on()
    response = urequests.get(url1)

    print("Status:", response.status_code)
    print("Response:")
    print(response.text)

    response.close()
    led2.off()
    
def PlaySongIntent():
    led2.on()
    response = urequests.get(url2)

    print("Status:", response.status_code)
    print("Response:")
    print(response.text)

    response.close()
    led2.off()
    
    
    


