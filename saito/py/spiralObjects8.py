def spiralObjects8(rad, crad, num, ix, iy, ir):
    r = 0.0
    ty = 0.0
    for i in range(num):
        name = pm.circle(r=crad)
        name[0].tx.set(rad)
        pm.rotate([0, r, 0],ws=True, p=[0, 0, 0])
        name[0].ty.set(ty)
        r += 30.0
        rad += ix
        ty += iy
        crad += ir
        
    pm.select(all = True)  
    pm.loft()
        