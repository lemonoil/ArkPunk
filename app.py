#encoding:utf-8
import frida,json
import sys,time
from flask import Flask
from flask_socketio import SocketIO, emit
import flask_login
from threading import Lock
import random

async_mode = None
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)

char_table = {}

class arkGlobal:
    def __init__(self):
        self.package_name = 'com.hypergryph.arknights'
        self.device = None
        self.session = None
arkglobal = arkGlobal()
scr = """
function getFp(idx){
    var Decimals = (Memory.readU32(idx))/2/2147483647;
    var Integer = Memory.readU32(ptr(idx).add(4));
    return Integer + Decimals;
}
function showMeTheId(preIdPtr){
    var offs = ptr(preIdPtr).add(120)
    var idx = Memory.readPointer(offs)
    var names = ''
    for(var i=12;;i+=2){
        var tmp = Memory.readUtf8String(ptr(idx).add(i));
        if(tmp === '') break;
        names = names + tmp;
    }
    return names
}


function damageHook(){
    var str_name_so = "libil2cpp.so"; 
    var n_addr_func_offset = 0x9009AD;
    var n_addr_so = Module.findBaseAddress(str_name_so);
    var n_addr_func = parseInt(n_addr_so, 16) + n_addr_func_offset;
    var ptr_func = new NativePointer(n_addr_func);
    var message = {};
    Interceptor.attach(ptr_func, {
        onEnter: function (args) { 
            message['source'] = showMeTheId(args[2]);
            message['sHp'] = getFp(ptr(args[2]).add(28));
            message['target'] =  showMeTheId(args[3]);
            message['tHp'] = getFp(ptr(args[3]).add(28));
            message['type'] = args[4];

        },
        onLeave: function (retval) {
            message["damage"] = getFp(retval);
            send(message);
        }
    });
}

Interceptor.detachAll();
setImmediate(damageHook);
"""

@socketio.on('connect', namespace='/')
def connect_msg():
    if( arkglobal.device == None):
        arkglobal.device = frida.get_usb_device()
        pid = arkglobal.device.spawn(arkglobal.package_name)
        arkglobal.session = arkglobal.device.attach(pid)
        arkglobal.device.resume(pid)
        time.sleep(15)
        script = arkglobal.session.create_script(scr)
        script.on("message" , on_message)
        script.load()
        socketio.emit('confirm_connection',{'msg':'connected success,script loaded'},namespace='/')
    else:
        socketio.emit('confirm_connection',{'msg':'connection OK'},namespace='/')

def on_message(message ,data):
    if(message['type'] == "send"):
        message = message['payload']
        if(message["source"] in char_table):
            charName = char_table[message["source"]]["name"]
            print(message)
            data = { '名称': '', 'val':0 , 'type': ''}
            data['名称'] = charName
            if(message['tHp'] < message['damage']):
                data['val'] = message['tHp']
            else:
                data['val'] = message['damage']
            if(message['type'] == '0x1'):
                data['type'] = '物理伤害'
            if(message['type'] == '0x2'):
                data['type'] = '法术伤害'
            if(message['type'] == '0x3'):
                data['type'] = '真实伤害'
            if(message['type'] == '0x4'):
                data['type'] = '治疗回复'
            socketio.emit('chartData',data,namespace='/')

if __name__ == '__main__':
    with open("character_table.json",'r',encoding='utf-8') as load_f:
        char_table = json.load(load_f)
    print("conent http://127.0.0.1:9081")
    socketio.run(app, host='127.0.0.1', port=9081, debug=True)
    sys.stdin.read()



