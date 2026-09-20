import ezdxf
import openpyxl
import math
from config import Parameters
from helpers import *

p = Parameters(
    clear_width=1800,
    skin_plate_height=1000,
    wall_height=1200,
    frame_above_wall=900,
    gear_box_dim=[250, 250, 300],
    spindle_dia=50,
    spindle_cover_h=1000,
    spindle_cover_d=100,
    concrete_thickness=500
)

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
    return dimstyle

dimname = create_dimst("EZDXF", 1, 20, 20)
doc.header["$DIMSTYLE"] = dimname.dxf.name

msp = doc.modelspace()

# LAYERS to use
def setup_layers(doc):
    doc.layers.add("F_OUTLINE",   color=2)
    doc.layers.add("F_HIDDEN",    color=11, linetype="DASHED")
    doc.layers.add("L_OUTLINE",   color=5)
    doc.layers.add("L_HIDDEN",    color=25, linetype="DASHED")
    doc.layers.add("H_OUTLINE",   color=6)
    doc.layers.add("H_HIDDEN",    color=6,  linetype="DASHED")
    doc.layers.add("C_OUTLINE",   color=1)
    doc.layers.add("S_CHAN_OUTL", color=2)
    doc.layers.add("CENTER",      color=1,  linetype="CENTER")
    doc.layers.add("DIM",         color=3)
    doc.layers.add("TEXT",        color=2)
    doc.layers.add("HATCH",       color=9)
    doc.layers.add("ASSY",        color=6)
setup_layers(doc)
create_channel_block(doc, "C100",  h=50, w=100, tw=6, tf=8)
create_channel_block(doc, "C150",  h=75, w=150, tw=8, tf=10)

pinblk = doc.blocks.new(name="PIN")
pinblk.add_lwpolyline(((10,0), (0,0), (0,50), (10,50)), close=True, dxfattribs={"layer": "0"})
pinblk.add_lwpolyline(((10,7.5), (166,7.5), (166,42.5), (10,42.5)), close=False, dxfattribs={"layer": "0"})
pinblk.add_circle((140,25), 5, dxfattribs={"layer": "0"})

Frame_X = doc.blocks.new(name="FrameXSec")
Leaf_X = doc.blocks.new(name="LeafXSec")
Hoist_X = doc.blocks.new(name="HoistXSec")
Conc_X = doc.blocks.new(name="ConcXSec")

