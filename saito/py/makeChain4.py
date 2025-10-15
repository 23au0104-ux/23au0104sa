import pymel.core as pm

def makeShader1(name, col):
    lambert = pm.createSurfaceShader('lambert')
    fra = pm.shadingNode('fractal', asTexture=True)
    p2d = pm.shadingNode('place2dTexture', asUtility=True)
    
    pm.sets(lambert[1], fe = name[0])
    fra.colorGainR.set(col[0])
    fra.colorGainG.set(col[1])
    fra.colorGainB.set(col[2])
    
    
    p2d.outUV >> fra.uvCoord
    p2d.outUvFilterSize >> fra.uvFilterSize
    fra.outColor >> lambert[0].color
    p2d.repeatU.set(4)
    p2d.repeatV.set(4)

def makeChain1(ws):
    num = ws["numSlider"].getValue()
    rad = ws["radSlider"].getValue()
    sx = ws["scaleXSlider"].getValue()
    sy = ws["scaleYSlider"].getValue()
    sz = ws["scaleZSlider"].getValue()
    col = ws["colorSlider"].getRgbValue()
    tx = 0.0
    ry = 90.0
    gname = pm.gravity()
    for i in range(num):
        tname = pm.torus(hr=rad)
        pm.rotate([0, ry, 90])
        pm.scale([sx, sy, sz])
        pm.move([tx, 0, 0])
        if i == 0:
            pm.constrain(tname[0], nail=True)
        else:
            pm.constrain(pname, tname[0], pin=True)
        pm.connectDynamic(tname[0], f=gname)
        tx += 4.0
        ry = 90.0 * (i % 2)
        pname = tname[0]
        makeShader1(tname, col)

def makeWindow():
    with pm.window(title="make Chain") as wn:
        with pm.columnLayout(adjustableColumn=True):
            ws = {}
            ws["numSlider"] = pm.intSliderGrp(label="個数", field=True, min=1, max=30, value=10)
            ws["radSlider"] = pm.floatSliderGrp(label="半径", field=True, min=0.0, max=1.0, value=0.1)
            ws["scaleXSlider"] = pm.floatSliderGrp(label="スケールX", field=True, min=0.0, max=10.0, value=2.0)
            ws["scaleYSlider"] = pm.floatSliderGrp(label="スケールY", field=True, min=0.0, max=10.0, value=3.0)
            ws["scaleZSlider"] = pm.floatSliderGrp(label="スケールZ", field=True, min=0.0, max=10.0, value=2.0)
            ws["colorSlider"] = pm.colorSliderGrp(label="カラー", rgb=[1.0, 0.0, 0.0])
        with pm.horizontalLayout():
            pm.button(label="作成", command=pm.Callback(makeChain1, ws))
            pm.button(label='閉じる', command=pm.Callback(pm.deleteUI, wn))

makeWindow()