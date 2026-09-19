import ezdxf
import openpyxl
import math




# Input Parameters
CLEAR_WIDTH = 1300.0        # mm
SKIN_PLATE_HEIGHT = 1500.0   # mm
WALL_HEIGHT = 2100.0        # mm
FRAME_ABOVE_WALL = 900.0    # mm
GEAR_BOX_DIM = (250,250,300)
SPINDLE_DIAMETER = 50
SPINDLE_COVER_HEIGHT = 1000
SPINDLE_COVER_DIAMETER = 100
CONCRETE_THICKNESS = 500

CB100 = 100
CH100 = 50
BP250 = 250
THK = 10

# Derived Parameters
FRAME_HEIGHT = WALL_HEIGHT + FRAME_ABOVE_WALL
SPINDLE_HEIGHT = FRAME_HEIGHT - SKIN_PLATE_HEIGHT + GEAR_BOX_DIM[-1] + THK*2 - 70


# Create Document
doc = ezdxf.new("R2018", setup=True)  
doc.units = ezdxf.units.MM
doc.header["$MEASUREMENT"] = 1
doc.header["$LUNITS"] = 2
doc.header["$INSUNITS"] = 4
doc.header['$LTSCALE'] = 40
def create_dimst(name, dimscale, dimtxt, dimasz):
    if name not in doc.dimstyles:
        doc.dimstyles.new(name)

    dimstyle = doc.dimstyles.get(name)
    dimstyle.dxf.dimscale = dimscale
    dimstyle.dxf.dimtxt = dimtxt
    dimstyle.dxf.dimasz = dimasz
    dimstyle.dxf.dimlfac = 1
    return name

dimname = create_dimst("EZDXF", 1, 20, 20)
doc.header["$DIMSTYLE"] = "dimname"

msp = doc.modelspace()

# LAYERS to use
def setup_layers(doc):
    doc.layers.add("F_OUTLINE", color=2)
    doc.layers.add("F_HIDDEN",  color=11, linetype="DASHED")
    doc.layers.add("L_OUTLINE", color=5)
    doc.layers.add("L_HIDDEN",  color=25, linetype="DASHED")
    doc.layers.add("H_OUTLINE", color=6)
    doc.layers.add("H_HIDDEN", color=6, linetype="DASHED")
    doc.layers.add("C_OUTLINE", color=1)
    doc.layers.add("CENTER",  color=1, linetype="CENTER")
    doc.layers.add("DIM",     color=3)
    doc.layers.add("TEXT",    color=2)
    doc.layers.add("HATCH",   color=9)
    doc.layers.add("ASSY",    color=6)

setup_layers(doc)


pinblk = doc.blocks.new(name="PIN")
pinblk.add_lwpolyline(((10,0), (0,0), (0,50), (10,50)), close=True, dxfattribs={"layer": "0"})
pinblk.add_lwpolyline(((10,7.5), (166,7.5), (166,42.5), (10,42.5)), close=False, dxfattribs={"layer": "0"})
pinblk.add_circle((140,25), 5, dxfattribs={"layer": "0"})



Frame_X = doc.blocks.new(name="FrameXSec")
Leaf_X = doc.blocks.new(name="LeafXSec")
Hoist_X = doc.blocks.new(name="HoistXSec")
Conc_X = doc.blocks.new(name="ConcXSec")