def draw_handle(blk):
    tk = p.thk
    hy = p.handleaxis
    hx = p.gb_l/2 + p.cover_length + p.thk*3
    co = p.shaftcover_handle_outer_r
    ci = p.shaftcover_handle_inner_r
    cl = p.cover_length_handle
    kh = p.locking_key_depth
    kl = p.locking_key_length
    hr = p.handle_radius
    pr = p.handle_pipe_radius
    pd = p.handle_pipe_dist
    hcx = pd + tk/2
    hcy = (hr - pr*2 - co)/3

    # Shaft Cover
    add_rect(blk, hx, hy-co, cl, co*2, "H_OUTLINE")
    add_m_line(blk, (hx, hy-ci), (hx+cl, hy-ci), [ci*2], "H_OUTLINE")

    # Locking Key
    add_rect(blk, hx, hy-ci, kl, kh, "H_OUTLINE")

    # Connecting Plates
    blk.add_lwpolyline(((hx+cl/2, hy+co), (hx+cl/2, hy+co+hcy), (hx+cl/2+hcx, hy+co+hcy*2), (hx+cl/2+hcx, hy+co+hcy*3)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((hx+cl/2, hy-co), (hx+cl/2, hy-co-hcy), (hx+cl/2+hcx, hy-co-hcy*2), (hx+cl/2+hcx, hy-co-hcy*3)), close=False, dxfattribs={"layer": "H_OUTLINE"})

    blk.add_lwpolyline(((hx+cl/2-tk, hy+co), (hx+cl/2-tk, hy+co+hcy+tk/2), (hx+cl/2+hcx-tk, hy+co+hcy*2+tk/2), (hx+cl/2+hcx-tk, hy+co+hcy*3)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_lwpolyline(((hx+cl/2-tk, hy-co), (hx+cl/2-tk, hy-co-hcy-tk/2), (hx+cl/2+hcx-tk, hy-co-hcy*2-tk/2), (hx+cl/2+hcx-tk, hy-co-hcy*3)), close=False, dxfattribs={"layer": "H_OUTLINE"})
    
    # Handle Pipe
    blk.add_circle((hx+cl/2+pd, hy+hr-pr), pr, dxfattribs={"layer": "H_OUTLINE"})
    blk.add_circle((hx+cl/2+pd, hy-hr+pr), pr, dxfattribs={"layer": "H_OUTLINE"})
    add_m_line(blk, (hx+cl/2+pd-pr, hy+hr-pr), (hx+cl/2+pd-pr, hy-hr+pr), [pr*2], "H_OUTLINE")

    # Handle Grip
    gl = p.handle_grip_length
    gr_i = p.grip_inner_radius
    gr_o = p.grip_outer_radius
    gx = hx + cl/2 + pd
    gy = hy - hr + pr
    add_rect(blk, gx, gy-gr_i, gl-tk/2, gr_i*2, "H_OUTLINE")
    add_rect(blk, gx+gl-tk/2 ,gy-gr_o, tk/2, gr_o*2, "H_OUTLINE")

    # Handle Grip Cover
    gcl = gl - pr - 2.5*tk
    gcr_i = p.grip_cover_inner_radius
    gcr_o = p.grip_cover_outer_radius
    add_rect(blk, gx+pr+tk, gy-gcr_o, gcl, gcr_o*2, "H_OUTLINE")
    add_m_line(blk, (gx+pr+tk, gy-gcr_i), (gx+pr+tk+gcl ,gy-gcr_i), [gcr_i*2], "H_HIDDEN")

def draw_gearbox(blk):
    GBL = p.gb_l
    GBH = p.gb_h
    hy = p.handleaxis
    hx = GBL/2
    THK = p.thk
    O = p.gearbottomplate_offset
    cr1 = p.gearshaft_cover_outer_r
    cr2 = p.gearshaft_cover_inner_r
    cl = p.cover_length
    sr = p.gearshafr_r
    sl = p.shaft_length
    phr = p.phlange_r

    # Gear Box Body
    add_rect(blk, -GBL/2-O, 0, GBL+O*2, THK, "H_OUTLINE")
    add_rect(blk, -GBL/2, THK+GBH, GBL, THK, "H_OUTLINE")
    add_m_line(blk, (-GBL/2,THK), (-GBL/2,THK+GBH), [GBL], "H_OUTLINE")

    # Shaft Cover
    add_m_line(blk, (hx, hy-cr1), (hx+cl, hy-cr1), [cr1-cr2, cr1+cr2, cr1*2], "H_OUTLINE")

    # Shaft
    add_rect(blk, hx, hy-sr, sl, sr*2, "H_OUTLINE")
 
    # phlange
    add_rect(blk, hx+cl, hy-phr, THK*2, phr*2, "H_OUTLINE")
    add_line(blk, (hx+cl+THK, hy-phr), (hx+cl+THK, hy+phr), "H_OUTLINE")

handle = doc.blocks.new(name="HANDLE")
draw_handle(handle)
g_box = doc.blocks.new(name="GEARBOX")
draw_gearbox(g_box)

def draw_frame_xsection(blk):
    W, H = p.clear_width, p.frame_height
    THK = p.thk
    TW = p.total_frame_width
    CB100 = p.cb100
    CH100 = p.ch100

    # Side Plate
    add_rect(blk, 0, 0, THK, H-300, "F_OUTLINE")
    add_rect(blk, TW-THK, 0, THK, H-300, "F_OUTLINE")

    # Side Chanel
    add_rect(blk, THK, 0, CB100, H, "F_OUTLINE")
    add_rect(blk, TW-THK-CB100, 0, CB100, H, "F_OUTLINE")
    add_m_line(blk, (THK*2, 0), (THK*2, H-CB100), [CB100-2*THK, CB100+W, CB100*2+W-2*THK], "F_HIDDEN")

    # Top Channel
    add_rect(blk, THK, H-CB100, TW-THK*2, CB100, "F_OUTLINE")
    add_m_line(blk, (THK, H-CB100+THK), (TW-THK, H-CB100+THK), [CB100-THK*2], "F_HIDDEN")

    # Bottom plate
    add_rect(blk, 0, 0, TW, -THK, "F_OUTLINE")

    # Bottom Channel
    add_rect(blk, 0, -THK, TW, -CH100, "F_OUTLINE")
    add_line(blk, (0, -THK-THK), (TW, -THK-THK), "F_HIDDEN")


def draw_leaf_xsection(blk):
    CH100 = p.ch100
    THK = p.thk
    SR = p.spindle_dia/2
    W = p.leaf_width
    H = p.skin_plate_height
    NVS = p.v_s_number
    NHS = p.h_s_number
    HC = p.h_spacing_Calculated
    VC = p.v_spacing_Calculated
    ssh = p.spindle_support_height_lower

    # Skin Plate
    add_rect(blk, 0, 0, W, H, "L_OUTLINE")

    # Spindle Support
    add_rect(blk, W/2-SR-THK, H, -THK, ssh, "L_OUTLINE")
    add_rect(blk, W/2+SR+THK, H, THK, ssh, "L_OUTLINE")

    # Locking Pin
    blk.add_blockref("PIN", (W/2-SR-THK*3, H+46), dxfattribs={"layer": "L_OUTLINE"})
    # Center Line
    add_line(blk, (W/2, -300), (W/2, H+300), "CENTER")

    # Stiffeners
    for i in range(NHS):
        add_rect(blk, 0, i*VC, W/2, CH100, "L_OUTLINE")
        add_line(blk, (0, i*VC+CH100-THK), (W/2, i*VC+CH100-THK), "L_HIDDEN")

        for j in range(1, NVS):
            if i >= (NHS-1):
                continue
            if j*HC+THK >= W/2:
                continue
            add_rect(blk, j*HC, i*VC+CH100, THK, VC-THK, "L_OUTLINE")

def draw_hoisting_xsection(blk):
    THK = p.thk
    GBH = p.gb_h
    SH = p.spindle_height
    SD = p.spindle_dia
    F = p.spindle_fillet
    SCH = p.spindle_cover_h
    SCD = p.spindle_cover_d
    UTP = p.spindle_unthreaded_portion
    PHD = p.spindle_cover_ph_dia
    ssh = p.spindle_support_height_upper

    blk.add_blockref("HANDLE", (0, 0))
    blk.add_blockref("GEARBOX", (0, 0))

    # Spindle Cover
    add_rect(blk, -SCD/2, GBH+THK*3, SCD, SCH, "H_OUTLINE")
    add_rect(blk, -PHD/2, GBH+THK*2, PHD, THK, "H_OUTLINE")
    add_m_line(blk, (-SCD/2+THK, GBH+THK*3), (-SCD/2+THK ,GBH+THK*3+SCH), [SCD-THK*2], "H_HIDDEN")

    # Spindle
    add_rect_with_chamfer(blk, -SD/2, GBH+THK*3+50-SH, SD, SH, F, "H_OUTLINE")
    add_m_line(blk, (-SD/2+F, GBH+THK*3+50-SH+UTP), (-SD/2+F, GBH+THK*3+50), [SD-2*F], "H_HIDDEN")

    # Spindle Support
    add_rect(blk, SD/2, GBH+THK*3+50-SH+ssh/2, THK, -ssh, "H_OUTLINE")
    add_rect(blk, -SD/2, GBH+THK*3+50-SH+ssh/2, -THK, -ssh, "H_OUTLINE")

def draw_concrete_xsection(blk):
    H = p.wall_height
    CW = p.clear_width
    CT = p.concrete_thickness
    CB100 = p.cb100
    CH100 = p.ch100
    THK = p.thk

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
msp.add_blockref("HoistXSec", (p.thk+p.cb100+p.clear_width/2, p.frame_height))
msp.add_blockref("ConcXSec", (p.thk+p.cb100+p.clear_width/2, 0))
msp.add_blockref("C100", (p.frame_height+1000, p.total_frame_width+1000), dxfattribs={"layer": "S_CHAN_OUTL", "rotation": 90})
msp.add_blockref("C150", (p.frame_height+1500, p.total_frame_width+1500))
doc.saveas("gate.dxf")