from dataclasses import dataclass

@dataclass(frozen=True)
class Parameters:
    clear_width: float
    skin_plate_height: float
    wall_height: float
    frame_above_wall: float
    gear_box_dim: tuple[float, float, float]
    spindle_dia: float
    spindle_cover_h: float
    spindle_cover_d: float
    concrete_thickness: float

    # Assumption
    vertical_spacing_assumed: float = 400
    horizontal_spacing_assumed: float = 350

    # Standard fabrication constants
    leaf_clearence: float = 25
    thk:  float = 10.0    # plate thickness
    cb100:   float = 100.0   # channel/beam bearing dimension
    ch100:   float =  50.0   # clear height offset
    cb150:  float = 150.0
    ch150:  float = 75.0
    spindle_unthreaded_portion: float = 200
    spindle_fillet: float = 5
    spindle_support_height_lower: float = 110
    spindle_support_height_upper: float = 200

    # Gear Box constants
    handleaxis: float = 240
    gearbottomplate_offset: float = 50
    gearshaft_cover_outer_r: float = 40
    gearshaft_cover_inner_r: float = 35
    cover_length: float = 30
    gearshafr_r: float = 15
    shaft_length: float = 100
    phlange_r: float = 65

    # Handle Constants
    handle_radius: float = 200
    handle_pipe_radius: float = 10
    handle_pipe_dist: float = 70
    shaftcover_handle_outer_r: float = 25
    shaftcover_handle_inner_r: float = 17
    cover_length_handle: float = 50
    locking_key_depth: float = 8
    locking_key_length: float = 30
    handle_grip_length: float = 175

    # Derived — computed once, available everywhere
    @property
    def frame_height(self) -> float:
        return self.wall_height + self.frame_above_wall

    @property
    def spindle_height(self) -> float:
        return (self.frame_height - self.skin_plate_height
                + self.gear_box_dim[-1] + self.thk*2 - 70)

    @property
    def total_frame_width(self) -> float:
        return (self.clear_width + self.thk*2 + self.cb100 * 2)

    @property
    def leaf_width(self) -> float:
        return (self.clear_width + (self.cb100-self.leaf_clearence)*2)

    # stiffeners
    @property
    def h_s_number(self) -> float:
        return round((self.skin_plate_height-self.ch100)/self.vertical_spacing_assumed)+1
    @property
    def v_s_number(self) -> float:
        return round(self.leaf_width/self.horizontal_spacing_assumed)-1
    @property
    def h_spacing_Calculated(self) -> float:
        return self.leaf_width/(self.v_s_number+1)
    @property
    def v_spacing_Calculated(self) -> float:
        return (self.skin_plate_height-self.ch100)/(self.h_s_number-1)

    
    @property
    def gb_l(self) -> float:  return self.gear_box_dim[0]
    @property
    def gb_w(self) -> float:  return self.gear_box_dim[1]
    @property
    def gb_h(self) -> float:  return self.gear_box_dim[-1]

    @property
    def spindle_cover_ph_dia(self) -> float:
        return self.spindle_cover_d + 80

    @property
    def grip_inner_radius(self) -> float: return self.handle_pipe_radius
    @property
    def grip_outer_radius(self) -> float: return self.handle_pipe_radius + 15

    @property
    def grip_cover_inner_radius(self) -> float: return self.handle_pipe_radius + 4
    @property
    def grip_cover_outer_radius(self) -> float: return self.handle_pipe_radius + 7