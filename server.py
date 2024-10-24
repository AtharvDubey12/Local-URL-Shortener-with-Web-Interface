import asyncio
import json
import subprocess
import time
import urllib.request
import sys

def internetcheck():
    try:
        urllib.request.urlopen("https://www.google.com", timeout= 5)
        return True
    except:
        return False
    

list= ['websockets']
for lib in list:
    try:
        __import__(lib)
    except ImportError:
        print(f"{lib} library is not available! please wait while we install it for you.")
        if internetcheck():
            print(f"An active internet connection has been detected, proceeding to install {lib} library")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"{lib} installed!")
        else:
            print("Internet connection not detected! please turn on the internet so that we can install missing libraries.")
            while True:
                if internetcheck():
                    print("internet connection established! proceeding to download missing libraries")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                    print(f"{lib} installed!")
                    break
                else:
                    end= int(input("enter 900 to end program, any other integer to resume (you'll need internet though!)"))
                    if end==900:
                        loopbreaker=0
                        break
                    else:
                        time.sleep(5)

import websockets
  
async def handler(websocket, path):
    async for message in websocket:
        data= json.loads(message)
        long_url= data.get("long_url","")
        if (long_url !="") and ("." in long_url):
            print(f"received long url: {long_url}")
            process= subprocess.Popen(["./main.exe", long_url], stdout=subprocess.PIPE, stderr= subprocess.PIPE)
            output, error= process.communicate()

            response= {"output": output.decode().strip(), "error": error.decode().strip()}
            await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        print("websocket server started on ws://localhost:8000")
        await asyncio.Future()

if __name__=="__main__":
    asyncio.run(main())