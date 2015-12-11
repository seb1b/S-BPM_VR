#!/usr/bin/python
import os
from functools import partial
import subprocess
import time
import webbrowser
import importlib
import ConfigParser
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from PyoConnectLib import *
myo = Myo(sys.argv[1] if len(sys.argv) >= 2 else None)
cfg = ConfigParser.SafeConfigParser()
scriptlist = []
for filename in os.listdir('./scripts/'):
    if filename.endswith('.py') and filename != '__init__.py':
        scriptlist.append(filename)

modulelist = {}
modulenamelist = []
p = None
pi = None
pn = None
isMyoConnected = False

def FormatFileName(fname):
    tmp = fname.replace('_', ' ')
    if tmp.endswith('.py'):
        tmp = tmp[:-3]
    if tmp.endswith('.pyoc'):
        tmp = tmp[:-5]
    return tmp


def OpenConfig():
    global cfg
    cfg.read('pyoc.cfg')
    if cfg.has_section('Scripts') == False:
        cfg.add_section('Scripts')


def SaveConfig():
    with open('pyoc.cfg', 'wb') as cf:
        cfg.write(cf)


def ReadConfig(key):
    if cfg.has_option('Scripts', key):
        val = cfg.get('Scripts', key)
    else:
        val = False
    return val


def ReadConfigDef(key, default):
    val = ReadConfig(key)
    if val == False:
        val = default
    return val


def SetConfig(key, value):
    cfg.set('Scripts', key, value)


def ConnectMyo():
    global isMyoConnected
    if isMyoConnected:
        myo.disconnect()
        time.sleep(1)
    myo.connect()
    isMyoConnected = True


def DisconnectMyo():
    global isMyoConnected
    if isMyoConnected:
        myo.disconnect()
        isMyoConnected = False
        print 'Myo disconnected'
    else:
        print 'Myo not connected'


def LoadScriptModule(sname):
    try:
        mod = importlib.import_module('scripts.' + sname)
    except:
        return False

    mod.myo = myo
    mod.sname = sname
    if hasattr(mod, 'scriptId') == False:
        print 'Module ' + sname + ' has no ID'
        mod.scriptId = ''
    if hasattr(mod, 'scriptTitle') == False:
        print 'Module ' + sname + ' has no title'
        mod.scriptTitle = FormatFileName(sname)
    if hasattr(mod, 'scriptDetailsUrl') == False:
        print 'Module ' + sname + ' has no URL'
        mod.scriptDetailsUrl = ''
    if hasattr(mod, 'scriptDescription') == False:
        print 'Module ' + sname + ' has no description'
        mod.scriptDescription = ''
    try:
        f_onPoseEdge = mod.onPoseEdge
    except:
        f_onPoseEdge = False

    if f_onPoseEdge:
        myo.Add_onPoseEdge(f_onPoseEdge)
    try:
        f_onLock = mod.onLock
    except:
        f_onLock = False

    if f_onLock:
        myo.Add_onLock(f_onLock)
    try:
        f_onUnlock = mod.onUnlock
    except:
        f_onUnlock = False

    if f_onUnlock:
        myo.Add_onUnlock(f_onUnlock)
    try:
        f_onPeriodic = mod.onPeriodic
    except:
        f_onPeriodic = False

    if f_onPeriodic:
        myo.Add_onPeriodic(f_onPeriodic)
    try:
        f_onWear = mod.onWear
    except:
        f_onWear = False

    if f_onWear:
        myo.Add_onWear(f_onWear)
    try:
        f_onUnwear = mod.onUnwear
    except:
        f_onUnwear = False

    if f_onUnwear:
        myo.Add_onUnwear(f_onUnwear)
    try:
        f_onBoxChange = mod.onBoxChange
    except:
        f_onBoxChange = False

    if f_onBoxChange:
        myo.Add_onBoxChange(f_onBoxChange)
    try:
        f_onEMG = mod.onEMG
    except:
        f_onEMG = False

    if f_onEMG:
        myo.add_emg_handler(f_onEMG)
    return mod


def LoadAllScripts():
    global modulelist
    global scriptlist
    global modulenamelist
    modulelist = {}
    modulenamelist = []
    myo.clear_handle_lists()
    for sfile in scriptlist:
        ei = scriptlist.index(sfile)
        mname = sfile[:-3]
        if ReadConfigDef(mname, 'on') == 'on':
            emod = LoadScriptModule(mname)
            if emod:
                modulelist[ei] = emod
                modulenamelist.append(mname)


def SetOnOffScript(arg):
    global btns
    if arg >= len(scriptlist):
        return False
    sf = scriptlist[arg]
    mname = sf[:-3]
    if mname in modulenamelist:
        SetConfig(mname, 'off')
    else:
        SetConfig(mname, 'on')
    LoadAllScripts()
    if mname in modulenamelist:
        btns[arg].config(text='ON', background='#50BBE7', relief=tk.SUNKEN)
    else:
        btns[arg].config(text='off', background='gray95', relief=tk.RAISED)


