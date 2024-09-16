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

## Tests
```bash
(.venv) $ pytest
=========================================== test session starts ============================================
platform darwin -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/alireza/python/Sky
collected 10 items

app_test.py ...                                                                                                          [ 30%]
dispatcher_test.py ..                                                                                                    [ 50%]
mod_cli_test.py ...                                                                                                      [ 80%]
mod_nc_test.py ..                                                                                                        [100%]

=========================================== 10 passed in 21.47s ============================================
```
