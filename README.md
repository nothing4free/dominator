```
     888                        d8b                   888                    
     888                        Y8P                   888                    
     888                                              888                    
 .d88888  .d88b.  88888b.d88b.  888 88888b.   8888b.  888888 .d88b.  888d888 
d88" 888 d88""88b 888 "888 "88b 888 888 "88b     "88b 888   d88""88b 888P"   
888  888 888  888 888  888  888 888 888  888 .d888888 888   888  888 888     
Y88b 888 Y88..88P 888  888  888 888 888  888 888  888 Y88b. Y88..88P 888     
 "Y88888  "Y88P"  888  888  888 888 888  888 "Y888888  "Y888 "Y88P"  888     [dev]  
```
Closely monitor, inspect and save a history of changes on hosts and domains.<br>
Made with <3 by n4free :)

## What is Dominator?

Dominator is a tool that you can use to monitor DNS changes through time on a domain. It is meant to be ran on a server or a computer constantly turned on with Internet access, as it runs periodically. <br>

This tool is on a functional alpha state, given that its core functionality (DNS monitoring) currently works, but many changes and additions will be introduced.

## Installation and use

<b>No sudo permissions are required for the setup. It is not recommended to run these steps as sudo.</b><br>
First, clone this repository on the server you want to install this tool in:

```git clone https://github.com/nothing4free/dominator```

Then, run the setup script. This script will set up the cron job that will execute the DNS lookups periodically.<br>
```python3 setup.py```

Once this has been done, the tool will be ready for its use. In order to access its CLI, run the ```dominator.py``` script:<br>

```python3 dominator.py```

Once it runs, make sure to add a new domain target. You can add as many domains as you want; these are the domains that will be periodically checked.<br>


It is designed in a way that the ```engine.py``` and ```exec.py``` files are not meant to be manually ran, but if you wish to perform a quick DNS lookup you can do so in the following way:<br>

```python3 engine.py <domain.tld>```

