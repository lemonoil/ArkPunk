# ArkPunk

> A Real-Time GameData Display Tool for Arknights

### versions

About Node_modules you can see them in package.json
> socketio.__version__ = '4.3.0'
>
> flask.__version__ = '1.1.2'
>
> frida.__version__ = '12.11.18'

### Install

#### Client Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:9080
npm run dev

# build electron application for production
npm run build


```

#### Hook Setup

> Install the same version frida & frida-serve
>
> pip all what you need (advice: python-socketio needs to match with the socket.io-client)
>
> run frida-serve on your device as root
>
> you can also use adb to connect your device (as MuMu, try `adb connect 127.0.0.1:7555`)
>
> 

### Update the Offset by yourself

Just renew the address offset: `n_addr_func_offset` of `entity_appliedmodifier` and ` nosourcedamage` function in `app.py`.
The first version(1.0.1) of this tool matches with arknights(1280)

### License MIT


---

This project was generated with [electron-vue](https://github.com/SimulatedGREG/electron-vue)@[45a3e22](https://github.com/SimulatedGREG/electron-vue/tree/45a3e224e7bb8fc71909021ccfdcfec0f461f634) using [vue-cli](https://github.com/vuejs/vue-cli). Documentation about the original structure can be found [here](https://simulatedgreg.gitbooks.io/electron-vue/content/index.html).
