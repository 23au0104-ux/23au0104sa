def window3(ws):
    num = ws["numSlider"].getValue()
    rad = ws["radSlider"].getValue()
    sx = ws["scaleXSlider"].getValue()
    sy = ws["scaleYSlider"].getValue()
    
    r = 0.0
    ty = 0.0
    for i in range(num):
        crad = 1.0
        ir = 0.0
        name = pm.circle(r=crad)
        name[0].tx.set(rad)
        pm.rotate([0, r, 0], ws=True, p=[0, 0, 0])
        name[0].ty.set(ty)
        r += 30.0
        rad += sx
        ty += sy
        crad += ir
        
    pm.select(all=True)  
    pm.loft()

def makeWindow():
    with pm.window():
        with pm.autoLayout():
            ws = { }
            ws["numSlider"] = pm.intSliderGrp(label="個数", field=True, min=0, max=100, value=30)
            ws["radSlider"] = pm.floatSliderGrp(label="半径", field=True, min=0.0, max=10.0, value=5.0)
            ws["scaleXSlider"] = pm.floatSliderGrp(label="増減値X", field=True, min=-1.0, max=1.0, value=-0.1)
            ws["scaleYSlider"] = pm.floatSliderGrp(label="増減値Y", field=True, min=0.0, max=1.0, value=0.3)
            pm.button(label="ばね作成", command=pm.Callback(window3, ws))

makeWindow()