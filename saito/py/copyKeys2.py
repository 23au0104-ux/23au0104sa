import re
import math
import pymel.core as pm

def rtod(name, v):
    if name in ['rotateX','rotateY','rotateZ']:
        v = math.degrees(v)
    return v
    
def getAttrName():
    attrs = pm.mel.eval('findAnimCurves graphEditor1FromOutliner')
    attrs2 = []
    for a in attrs:
        attrs2. append(re.sub('.*_','',a))
    return attrs2

def copyKeyframe(c, num ,name ,attr2 ,nscale,kscale):
    for i in range(c.numKeys()):
        pm.currentTime(int(c.getTime(i)*kscale) + num)
        attr2.set(rtod(name,c.getValue(i)*nscale))
        pm.setKeyframe(attr2)

def copyTangent(cn,cn2):
    intangent = pm.keyTangent(cn,q=True, ia=True)
    for i,t in enumerate(intangent):
        pm.keyTangent(cn2, e=True, index=[i,], ia=t)
    outtangent = pm.keyTangent(cn,q=True, oa=True)
    for i,t in enumerate(outtangent):
        pm.keyTangent(cn2, e=True, index=[i,], oa=t)

def copyKey(name,num,nscale,kscale):
    s = pm.selected() 
    attr = s[0].attr(name)
    attr2 = s[1].attr(name)
    cn = pm.findKeyframe(attr, c=True)
    c= pm.PyNode(cn[0])
    copyKeyframe(c,num,name,attr2,nscale,kscale)
    cn2 = pm.findKeyframe(attr2, c=True)
    copyTangent(cn, cn2)
    
def copyKey2(ws):
    num = ws["numSlider"].getValue()
    nscale = ws["scaleSlider"].getValue()
    kscale = ws["keySlider"].getValue()
    attrs = getAttrName()
    for a in attrs:
        copyKey(a, num,nscale,kscale)



def makeWindow():
    with pm.window():
        ws = {}
        with pm.autoLayout():
            
            ws["scaleSlider"] = pm.floatSliderGrp(label="値スケール", field=True, min=0.0, max=10.0, value=1.0)
            ws["keySlider"] = pm.floatSliderGrp(label="キースケール", field=True, min=0.0, max=10.0, value=1.0)
            ws["numSlider"] = pm.floatSliderGrp(label="遅延フレーム数", field=True, min=0, max=100, value=0)
            
            pm.button(label='キーのコピー', command=pm.Callback(copyKey2, ws))
            
makeWindow()