import pymel.core as pm

def lastname(name):
    return name.split('|')[-1]
def makeObject(ws):
    sx = 1
    sy = 1
    sz = 1
    
    if ws['CheckBox1'].getValue():
        sx = ws["scaleXSlider"].getValue()
    if ws['CheckBox2'].getValue():
        sy = ws["scaleYSlider"].getValue()
    if ws['CheckBox3'].getValue():
        sz = ws["scaleZSlider"].getValue()
    
    func = {}
    func[lastname(ws['radioButton1'])] = pm.polySphere
    func[lastname(ws['radioButton2'])]= pm.polyCube
    func[lastname(ws['radioButton3'])]= pm.polyCone
        
    name = ws['radioCollection1'].getSelect()
    func[name]()

    pm.scale([sx, sy, sz])
    
def makeWindow():
    with pm.window() as wn:
        with pm.autoLayout():
            with pm.horizontalLayout():
                ws = {}
                ws['CheckBox1'] = pm.checkBox(label='スケールX')
                ws['CheckBox2'] = pm.checkBox(label='スケールY')
                ws['CheckBox3'] = pm.checkBox(label='スケールZ')
            
            with pm.horizontalLayout():
                ws['radioCollection1'] = pm.radioCollection()
                ws['radioButton1'] = pm.radioButton(label='球体', select=True)
                ws['radioButton2'] = pm.radioButton(label='立方体')
                ws['radioButton3'] = pm.radioButton(label='コーン')

            ws["scaleXSlider"] = pm.floatSliderGrp(label="スケールX", field=True, min=0.0, max=10.0, value=1.0)
            ws["scaleYSlider"] = pm.floatSliderGrp(label="スケールY", field=True, min=0.0, max=10.0, value=1.0)
            ws["scaleZSlider"] = pm.floatSliderGrp(label="スケールZ", field=True, min=0.0, max=10.0, value=1.0)
            
            with pm.horizontalLayout():
                pm.button(label='作成', command=pm.Callback(makeObject, ws))
                pm.button(label='閉じる', command=pm.Callback(pm.deleteUI, wn))

makeWindow()


