import pymel.core as pm

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
        with pm.formLayout() as form:
            with pm.tabLayout() as tab:
                ws = {}
                with pm.autoLayout() as tab1:
                    with pm.horizontalLayout():
                        ws['CheckBox1'] = pm.checkBox(label='ScaleX')
                        ws['CheckBox2'] = pm.checkBox(label='ScaleY')
                        ws['CheckBox3'] = pm.checkBox(label='ScaleZ')
                with pm.autoLayout() as tab2:
                    with pm.horizontalLayout():
                        ws['radioCollection1'] = pm.radioCollection()
                        ws['radioButton1'] = pm.radioButton(label='球体', select=True)
                        ws['radioButton2'] = pm.radioButton(label='立方体')
                        ws['radioButton3'] = pm.radioButton(label='コーン')
                with pm.autoLayout() as tab3:
                    ws["scaleXSlider"] = pm.floatSliderGrp(label="スケールX", field=True, min=0.0, max=10.0, value=1.0)
                    ws["scaleYSlider"] = pm.floatSliderGrp(label="スケールY", field=True, min=0.0, max=10.0, value=1.0)
                    ws["scaleZSlider"] = pm.floatSliderGrp(label="スケールZ", field=True, min=0.0, max=10.0, value=1.0)

            with pm.horizontalLayout() as tabs:
                pm.button(label='作成', command=pm.Callback(makeObject, ws))
                pm.button(label='閉じる', command=pm.Callback(pm.deleteUI, wn))


    pm.tabLayout(tab,edit=True, tabLabel=[[tab1,"方向"],[tab2,"プリミティブ"],[tab3,"スケール"]])
    form.attachForm(tab,"top",0)
    form.attachForm(tab,"right",5)
    form.attachForm(tab,"bottom",50)
    form.attachForm(tab,"left",5)

    form.attachControl(tabs,"top",5,tab)
    form.attachForm(tabs,"right",5)
    form.attachForm(tabs,"bottom",0)
    form.attachForm(tabs,"left",5)

makeWindow()