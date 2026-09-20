def add_rect(blk, x, y, w, h, layer):
    """Closed rectangle, lower-left at (x, y)."""
    return blk.add_lwpolyline(
        [(x, y), (x+w, y), (x+w, y+h), (x, y+h)],
        close=True, dxfattribs={"layer": layer},
    )
def add_rect_with_chamfer(blk, x, y, w, h, f, layer):
    """Closed rectangle, lower-left at (x, y)."""
    return blk.add_lwpolyline(
        [(x+f, y), (x+w-f, y), (x+w, y+f), (x+w, y+h-f), (x+w-f, y+h), (x+f, y+h), (x, y+h-f), (x, y+f)],
        close=True, dxfattribs={"layer": layer},
    )

def add_line(blk, p1, p2, layer):
    return blk.add_line(p1, p2, dxfattribs={"layer": layer})

def add_m_line(blk, p1, p2, offsets, layer):
    blk.add_line(p1, p2, dxfattribs={"layer": layer})
    if p1[0] == p2[0]:
        for offset in offsets:
            blk.add_line((p1[0]+offset, p1[1]), (p2[0]+offset, p2[1]), dxfattribs={"layer": layer})
    elif p1[1] == p2[1]:
        for offset in offsets:
            blk.add_line((p1[0], p1[1]+offset), (p2[0], p2[1]+offset), dxfattribs={"layer": layer})
    else:
        return

def create_channel_block(doc, name, h, w, tw, tf, r=8):
    blk = doc.blocks.new(name=name)

    # pts = [
    #     (-w/2, -h/2), (w/2, -h/2), (w/2, -h/2+tf),
    #     (w/2-tw, -h/2+tf), (w/2-tw, h/2-tf),
    #     (w/2, h/2-tf), (w/2, h/2), (-w/2, h/2),
    # ]
    pts = [
        (0, 0), (0, h), (tf,h),
        (tf, tw), (w-tf, tw),
        (w-tf, h), (w, h), (w, 0)
    ]
    blk.add_lwpolyline(pts, close=True, dxfattribs={"layer": "S_CHAN_OUTL"})
    return blk

