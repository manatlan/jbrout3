My attempt to port the good old [jbrout/py2/gtk](https://manatlan.com/jbrout/) to python3/wuy's web app.

Currently, it's in pre-alpha stage : USE AT YOUR OWN RISK ;-)

The idea : The old jbrout used gtk with python2 (there are a lot of works to port it to python3, with gobject changes). This version use [wuy](https://github.com/manatlan/wuy), which will make it completly independant of the OS. It will reuse your chrome installation, to run a windowed version of jbrout. The frontend is full html/js/css, using vuejs + vuex. It communicates with the serverside thru a websocket. The serverside use the good olds python apis.

BTW, it will be possible to use [cefpython3](https://github.com/cztomczak/cefpython), to make a standalone version. And it will be possible to run jbrout headless (server mode), and use it thru any browsers (but we will need to handle session/multi-users).

Currently, it uses the simplest way : you will need to have a chrome/chromium installed.

With some little changes : "the path to your jbrout/conf", you should be able to test it against your old conf (except the jbrout.conf). It works !

To run it :

In your env:

    $ git clone https://github.com/manatlan/jbrout3.git
    $ cd jbrout3
    $ python3 -m pip install -r requirements.txt
    $ python3 jbrout.py

In a python3's virtualenv:

    $ python3 -m venv FOLDER
    $ cd FOLDER
    $ source bin/activate
    $ git clone https://github.com/manatlan/jbrout3.git
    $ cd jbrout3
    $ python3 -m pip install -r requirements.txt
    $ python3 jbrout.py

On Windows:

    install "jpegtran.exe" (will be embedded in the futur/final executable)

On others OS:

    sudo apt-get install exiftran
