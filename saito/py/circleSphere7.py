import pymel.core as pm

def circleSphere7(rad, num, s):
    r = 0.0
    
    for i in range(3):
        for i in range(num):
            pm.sphere()
            pm.move([rad,0,0])
            pm.scale([s,s,s])
            pm.rotate([0,r,0],ws = True,p = [0,0,0])
            
            r += 360.0 / num
        s= s-1
        rad += s*2+1
            
circleSphere7(12.0, 8, 5.0)