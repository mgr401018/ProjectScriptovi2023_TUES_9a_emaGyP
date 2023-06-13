WIDTH    = 740
HEIGTH   = 360
FPS      = 60
TILESIZE = 16

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 50
UI_FONT = '.\\graphics\\font\joystix.ttf'
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'.\\graphics\\weapons\\sword\\full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'.\\graphics\\weapons\\rapier\\full.png'}}

monster_data = {
    'orc':{'health':300,'exp':250,'damage':25,'speed':2,'resistance':4,'attack_radius':10,'notice_radius':100},
    'bat':{'health':60,'exp':100,'damage':5,'speed':3,'resistance':12,'attack_radius':13,'notice_radius':120}
}