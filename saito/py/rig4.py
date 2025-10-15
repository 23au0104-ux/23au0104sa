import pymel.core as pm
import re


class MyBoundingBox:
    
    def __init__(self,w,h,d):
        
        self.w = w
        self.h = h
        self.d = d
        
    def width(self):
        
        return self.w
        
    def height(self):
        
        return self.h
        
    def depth(self):
        
        return self.d

class MyJoint:
    def __init__(self, pj, p):
        self.pj = pj
        self.p = p
#-------
        self.pa = None

#------- 
    def setPreferredAngle(self,):
        self.pa = pa
        
    def make(self):
        pj = None
        if self.pj:
            pj = self.pj.getJoint()
        self.j = pm.joint(pj, p=self.p)
        
#-------
        if self.pj:
            pm.joint(pj,e=True,zso=True,oj='xyz',sao='yup')
        
    def getJoint(self):
        return self.j
        
    def getPosition(self):
        return self.p
        
    def scale(self, sx,sy,sz):
        self.p[0] *= sx
        self.p[1] *= sy
        self.p[2] *= sz

class MyJointList:
    def __init__(self, js):
        self.js = js
        
    def getBoundingBox(self):
        
        ps = [j.getPosition() for j in self.js]
        xs = [p[0] for p in ps]
        ys = [p[1] for p in ps]
        zs = [p[2] for p in ps]
        
        w = max(xs) - min(xs)
        h = max(ys) - min(ys)
        d = max(zs) - min(zs)
        
        return MyBoundingBox(w, h, d)  
        
    def make(self):
        for j in self.js:
            j.make()
            
    def scale(self, sx,sy,sz):
        
        for j in self.js:
            j.scale(sx,sy,sz)

#------
    def __getitem__(self,n):
        return self.js[n]

#------        
def setPreferredAngle(rigdata):
    js = rigdata['jlist']
    for n,pa in rigdata['pa']: #n→番号,pa→[X,Y,Z]
        js[n].setPreferredAngle(pa)

def readRigData(rigdata):
    with open(rigdata["fn"])as fp:
        rigdata['rd'] = fp.read()

def jsToList(d):
    return[int(d[0]),[float(d[1]), float(d[2]), float(d[3])]]
    
def paToList(d):
    return[int(d[0]),[float(d[1]),float(d[2]),float(d[3])]]

def toList(rigdata):
#------
    func = {'js':jsToList,'pa':paToList}
    for k in func.keys():
        rigdata[k] = []
    rd = rigdata['rd'].split('\n')
    rd = [re.sub('#.*$','',d)for d in rd]
    rd = [d.split()for d in rd]
    rd = [d for d in rd if d]
    for d in rd:
        rigdata[d[0]].append(func[d[0]](d[1:]))
    #rigdata['js'] = [[int(d[0]),[float(d[1]), float(d[2]), float(d[3])]] for d in rd]

def makeJointList(rigdata):
    js = [None]
    for n,p in rigdata['js']:
        js.append(MyJoint(js[n],p))
    rigdata['jlist'] = MyJointList(js[1:])
        
def makeJoint(rigdata):
    rigdata['jlist'].make()

def makeAll(rigdata):
    rigdata = rigdata
    readRigData(rigdata)
    toList(rigdata)
    makeJointList(rigdata)
    scaleJoint(rigdata)
    makeJoint(rigdata)
    #-------
    setPreferredAngle(rigdata)
def getRig(rigdata):
    rigdata["fn"] = pm.fileDialog2(ff='*.rig', ds=2, okc='OK', fm=1)[0]
    
def getJointData(js,pj,rigdata):
    rigdata['js'].append(js)
    rigdata['pj'].append(pj)
    rigdata['ps'].append(js.getTranslation(space='world'))
    for j in js.getChildren():
        getJointData(j,js,rigdata)


def jointData1():
    js = pm.selected()
    rigdata = {'js':[],'pj':[],'ps':[],'pn':[0]}
    getJointData(js[0],None,rigdata)
    i = 1
    for d in rigdata['pj'][1:]:
        rigdata['pn'].append(rigdata['js'].index(d) - i)
        i += 1
    s = []
    for n,p in zip(rigdata['pn'], rigdata['ps']):
        s.append(' '.join([str(n), str(p[0]),str(p[1]),str(p[2])]))
    s = '\n'.join(s)
    fn = pm.fileDialog2(ff='*.rig', ds=2, okc='OK', fm=0)[0]
    with open(fn,'w') as fp:
        fp.write(s)
        
def scaleJoint(rigdata):
    
    sel = pm.selected()
    b = sel[0].getBoundingBox()
    w1,h1,d1 = b.width(),b.height(),b.depth()
    b = rigdata["jlist"].getBoundingBox()
    w2,h2,d2 = b.width(),b.height(),b.depth()
    sx,sy,sz = w1/w2,h1/h2,d1/d2
    rigdata["jlist"].scale(sx,sy,sz)

def makeWindow():
    with pm.window():
        with pm.autoLayout():
            rigdata = {}
            pm.button(label='ジョイント選択', command=pm.Callback(getRig,rigdata))
            pm.button(label='ジョイント作成', command=pm.Callback(makeAll,rigdata))
            #pm.button(label='選択したジョイントを保存', command=pm.Callback(jointData1))

makeWindow()