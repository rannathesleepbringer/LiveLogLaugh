# LiveLogLaugh
The worst option for logging in Python
Thank you MCodingLLC for the terrible idea, since he said not to do this.

## Extract and install the library using:
```
python -m pip install -e liveloglaugh
```
## Copy configs
Currently you should copy both json config files to your root directory of your project. You can use just the queued-stderr-file.json if you are on Python 12 or above.


## Import the library and add to your function as a decorator
``` 
from liveloglaugh import love
@love
def Function():
  print("test")

```
## Logs will be saved based on the config placed next to your project file
