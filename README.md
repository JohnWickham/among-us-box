# Among Us Box
### The light switch task from Among Us that sabotages your lights for real

## Installation
```
$ pip3 install pygame

$ sudo apt-get install libavahi-compat-libdnssd-dev
$ sudo pip3 install HAP-python HAP-python[QRCode]
```

## Starting at boot

1. Create a file at `/etc/systemd/system/among-us-box.service` with this:

  ```
  [Unit]
  Description=Among Us Sabotage Box
  After=network.target network-online.target
  
  [Service]
  Type=simple
  ExecStart=/user/bin/python3 /home/john/among-us-box/main.py
  
  [Install]
  WantedBy=multi-user.target
  ```
  
  This creates a systemd service that runs the script as a daemon process.

2. Enable the service with `sudo systemctl enable among-us-box`.

## Troubleshooting

If the volume of sound effects seems too low, try running `sudo amixer cset numid=1 70%` (after checking any hardware volume controls, of course).