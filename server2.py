import sys
import urllib.request
import subprocess
import time

def internetcheck():
    try:
        urllib.request.urlopen("https://www.google.com", timeout= 5)
        return True
    except:
        return False
    

list= ['flask']
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




from flask import Flask, redirect, abort
app = Flask(__name__)


def load_mappings():
    url_mappings={}
    with open('udb.txt','r') as file:
        for line in file:
            long_url, short_url, _=line.strip().split(',')
            if not long_url.startswith(('https://', 'http://')):
                long_url= "https://" + long_url
                url_mappings[short_url]=long_url
            else:
                url_mappings[short_url]=long_url

    return url_mappings

load_mappings()

@app.route('/<short_url>')
def redirect_to_long(short_url):
    url_mappings= load_mappings()
    long_url= url_mappings.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return abort(404)

if __name__=='__main__':
    app.run(debug=False)
