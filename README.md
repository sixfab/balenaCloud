## A Simple Server for using Sixfab GPS Shield with Python

This is a simple using Sixfab GPS Shield project that works on any of the devices supported by [balena][balena-link].

To get this project up and running, you will need to signup for a balena account [here][signup-page] and set up a device, have a look at our [Getting Started tutorial][gettingStarted-link]. Once you are set up with balena, you will need to clone this repo locally:
```
$ git clone https://github.com/sixfab/balenaCloud.git
```
Then add your balena application's remote:
```
$ git remote add balena username@git.balena-cloud.com:username/myapp.git
```
and push the code to the newly added remote:
```
$ git push balena master
```
It should take a few minutes for the code to push. While you wait, lets enable device URLs so we can see the server outside of our local network. This option can be toggled on the device summary page, pictured below or in the `Actions` tab in your device dashboards.

Then at your balena logs you should be able to see the Gps outputs.

```
NOTE : Please enable uart from balena device configuration page! ( Screenshot : ![Enable Uart](https://raw.githubusercontent.com/sixfab/balenaCloud/master/enable_uart.png) )
```


[balena-link]:https://balena.io/
[signup-page]:https://dashboard.balena-cloud.com/signup
[gettingStarted-link]:http://balena.io/docs/learn/getting-started/
