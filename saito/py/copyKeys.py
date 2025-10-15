import math
import pymel.core as pm

def rtod(name, v):
    if name in ['rx','ry','rz']:
        v = math.degrees(v)
    return v
    
def copyKey(name,num):
    s = pm.selected() 
    attr = s[0].attr(name)
    attr2 = s[1].attr(name)
    cn = pm.findKeyframe(attr, c=True)
    c= pm.PyNode(cn[0])
    for i in range(c.numKeys()):
        pm.currentTime(c.getTime(i) + num)
        attr2.set(rtod(name, c.getValue(i)))
        pm.setKeyframe(attr2)

def CheckBox(ws):

    if ws['CheckBox1'].getValue():
        num = ws["TimeSlider"].getValue()
        copyKey('tx',num)
    if ws['CheckBox2'].getValue():
        num = ws["TimeSlider"].getValue()
        copyKey('ty',num)
    if ws['CheckBox3'].getValue():
        num = ws["TimeSlider"].getValue()
        copyKey('tz',num)
    if ws['CheckBox4'].getValue():
        num = ws["TimeSlider"].getValue()
        copyKey('rx',num)
    if ws['CheckBox5'].getValue():
        num = ws["TimeSlider"].getValue()
        copyKey('ry',num)
    if ws['CheckBox6'].getValue():
        num = ws["TimeSlider"].getValue()
        copyKey('rz',num)
    
def makeWindow():
    with pm.window():
        with pm.autoLayout():
            with pm.horizontalLayout():
                ws = {}
                ws['CheckBox1'] = pm.checkBox(label='tx')
                ws['CheckBox2'] = pm.checkBox(label='ty')
                ws['CheckBox3'] = pm.checkBox(label='tz')
            with pm.horizontalLayout():
                ws['CheckBox4'] = pm.checkBox(label='rx')
                ws['CheckBox5'] = pm.checkBox(label='ry')
                ws['CheckBox6'] = pm.checkBox(label='rz')

            ws["TimeSlider"] = pm.intSliderGrp(label="遅延フレーム数", field=True, min=0, max=100, value=0)
            
            pm.button(label='キーのコピー', command=pm.Callback(CheckBox, ws))
                
makeWindow()