def QuitCurrentScript():
    global p
    global pi
    if p != None:
        if p.poll() == None:
            p.terminate()
            time.sleep(0.5)
        if p.poll() == None:
            p.kill()
            time.sleep(0.5)
        if p.poll() == None:
            return False
    if pi != None:
        btns[pi].configure(background='gray95', relief=tk.RAISED)
        pi = None
        pn = None
    return True


def CallScript(i):
    global p
    if p != None:
        if p.poll() == None:
            return False
    if i >= len(scriptlist):
        return False
    sf = scriptlist[i]
    p = subprocess.Popen(['python', sf])
    print 'pid: ' + str(p.pid)
    return True


def ActivateScript(arg):
    global pi
    global pn
    if arg < len(scriptlist):
        prev_pi = pi
        if QuitCurrentScript() == False:
            print 'Error: could not terminate previous script'
            return False
        if prev_pi != arg:
            if CallScript(arg) == False:
                print 'Error: could not call script'
                return False
            else:
                pi = arg
                pn = scriptlist[arg]
                btns[pi].configure(background='#50BBE7', relief=tk.SUNKEN)
                return True
    else:
        print 'Error: script index out of scriptlist'
        return False


def Close():
    global root
    global pleaseQuit
    QuitCurrentScript()
    root.quit()
    pleaseQuit = True
    SaveConfig()


def AboutBox():
    webbrowser.open('http://www.fernandocosentino.net/pyoconnect')


OpenConfig()
LoadAllScripts()
root = tk.Tk()
root.title('PyoConnect v2.0')
main = tk.Frame(root, width=300, height=300, background='gray95')
main.pack(fill=tk.BOTH, expand=1)
topframe = tk.Frame(main, width=300, height=50, padx=10, pady=10, background='gray20')
topframe.pack_propagate(0)
topframe.pack(fill=tk.BOTH)
toplabel = tk.Label(topframe, text='PyoConnect', background='gray20', foreground='#50BBE7', font='Arial 20')
toplabel.pack(fill=tk.BOTH)
connframe = tk.Frame(main, width=300, height=50, padx=10, pady=10, background='gray95')
connframe.pack(fill=tk.X)
connbtn = tk.Button(connframe, text='Connect Myo', background='#50BBE7', foreground='white', border=0, command=ConnectMyo, relief=tk.RAISED)
connbtn.pack(side=tk.LEFT)
connbtn = tk.Button(connframe, text='Disconnect', background='#50BBE7', foreground='white', border=0, command=DisconnectMyo, relief=tk.RAISED)
connbtn.pack(side=tk.RIGHT)
btnframe = tk.Frame(main, width=280, padx=10, pady=10, background='gray95')
btnframe.pack(fill=tk.X)
i = 0
btns = []
for sfile in scriptlist:
    si = scriptlist.index(sfile)
    mname = sfile[:-3]
    eframe = tk.Frame(btnframe, width=280, height='36', background='gray95', borderwidth='1', relief=tk.RIDGE)
    eframe.pack_propagate(0)
    eframe.pack(fill=tk.BOTH)
    try:
        etitle = modulelist[si].scriptTitle
    except:
        etitle = FormatFileName(sfile)

    elabel = tk.Label(eframe, text=etitle, background='gray95')
    elabel.pack(side=tk.LEFT)
    ebtn = tk.Button(eframe, border=0)
    btns.append(ebtn)
    if mname in modulenamelist:
        btns[i].config(text='ON', background='#50BBE7', relief=tk.SUNKEN, command=partial(SetOnOffScript, i))
    else:
        btns[i].config(text='off', background='gray95', relief=tk.RAISED, command=partial(SetOnOffScript, i))
    btns[i].scriptname = sfile
    btns[i].modname = mname
    btns[i].script_id = i
    btns[i].frame = eframe
    btns[i].label = elabel
    btns[i].pack(side=tk.RIGHT)
    i += 1

tk.Label(btnframe, text=' ', background='gray95').pack()
tk.Button(btnframe, text='About', background='#50BBE7', border=0, command=AboutBox).pack(side=tk.LEFT)
tk.Button(btnframe, text='Quit', background='#50BBE7', border=0, command=Close).pack(side=tk.RIGHT)
pleaseQuit = False
t0 = time.time()
cnt = 0
while pleaseQuit == False:
    root.update()
    if isMyoConnected:
        t0 = time.time()
        p = myo.run(1.0)
        if time.time() - t0 > 0.3:
            DisconnectMyo()
        else:
            myo.tick()

try:
    root.destroy()
except:
    pass
