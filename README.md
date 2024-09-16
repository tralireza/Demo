# NetConf Demo

### Build

```bash
$ docker build -t app .
```

### Start

```bash
$ docker compose up
```

## REST endpoints

```bash
Endpoint          Methods  Rule
----------------  -------  -------------------------
alive             GET      /alive
cli.ifs           GET      /cli/ifs
cli.version       GET      /cli/version
config            GET      /config
dryrun            GET      /dryrun
mod_nc.lifCreate  POST     /netconf/lfs
mod_nc.lifDelete  DELETE   /netconf/lfs/<int:number>
```

## Access
Nginx is running on port 8000, WSGI(flask) app is on 5000.
```bash
$ curl http://127.0.0.1:8000/alive
{
  "alive": true
}
$ curl http://127.0.0.1:8000/config
{
  "HOST": "sandbox-iosxr-1.cisco.com",
  "USR": "admin",
  "PASSWD": "C1sco12345"
}
$ curl http://127.0.0.1:8000/cli/version

Mon Sep 16 03:30:28.937 UTC
Cisco IOS XR Software, Version 7.3.2
Copyright (c) 2013-2021 by Cisco Systems, Inc.

Build Information:
 Built By     : ingunawa
 Built On     : Wed Oct 13 20:00:36 PDT 2021
 Built Host   : iox-ucs-017
 Workspace    : /auto/srcarchive17/prod/7.3.2/xrv9k/ws
 Version      : 7.3.2
 Location     : /opt/cisco/XR/packages/
 Label        : 7.3.2-0

cisco IOS-XRv 9000 () processor
System uptime is 1 week 5 days 13 hours 43 minutes
$ curl http://127.0.0.1:8000/cli/ifs

Mon Sep 16 03:30:57.262 UTC

               Intf       Intf        LineP              Encap  MTU        BW
               Name       State       State               Type (byte)    (Kbps)
--------------------------------------------------------------------------------
                Lo1          up          up           Loopback  1500          0
               Lo66          up          up           Loopback  1500          0
               Lo83          up          up           Loopback  1500          0
               Lo88          up          up           Loopback  1500          0
              Lo100          up          up           Loopback  1500          0
              Lo101          up          up           Loopback  1500          0
              Lo102          up          up           Loopback  1500          0
              Lo200          up          up           Loopback  1500          0
              Lo220          up          up           Loopback  1500          0
              Lo222          up          up           Loopback  1500          0
              Lo300          up          up           Loopback  1500          0
              Lo333          up          up           Loopback  1500          0
             Lo3434          up          up           Loopback  1500          0
                Nu0          up          up               Null  1500          0
     Mg0/RP0/CPU0/0          up          up               ARPA  1514    1000000
          Gi0/0/0/0        down        down               ARPA  1514    1000000
          Gi0/0/0/1  admin-down  admin-down               ARPA  1514    1000000
          Gi0/0/0/2        down        down               ARPA  1514    1000000
          Gi0/0/0/3        down        down               ARPA  1514    1000000
          Gi0/0/0/4        down        down               ARPA  1514    1000000
          Gi0/0/0/5  admin-down  admin-down               ARPA  1514    1000000
          Gi0/0/0/6  admin-down  admin-down               ARPA  1514    1000000

```

## Tests
```bash
(.venv) $ pytest
===================================== test session starts ============================================
platform darwin -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/alireza/python/Sky
collected 10 items

app_test.py ...                                                                                 [ 30%]
dispatcher_test.py ..                                                                           [ 50%]
mod_cli_test.py ...                                                                             [ 80%]
mod_nc_test.py ...                                                                              [100%]

======================================== 10 passed in 21.47s =========================================
```
