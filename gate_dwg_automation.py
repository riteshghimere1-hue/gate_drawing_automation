import ezdxf
import openpyxl


# Input Parameters
CLEAR_WIDTH = 1300.0        # mm
SKIN_PLATE_HEIGHT = 1500.0   # mm
WALL_HEIGHT = 2100.0        # mm
FRAME_ABOVE_WALL = 900.0    # mm

CB100 = 100
CH100 = 50
BP250 = 250
THK = 10

# Derived Parameters
FRAME_HEIGHT = WALL_HEIGHT + FRAME_ABOVE_WALL

# Create Document
doc = ezdxf.new("R2018", setup=True)   # setup=True loads linetypes + EZDXF dimstyle
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
    W = CLEAR_WIDTH + 75*2
    H = SKIN_PLATE_HEIGHT
    NVS = round(W/350)-1
    NHS = round((H-50)/350)+1
    HC = W/(NVS+1)
    VC = (H-50)/(NHS-1)
    blk.add_lwpolyline(((0, 0), (W, 0), (W, H), (0, H)), close=True, dxfattribs={"layer": "L_OUTLINE"})
    blk.add_lwpolyline(((W/2-42.5, H), (W/2-42.5, H+110), (W/2-42.5-THK, H+110), (W/2-42.5-THK, H)), close=False, dxfattribs={"layer": "L_OUTLINE"})
    blk.add_lwpolyline(((W/2+42.5, H), (W/2+42.5, H+110), (W/2+42.5+THK, H+110), (W/2+42.5+THK, H)), close=False, dxfattribs={"layer": "L_OUTLINE"})
    blk.add_blockref("PIN", (W/2-42.5-THK*2, H+46))
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


draw_frame_xsection(Frame_X)
draw_leaf_xsection(Leaf_X)
msp.add_blockref("FrameXSec", (0,0))
msp.add_blockref("LeafXSec", (35,0))
doc.saveas("gate.dxf")