def draw_handle(blk):
    co = 50
    ci = 34
    hd = 400
    pd = 20
    blk.add_lwpolyline(((0, co/2), (0, -co/2), (50, -co/2), (50, co/2)), close=True, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((0, ci/2), (50, ci/2), dxfattribs={"layer": "H_HIDDEN"})
    blk.add_line((0, -ci/2), (50, -ci/2), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(
        ((0, -ci/2), (0, -ci/2+8), (30, -ci/2+8), (30, -ci/2)),
        close=False, dxfattribs={"layer": "H_OUTLINE"}
    )
    
    blk.add_lwpolyline(((25, co/2), (25, co/2+50), (25+75, co/2+105), (25+75, co/2+155)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((25, -co/2), (25, -co/2-50), (25+75, -co/2-105), (25+75, -co/2-155)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    
    blk.add_lwpolyline(((25-10, co/2), (25-10, co/2+50+5), (25+75-10, co/2+105+5), (25+75-10, co/2+155)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((25-10, -co/2), (25-10, -co/2-50-5), (25+75-10, -co/2-105-5), (25+75-10, -co/2-155)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    
    blk.add_circle((95, hd/2-pd/2), pd/2, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_circle((95, -hd/2+pd/2), pd/2, dxfattribs={"layer": "H_OUTLINE"})
    

    blk.add_line((105, hd/2-pd/2), (105, -hd/2+pd/2), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((105-pd, hd/2-pd/2), (105-pd, -hd/2+pd/2), dxfattribs={"layer": "H_OUTLINE"})

    blk.add_lwpolyline(
        ((95, -hd/2+pd), (290 ,-hd/2+pd), (290 ,-hd/2+pd+15), (295, -hd/2+pd+15), (295, -hd/2-15), (290, -hd/2-15), (290, -hd/2), (95, -hd/2)),
        close=False, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(
        ((107, -173), (107+180, -173), (107+180, -173-34), (107, -173-34)),
        close=True, dxfattribs={"layer": "H_OUTLINE"}
    )
    blk.add_line((107, -173-3), (107+180, -173-3), dxfattribs={"layer": "H_HIDDEN"})
    blk.add_line((107, -173-34+3), (107+180, -173-34+3), dxfattribs={"layer": "H_HIDDEN"})

def draw_gearbox(blk):
    GBL = GEAR_BOX_DIM[0]
    GBH = GEAR_BOX_DIM[-1]
    hy = 240
    hx = 125

    blk.add_lwpolyline(((-GBL/2-50, 0), (-GBL/2-50, THK), (GBL/2+50, THK), (GBL/2+50, 0)), close=True, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((GBL/2,THK), (GBL/2,THK+GBH), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((-GBL/2,THK), (-GBL/2,THK+GBH), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((-GBL/2, THK+GBH), (-GBL/2, THK*2+GBH), (GBL/2, THK*2+GBH), (GBL/2, THK+GBH)), close=True, dxfattribs={"layer": "H_OUTLINE"}) 

    blk.add_line((hx, hy+40), (hx+30, hy+40), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((hx, hy+35), (hx+30, hy+35), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((hx, hy+15), (hx+50, hy+15), dxfattribs={"layer": "H_HIDDEN"})
    blk.add_line((hx, hy-15), (hx+50, hy-15), dxfattribs={"layer": "H_HIDDEN"})
    blk.add_line((hx, hy-40), (hx+30, hy-40), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((hx, hy-35), (hx+30, hy-35), dxfattribs={"layer": "H_OUTLINE"})

    

    blk.add_lwpolyline(((hx+30, hy+65), (hx+50, hy+65), (hx+50, hy-65), (hx+30, hy-65)), close=True, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((hx+40, hy-65), (hx+40, hy+65), dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((hx+50, hy+15), (hx+100, hy+15), (hx+100, hy-15), (hx+15, hy-15)), close=False, dxfattribs={"layer": "H_OUTLINE"})


handle = doc.blocks.new(name="HANDLE")
draw_handle(handle)
g_box = doc.blocks.new(name="GEARBOX")
draw_gearbox(g_box)

def draw_frame_xsection(blk):
    W, H = CLEAR_WIDTH, FRAME_HEIGHT
    TW = W + THK*2 + CB100*2

    # Vertical Parts
    blk.add_line((0, 0), (0, H-300), dxfattribs={"layer": "F_OUTLINE"})
    blk.add_line((0, H-300), (10, H-300), dxfattribs={"layer": "F_OUTLINE"})

    blk.add_line((TW, 0), (TW, H-300), dxfattribs={"layer": "F_OUTLINE"})
    blk.add_line((TW, H-300), (TW-10, H-300), dxfattribs={"layer": "F_OUTLINE"})

    blk.add_line((THK, 0), (THK, H), dxfattribs={"layer": "F_OUTLINE"})
    blk.add_line((THK+THK, 0), (THK+THK, H-CB100), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((CB100, 0), (CB100, H-CB100), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((THK+CB100, 0), (THK+CB100, H), dxfattribs={"layer": "F_OUTLINE"})

    blk.add_line((TW-THK, 0), (TW-THK, H), dxfattribs={"layer": "F_OUTLINE"})
    blk.add_line((TW-THK-THK, 0), (TW-THK-THK, H-CB100), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((TW-CB100, 0), (TW-CB100, H-CB100), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((TW-THK-CB100, 0), (TW-THK-CB100, H), dxfattribs={"layer": "F_OUTLINE"})

    # Horizontal Parts
    blk.add_line((THK, H), (TW-THK, H), dxfattribs={"layer": "F_OUTLINE"})
    blk.add_line((THK, H-THK), (TW-THK, H-THK), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((THK, H-CB100+THK), (TW-THK, H-CB100+THK), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((THK, H-CB100), (TW-THK, H-CB100), dxfattribs={"layer": "F_OUTLINE"})

    blk.add_line((0, 0), (TW, 0), dxfattribs={"layer": "F_OUTLINE"})
    blk.add_line((0, -THK), (TW, -THK), dxfattribs={"layer": "F_OUTLINE"})
    blk.add_line((0, -THK-THK), (TW, -THK-THK), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((0, -CH100), (TW, -CH100), dxfattribs={"layer": "F_OUTLINE"})

    blk.add_line((0, 0), (0, -CH100), dxfattribs={"layer": "F_HIDDEN"})
    blk.add_line((TW, 0), (TW, -CH100), dxfattribs={"layer": "F_OUTLINE"})


def draw_leaf_xsection(blk):
    SR = SPINDLE_DIAMETER/2
    W = CLEAR_WIDTH + 75*2
    H = SKIN_PLATE_HEIGHT
    NVS = round(W/350)-1
    NHS = round((H-50)/350)+1
    HC = W/(NVS+1)
    VC = (H-50)/(NHS-1)
    blk.add_lwpolyline(((0, 0), (W, 0), (W, H), (0, H)), close=True, dxfattribs={"layer": "L_OUTLINE"})
    blk.add_lwpolyline(((W/2-SR-THK, H), (W/2-SR-THK, H+110), (W/2-SR-THK-THK, H+110), (W/2-SR-THK-THK, H)), close=False, dxfattribs={"layer": "L_OUTLINE"})
    blk.add_lwpolyline(((W/2+SR+THK, H), (W/2+SR+THK, H+110), (W/2+SR+THK+THK, H+110), (W/2+SR+THK+THK, H)), close=False, dxfattribs={"layer": "L_OUTLINE"})
    blk.add_blockref("PIN", (W/2-SR-THK*3, H+46))
    blk.add_line((W/2, -300), (W/2, H+300), dxfattribs={"layer": "Center"})
    for i in range(NHS):
        blk.add_line((0, i*VC+CH100), (W/2, i*VC+CH100), dxfattribs={"layer": "L_OUTLINE"})
        blk.add_line((0, i*VC+CH100-THK), (W/2, i*VC+CH100-THK), dxfattribs={"layer": "L_HIDDEN"})
        blk.add_line((0, i*VC), (W/2, i*VC), dxfattribs={"layer": "L_OUTLINE"})
        for j in range(1, NVS):
            if i >= (NHS-1):
                continue
            if j*HC+10 >= W/2:
                continue
            blk.add_line((j*HC, i*VC+CH100), (j*HC, (i+1)*VC), dxfattribs={"layer": "L_OUTLINE"})
            blk.add_line((j*HC+10, i*VC+CH100), (j*HC+10, (i+1)*VC), dxfattribs={"layer": "L_OUTLINE"})
            blk.add_line((j*HC, (i+1)*VC), (j*HC, (i+1)*VC+CH100-10), dxfattribs={"layer": "L_HIDDEN"})
            blk.add_line((j*HC+10, (i+1)*VC), (j*HC+10, (i+1)*VC+CH100-10), dxfattribs={"layer": "L_HIDDEN"})

def draw_hoisting_xsection(blk):
    GBL = GEAR_BOX_DIM[0]
    GBH = GEAR_BOX_DIM[-1]
    SH = SPINDLE_HEIGHT
    SR = SPINDLE_DIAMETER/2
    SCH = SPINDLE_COVER_HEIGHT
    SCR = SPINDLE_COVER_DIAMETER/2

    blk.add_blockref("HANDLE", (195, 240))
    blk.add_blockref("GEARBOX", (0, 0))

    blk.add_lwpolyline(((-SCR-40, GBH+THK*2), (-SCR-40, GBH+THK*3), (SCR+40, GBH+THK*3), (SCR+40, GBH+THK*2)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((-SCR, GBH+THK*3), (-SCR, GBH+THK*3+SCH), (SCR, GBH+THK*3+SCH), (SCR, GBH+THK*3)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((-SCR+10, GBH+THK*3), (-SCR+10 ,GBH+THK*3+SCH), dxfattribs={"layer": "H_HIDDEN"})
    blk.add_line((SCR-10, GBH+THK*3), (SCR-10 ,GBH+THK*3+SCH), dxfattribs={"layer": "H_HIDDEN"})

    blk.add_lwpolyline(((-SR, GBH+THK*3+50-SH), (-SR, GBH+THK*3+50-10), (-SR+5, GBH+THK*3+50), (SR-5, GBH+THK*3+50), (SR, GBH+THK*3+50-10), (SR, GBH+THK*3+50-SH)), close=True, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_line((-SR+5, GBH+THK*3+50-SH+300), (-SR+5, GBH+THK*3+50), dxfattribs={"layer": "H_HIDDEN"})
    blk.add_line((SR-5, GBH+THK*3+50-SH+300), (SR-5, GBH+THK*3+50), dxfattribs={"layer": "H_HIDDEN"})
    blk.add_lwpolyline(((SR, GBH+THK*3+50-SH+100), (SR, GBH+THK*3+50-SH-100), (SR+10, GBH+THK*3+50-SH-100), (SR+10, GBH+THK*3+50-SH+100)), close=True, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((-SR, GBH+THK*3+50-SH+100), (-SR, GBH+THK*3+50-SH-100), (-SR-10, GBH+THK*3+50-SH-100), (-SR-10, GBH+THK*3+50-SH+100)), close=True, dxfattribs={"layer": "H_OUTLINE"})

def draw_concrete_xsection(blk):
    H = WALL_HEIGHT
    CW = CLEAR_WIDTH
    CT = CONCRETE_THICKNESS

    c_poly = ((-CW/2-CB100-THK, H), (-CW/2-CT, H), (-CW/2-CT, -CT), (CW/2+CT, -CT), (CW/2+CT, H), (CW/2+CB100+THK, H), (CW/2+CB100+THK, -THK-CH100), (-CW/2-CB100-THK, -THK-CH100))
    blk.add_lwpolyline(c_poly, close=True, dxfattribs={"layer": "C_OUTLINE"})

    hatch = blk.add_hatch( color=9, dxfattribs={'layer': 'HATCH'})
    hatch.set_pattern_fill("AR-CONC", scale=3, angle=0)
    hatch.paths.add_polyline_path(c_poly, is_closed=True)

    blk.add_lwpolyline(((CW/2+CT/2, H), (CW/2+CT/2, -CT/2), (-CW/2-CT/2, -CT/2), (-CW/2-CT/2 ,H)), close=False, dxfattribs={"layer": "C_OUTLINE"})


draw_frame_xsection(Frame_X)
draw_leaf_xsection(Leaf_X)
draw_hoisting_xsection(Hoist_X)
draw_concrete_xsection(Conc_X)
msp.add_blockref("FrameXSec", (0,0))
msp.add_blockref("LeafXSec", (35,0))
msp.add_blockref("HoistXSec", (THK+CB100+CLEAR_WIDTH/2, FRAME_HEIGHT))
msp.add_blockref("ConcXSec", (THK+CB100+CLEAR_WIDTH/2, 0))
doc.saveas("gate.dxf")