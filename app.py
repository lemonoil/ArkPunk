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
enemy_table = {}
class arkGlobal:
    def __init__(self):
        self.package_name = 'com.hypergryph.arknights'
        self.device = None
        self.session = None
arkglobal = arkGlobal()
scr = """
var mp = {};
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

function mphook(){
    var str_name_so = "libil2cpp.so"; 
    var n_addr_func_offset = 0xCBED55;
    var n_addr_so = Module.findBaseAddress(str_name_so);
    var n_addr_func = parseInt(n_addr_so, 16) + n_addr_func_offset;
    var ptr_func = new NativePointer(n_addr_func);
    var message = {};
    var tar = '';
    Interceptor.attach(ptr_func, {
        onEnter: function (args) {
            tar = ptr(this.context.sp).sub(0x5c);
            tar = tar.toString();
            if(mp[tar] === undefined){
                mp[tar] = [];
            }
            var tmp = Memory.readPointer(args[3]);
            mp[tar].push(showMeTheId(tmp));
        },
        onLeave: function (retval) {
            
        }
    });
}
function mphook3(){
    var str_name_so = "libil2cpp.so"; 
    var n_addr_func_offset = 0x10CDEF5;
    var n_addr_so = Module.findBaseAddress(str_name_so);
    var n_addr_func = parseInt(n_addr_so, 16) + n_addr_func_offset;
    var ptr_func = new NativePointer(n_addr_func);
    var message = {};
    var tar = '';
    
    Interceptor.attach(ptr_func, {
        onEnter: function (args) {
            var flag = 1;
            var damageType = Memory.readPointer(ptr(args[1]).add(52))
            //console.log(damageType);
            message['type'] = damageType;
            var Rdata = getFp(ptr(args[1]).add(28))
            var realdelta = 0;
            if(getFp(ptr(args[1]).add(28))>4000000095)
                realdelta = 4294967295 - getFp(ptr(args[1]).add(28)) + 1;
            else realdelta = getFp(ptr(args[1]).add(28))
            //console.log(realdelta)
            message['val'] = realdelta;
            tar = ptr(args[1]);
            tar = tar.toString();
            var z = 0; z >>> 0;
            if(Memory.readU32(ptr(args[1]).add(8)) !== z) {
                var gt = Memory.readPointer(ptr(args[1]).add(8));
                gt = showMeTheId(gt);
                message['target'] = gt;
                if(Memory.readU32(ptr(args[1])) === z){
                    if(mp[tar] !== undefined){
                        //console.log(mp[tar][0]);
                        message['source'] = mp[tar][0];
                        mp[tar].shift();
                    }else{
                        flag = 0;
                    }
                }else{
                    var tt = Memory.readPointer(ptr(args[1]).add(0))
                    tt = showMeTheId(tt)
                    message['source'] = tt;
                    //console.log(tt)
                }
            }else{
                flag = 0;
            }

            if(flag !== 0){
                send(message);
            }
        },
        onLeave: function (retval) {
            
        }
    });
}
Interceptor.detachAll();
setImmediate(mphook);
setImmediate(mphook3);
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
        socketio.emit('confirm_connection',{'msg':message["source"]},namespace='/')
        if(message["source"] in char_table):
            charName = char_table[message["source"]]["name"]
            print(message)
            data = { '名称': '', 'val':0 , 'type': ''}
            data['名称'] = charName
            data['val'] = message['val']
            flag=0
            if(message['target'] in enemy_table):
                if(message['type'] == '0x0' or message['type'] == '0x4'):
                    flag = 1
                if(message['type'] == '0x1'):
                    data['type'] = '物理伤害'
                if(message['type'] == '0x2'):
                    data['type'] = '法术伤害'
                if(message['type'] == '0x3'):
                    data['type'] = '真实伤害'
            elif(message['target'] in char_table):
                if(message['type'] == '0x4'):
                    data['type'] = '治疗回复'
                elif(message['type'] != '0x0'):
                    data['type'] = '友方伤害'
                else:
                    flag=1
            else:
                flag=1
            if(flag == 0):
                socketio.emit('damageData',data,namespace='/')



if __name__ == '__main__':
    with open("character_table.json",'r',encoding='utf-8') as load_f:
        char_table = json.load(load_f)
    with open("enemy_handbook_table.json",'r',encoding='utf-8') as load_f:
        enemy_table = json.load(load_f)
    print("conent http://127.0.0.1:9081")
    socketio.run(app, host='127.0.0.1', port=9081, debug=True)
    sys.stdin.read()



