# Onyx

[![Build Status](https://travis-ci.org/OnyxProject/Onyx.svg?branch=master)](https://travis-ci.org/OnyxProject/Onyx)

![Alt](http://nsa38.casimages.com/img/2017/06/08/17060809355462415.png)

**Website :** [https://onyxlabs.fr](https://onyxlabs.fr)

## Project

Onyx aims to simplify your life, its primary goal is to bring everything together in one place.

Want to check your emails, add appointments, have the weather and set your alarm clocks at the same time? This is the goal of Onyx, to centralize everything.

You go home, you start your computer and your home page is Onyx, then you connect with your personal account and you come across your homepage filled with your widgets that you have chosen beforehand

You decide to launch your favorite music while you check your mails on the mailbox.

Then you will program your alarm clock for the next day with your favorite music to wake you up

The next day, Onyx wakes you up with your music and tells you the time and weather of the day so you can dress up the right way, and gives you your appointments of the day that come directly from your Google account !

## Specifications

Onyx is written in Python with the framework Flask
It use the MycroftAi Skill System for a better experience

## Prerequisites

All Prerequisites are in the install_debian_script.sh and dev_setup.sh


## Getting Started

The easiest way to install onyx on a Raspberry Pi is to download the Onyx Installer directly from ou website : [https://onyxlabs.fr](https://onyxlabs.fr)

Or to install Onyx manually to contribute :

```bash
git clone https://github.com/OnyxProject/Onyx onyx
```

```bash
cd onyx
```

```bash
sudo bash install_debian_script.sh
```

```bash
bash setup.py
```

That's it !

## Running Onyx Quick Start

To start the essential of Onyx run `./onyx.sh start`. This will open all service (service, skills, client and voice) and after you can see the log of each service in the log folder (e.g. ./log/onyx-service.log).

To stop Onyx run `./onyx.sh stop`. This will quit all screens.
Finally to restart Onyx run './onyx.sh restart`.

Quick screen tips
- run `screen -list` to see all running screens
- run `screen -r [screen-name]` (e.g. `screen -r onyx-service`) to reatach a screen
- to detach a running screen press `ctrl + a, ctrl + d`
See the screen man page for more details

## Start each service manually

You can use the `./start.sh` script !
It use virtualenv so you must execute the `dev_setup.sh` before.
To use it just do this :

- run `./start.sh service`
- run `./start.sh client`
- run `./start.sh skills`
- run `./start.sh voice`

# FAQ/Common Errors

#### When running onyx, I get the error `onyx.messagebus.client.ws - ERROR - Exception("Uncaught 'error' event.",)`

This means that you are not running the `./start.sh service` process. In order to fully run Onyx, you must run `./start.sh service`, `./start.sh skills`, `./start.sh voice` and `./start.sh client` all at the same time. This can be done using different terminal windows, or by using the included `./onyx.sh start`, which runs all four process using `screen`.

## Links

- [Website](http://onyxlabs.fr)
- [Blog](http://onyxlabs.fr/blog)
- [Forum](http://community.onyxlabs.fr)

## Social Media

[![Github](https://github.frapsoft.com/social/github.png)](https://github.com/OnyxProject/Onyx)[![Docker](https://github.frapsoft.com/social/docker.png)](https://hub.docker.com/r/onyxproject/onyx/)[![Twitter](https://github.frapsoft.com/social/twitter.png)](https://twitter.com/LabsOnyx)[![Facebook](https://github.frapsoft.com/social/facebook.png)](https://www.facebook.com/LabsOnyx/)
