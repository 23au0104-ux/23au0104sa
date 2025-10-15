from random import uniform
import pymel.core as pm

def makeRock2(num, xRange, yRange, zRange):
    for i in range(num):
        pm.polySphere()
        lname = pm.lattice(objectCentered=True)
        s = [uniform(1.0, 3.0) for _ in range(3)]
        pm.scale(s)
        t = [uniform(-r, r) for r in [xRange, yRange, zRange]]
        pm.move(t)
        for obj in lname[1].pt:
            pm.select(obj)
            t = [uniform(-0.6, 0.6) for _ in range(3)]
            pm.move(t, r=True)

def rand3(xRange, yRange, zRange):
    return [uniform(-r, r) for r in [xRange, yRange, zRange]]

def makeParticle(num, xRange, yRange, zRange):  
    positions = [rand3(xRange, yRange, zRange) for _ in range(num)]
    pm.particle(p=positions)

def lastname(name):
    return name.split('|')[-1]

def makeRockCallback(ws):
    makeRock2(int(ws['nu'].getValue()), ws['xs'].getValue(), ws['ys'].getValue(), ws['zs'].getValue())

def makeParticleCallback(ws):
    makeParticle(int(ws['nu'].getValue()), ws['xs'].getValue(), ws['ys'].getValue(), ws['zs'].getValue())

def makeObjects6(ws):
    name = ws['radioC'].getSelect()
    if name == lastname(ws['radioB1']):
        makeRockCallback(ws)
    elif name == lastname(ws['radioB3']):
        makeParticleCallback(ws)

def makeWindow():
    with pm.window() as wn:
        with pm.autoLayout():
            ws = {}
            with pm.horizontalLayout():
                ws['radioC'] = pm.radioCollection()
                ws['radioB1'] = pm.radioButton(label='岩石', select=True)
                ws['radioB3'] = pm.radioButton(label='パーティクル')
            ws['nu'] = pm.intSliderGrp(label='個数', field=True, min=1, max=100, value=30) 
            ws['xs'] = pm.floatSliderGrp(label='範囲X', field=True, min=0.0, max=20.0, value=5.0)
            ws['ys'] = pm.floatSliderGrp(label='範囲Y', field=True, min=0.0, max=20.0, value=5.0)
            ws['zs'] = pm.floatSliderGrp(label='範囲Z', field=True, min=0.0, max=20.0, value=5.0)
            with pm.horizontalLayout():
                pm.button(label='作成', command=lambda unused: makeObjects6(ws))
                pm.button(label='閉じる', command=lambda unused: pm.deleteUI(wn))

makeWindow()
