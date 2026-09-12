"""Concept 08: one measured furniture model for plan and two interior views."""
import ast
import copy
import json
import types
from pathlib import Path
from math import tan, radians, cos, sin, pi
import numpy as np
from PIL import Image
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).parent
source = ast.parse((ROOT / 'open_orangery_study.py').read_text())
cut = next(i for i, n in enumerate(source.body) if isinstance(n, ast.Assign)
           and any(isinstance(t, ast.Name) and t.id == 'OUT' for t in n.targets))
study = types.ModuleType('open_plan')
study.__file__ = str(ROOT / 'open_orangery_study.py')
exec(compile(ast.Module(body=source.body[:cut], type_ignores=[]), str(ROOT / 'open_orangery_study.py'), 'exec'), study.__dict__)
m = study.m
original_rooms = copy.deepcopy(m.rooms)
m.furniture = [f for f in m.furniture if f['room'] not in ('KL', 'OR')]
items = []


def item(name, x, y, w, d, kind, material, height, room='KL', facing=None):
    m.furn(room, name, x, y, w, d, kind)
    items.append(dict(name=name, rect=[x, y, w, d], kind=kind, material=material,
                      height=height, room=room, facing=facing))


item('Media unit', .35, 15.35, .4, 2.2, 'cabinet', 'oak', .5)
item('Stove placeholder', .60, 13.95, .55, .60, 'stove', 'charcoal', 1.05)
item('Sofa', 4.6, 14.85, 1, 2.8, 'sofa', 'oatmeal', .86, facing='west')
item('Armchair A', 2.1, 14.7, .85, .85, 'chair', 'linen', .82, facing='south')
item('Armchair B', 1.3, 16.8, .85, .85, 'chair', 'linen', .82, facing='east')
item('Lounge table', 3, 15.5, .8, 1.2, 'table', 'oak', .38)
item('Dining table', 7.85, 14.2, 1, 3, 'table', 'oak', .75)
for y in [14.325, 15.075, 15.825, 16.575]:
    item('Dining chair', 7.3, y, .5, .5, 'diningchair', 'oak', .82, facing='east')
    item('Dining chair', 8.9, y, .5, .5, 'diningchair', 'oak', .82, facing='west')
item('Island', 10.95, 14.95, 2.8, 1.05, 'island', 'green', .92)
for x in [11.3, 12.1, 12.9]:
    item('Island stool', x, 14.30, .5, .5, 'stool', 'oak', .68, facing='south')
# Module positions are spatial allowances, not a supplier's cabinet schedule.
for name, x, width in [('Drawers', 9.8, 1), ('Sink base', 10.8, .8),
                       ('Dishwasher', 11.6, .6), ('Bins', 12.2, .4)]:
    item(name, x, 17.45, width, .6, 'kitchen', 'ivory', .92)
item('Oven tower', 12.6, 17.45, .6, .6, 'tall', 'ivory', 2.2)
item('Fridge / freezer', 13.2, 17.45, .6, .6, 'tall', 'ivory', 2.2)
item('Garden sofa', 12.7, 10.25, .85, 1.8, 'sofa', 'oatmeal', .82, 'OR', 'east')
item('Garden table', 13.8, 11, .6, .6, 'table', 'oak', .4, 'OR')
item('Garden chair', 15.35, 10.3, .85, .85, 'chair', 'linen', .82, 'OR', 'west')
HEARTH = [.35, 13.5, 1.35, 1.5]
RUG = [2.25, 15.7, 3.45, 2.10]
HOB = [12.55, 15.43, .8, .45]
SINK = [10.92, 17.51, .56, .42]
m.routes['Garden sitting to dining'] = [(14.85, 12.25), (14.85, 13.85), (10.2, 13.85)]
m.routes['Garden door approach'] = [(14.85, 13.8), (14.85, 11.8), (14.85, 10.15), (14.4, 10.05)]
m.routes['Dining to cooking aisle'] = [(10.52, 13.85), (10.52, 16.65), (12.0, 16.7)]
m.routes['Rear of dining'] = [(6.1, 17.65), (9.35, 17.65)]
m.routes['Lounge approach'] = [(6.1, 13.85), (3.95, 13.85), (3.8, 14.65)]
issues = m.verify()
assert not issues, issues
assert m.rooms == original_rooms
for f in m.furniture:
    if f['room'] == 'KL' and f['name'] != 'Stove placeholder':
        assert m.overlap(HEARTH, f['rect']) == 0, f['name']
assert m.overlap(HEARTH, RUG) == 0

OUT = ROOT / 'output/pdf'
TMP = ROOT / 'tmp/pdfs/concept-08'
TMP.mkdir(parents=True, exist_ok=True)
PDF = OUT / 'concept-08-shared-space.pdf'
C = {'paper': '#fffdf8', 'ivory': '#f6edde', 'floor': '#dfceb0', 'floor_alt': '#e3d2b5', 'oak': '#ba915e',
     'green': '#244b36', 'oatmeal': '#c2ad8a', 'linen': '#e7d9bd', 'stone': '#d4bd92',
     'charcoal': '#34352e', 'bronze': '#7f6241', 'sky': '#e6eee5', 'garden': '#aebf91',
     'ink': '#30392f', 'muted': '#666553', 'line': '#c6bcaa', 'rug': '#e2d4b8',
     'worktop': '#edddbd', 'glass': '#dce9df'}
m.PALETTE.update(C)
m.c = m.canvas.Canvas(str(PDF), pagesize=(420*m.mm, 297*m.mm))
m.c.setTitle('Concept 08 - coordinated shared space')
m.c.setAuthor('House plan working study')


def txt(x, y, value, size=3, bold=False, **kw):
    m.text(x, y, value, size, 'Helvetica-Bold' if bold else 'Helvetica', **kw)


def header(page, title, sub):
    m.rect(0, 0, 420, 297, 'paper', None)
    txt(14, 12, 'COURTYARD HOUSE / CONCEPT 08 / SHARED SPACE', 2.7, fill='muted')
    txt(14, 23, title, 6.2, True)
    txt(14, 31, sub, 2.85, fill='muted')
    m.line(14, 36, 406, 36, 'line', .3)
    m.line(14, 280, 406, 280, 'line', .25)
    txt(14, 287, 'WORKING PROPOSAL | Furniture, appliances and heights are study sizes. Structure, stove installation and thermal performance remain open.', 2.35, fill='muted')
    txt(406, 287, f'{page} / 3', 2.6, align='right', fill='muted')


def note(x, y, title, lines):
    txt(x, y, title, 3.15, True)
    m.paragraph(x, y+7, lines, size=2.75, step=4.8)


def badge(p, x, y, label):
    X, Y = p.xy((x, y))
    m.rect(X-3, Y-3, 6, 5.5, 'paper', 'muted', .15)
    txt(X, Y+1, label, 2.6, True, align='center')


header(1, 'One room, four places to spend time', 'Enlarged furnished plan 1:50 at A3, printed at 100% | Concept 07 walls and openings retained | All dimensions in metres')
p = m.Plan(20, -138, 20, True)
m.c.saveState()
clip = m.c.beginPath(); clip.rect(14*m.mm, (297-230)*m.mm, 392*m.mm, 190*m.mm)
m.c.clipPath(clip, stroke=0)
saved_furniture = m.furniture
m.furniture = []
saved_doors = m.doors
m.doors = [d for d in m.doors if d.id not in ('O05', 'O07')]
m.PALETTE.update({'shared': C['floor'], 'family': '#f5f0e6', 'service': '#f5f0e6', 'circulation': '#f5f0e6', 'guest': '#f5f0e6'})
p.draw(labels=False)
m.furniture, m.doors = saved_furniture, saved_doors
p.rect(*RUG, 'rug', None)
p.rect(*HEARTH, 'stone', 'muted', .2)
for f in items:
    x, y, w, d = f['rect']
    p.rect(x, y, w, d, f['material'], 'muted', .15)
    if f['kind'] in ('sofa', 'chair', 'diningchair'):
        b = .18 if f['kind'] != 'diningchair' else .07
        facing = f['facing']
        back = {'west': (x+w-b, y, b, d), 'east': (x, y, b, d),
                'north': (x, y+d-b, w, b), 'south': (x, y, w, b)}[facing]
        p.rect(*back, f['material'], 'muted', .12)
    if f['kind'] == 'stove':
        p.line((x+w, y+.07), (x+w, y+d-.07), 'bronze', .65)
    if f['kind'] == 'tall':
        p.line((x, y), (x+w, y+d), 'muted', .1)
p.rect(*HOB, 'charcoal', 'muted')
p.rect(*SINK, 'glass', 'muted')
p.text(11.85, 15.45, 'PREP', 2.1, fill='paper')
p.text(13.0, 15.69, 'HOB', 1.9, fill='paper')
for x, label in [(10.3, 'DRAWERS'), (11.2, 'SINK'), (11.9, 'DW'), (12.4, 'BIN'), (12.9, 'OV'), (13.5, 'FF')]:
    p.text(x, 17.81, label, 1.85)
for name in ['Guests to living', 'Garden door approach', 'Dining to cooking aisle', 'Rear of dining']:
    for a, b in zip(m.routes[name], m.routes[name][1:]):
        p.line(a, b, 'green', .3, [2, 1.3])
p.dimension((7.85, 14.2), (7.85, 17.2), -.85, '3.00 table', True)
p.dimension((10.95, 14.95), (13.75, 14.95), 1.7, '2.80 island')
p.dimension((10.75, 16.0), (10.75, 17.45), -.15, '1.45 aisle', True)
p.dimension((12.55, 9.65), (16.55, 9.65), -.5, '4.00 open garden zone')
p.text(14.6, 12.7, 'GARDEN SITTING / 14.0 m2', 2.6)
p.text(8.2, 17.90, 'DINING / EIGHT PLACES', 2.6)
p.text(3.05, 17.98, 'LOUNGE', 2.6)
p.text(15.1, 16.5, 'PANTRY', 2.6, fill='muted')
p.text(17.25, 17.0, 'ENTRANCE', 2.35, fill='muted')
p.text(18.85, 10.7, 'SNUG', 2.6, fill='muted')
p.text(18.85, 12.95, 'WC', 2.6, fill='muted')
p.text(10.15, 12.0, 'COURTYARD', 2.6, fill='muted')
p.text(17.1, 10.0, 'D17', 2.3, fill='muted')
for x, y, label in [(.95, 13.2, '1'), (8.35, 15.7, '2'), (12.0, 16.0, '3'), (14.45, 10.05, '4')]:
    badge(p, x, y, label)
CAMERAS = [((8.2, 13.8, 1.6), (.6, 15.65, 1.65)), ((7.2, 17.6, 1.6), (14.0, 13.0, 2.15))]
for i, (cam, target) in enumerate(CAMERAS):
    dx, dy = target[0]-cam[0], target[1]-cam[1]
    norm = (dx*dx+dy*dy)**.5
    end = (cam[0]+dx/norm*.7, cam[1]+dy/norm*.7)
    p.line(cam[:2], end, 'bronze', .55)
    p.line(end, (end[0]-.2*dx/norm+.12*dy/norm, end[1]-.2*dy/norm-.12*dx/norm), 'bronze', .4)
    badge(p, cam[0], cam[1], chr(65+i))
m.c.restoreState()
m.rect(14, 37, 241, 72, 'paper', None)
note(20, 49, '1 / THE LOUNGE', ['2.80 x 1.00 sofa stays facing the media wall.', 'Shorter 2.20 media unit; north chair moved.', '1.35 x 1.50 hearth zone reserves the stove end.', 'Hearth size and appliance clearances unverified.'])
note(143, 49, '2 / DINING + 3 / KITCHEN', ['3.00 x 1.00 table; four chairs on each long side.', 'Island moved 0.45 toward the rear counter.', 'Three stools now face in from the garden side.', '1.45 clear between island and rear worktop.'])
for i in range(5): p.rect(i+.35, 18.75, 1, .1, 'ink' if i%2==0 else 'paper', 'ink', .1)
p.text(2.85, 19.15, '5 m scale bar', 2.4)
p.dimension((.35, 18.05), (17.75, 18.05), 1.15, '17.40 m shared-room envelope (stepped at pantry)')
note(20, 252, '4 / GARDEN SITTING', ['1.80 x 0.85 sofa, one chair and a small table.', 'The central approach to the sliding door stays open.', 'Same floor; shading and vent controls still to place.'])
note(153, 252, 'KITCHEN MODULE ALLOWANCES', ['2.80 base run: drawers, sink, dishwasher and bins.', 'Two 0.60 towers: ovens and fridge/freezer.', 'Island hob / extraction route needs coordination.'])
note(287, 252, 'READING THE PLAN', ['Green dashed lines: selected 0.70 m route checks.', 'A and B: interior cameras; plan top is not north.', '1.20 to island with chairs pulled out by 0.35.'])
m.c.showPage()

# The interior drawings use a depth buffer, so surfaces obscure one another correctly.
faces = []


def face(points, material):
    faces.append((np.array(points, dtype=float), material))


def cube(x, y, z, w, d, h, material):
    face([(x,y,z),(x,y+d,z),(x,y+d,z+h),(x,y,z+h)], material)
    face([(x+w,y,z),(x+w,y,z+h),(x+w,y+d,z+h),(x+w,y+d,z)], material)
    face([(x,y,z),(x,y,z+h),(x+w,y,z+h),(x+w,y,z)], material)
    face([(x,y+d,z),(x+w,y+d,z),(x+w,y+d,z+h),(x,y+d,z+h)], material)
    face([(x,y,z+h),(x,y+d,z+h),(x+w,y+d,z+h),(x+w,y,z+h)], material)


def ceiling(y):
    return 3.5 + min(y-13.15, 18.05-y)*tan(radians(30))


def wall_y(y, x0, x1, height, openings=(), material='ivory', glazed=()):
    cuts = sorted(set([x0, x1]+[v for a,b,lo,hi in openings for v in (a,b)]))
    for a, b in zip(cuts, cuts[1:]):
        holes = [(lo,hi) for l,r,lo,hi in openings if l <= (a+b)/2 <= r]
        for lo, hi in ([(0,height)] if not holes else [(0,holes[0][0]),(holes[0][1],height)]):
            if hi>lo: face([(a,y,lo),(b,y,lo),(b,y,hi),(a,y,hi)], material)
    for a,b,lo,hi in openings:
        mat = 'glass' if hi>2.2 else 'ivory'
        if lo>0:
            face([(a,y+.005,lo),(b,y+.005,lo),(b,y+.005,hi),(a,y+.005,hi)], mat)
        if a in glazed:
            for x in [a, (a+b)/2, b]: cube(x-.022,y-.02,lo,.044,.04,hi-lo,'bronze')
            for z in [lo,hi]: cube(a,y-.02,z,b-a,.04,.035,'bronze')


# Floor tiles follow the L-shaped shared room and continue into the garden zone.
for room_id in ['KL', 'OR', 'GH2', 'PA', 'H', 'S', 'WC']:
    poly = m.R[room_id].poly
    xmin, xmax = min(x for x,y in poly), max(x for x,y in poly)
    ymin, ymax = min(y for x,y in poly), max(y for x,y in poly)
    xs = sorted(set([xmin,xmax]+[x for x,y in poly]+list(np.arange(np.ceil(xmin/1.2)*1.2,xmax,1.2))))
    ys = sorted(set([ymin,ymax]+[y for x,y in poly]+list(np.arange(np.ceil(ymin/.6)*.6,ymax,.6))))
    for x,xx in zip(xs,xs[1:]):
        for y,yy in zip(ys,ys[1:]):
            if m.inside(((x+xx)/2,(y+yy)/2),poly):
                face([(x,y,0),(xx,y,0),(xx,yy,0),(x,yy,0)], 'floor_alt' if (int(x/1.2)+int(y/.6))%3==0 else 'floor')
wall_y(13.15,.35,17.75,3.5,[(3.5,4.4,0,2.2),(9,11.6,0,2.7),(12.55,16.55,0,3.1),(16.6,17.7,0,2.6)], glazed=(9,))
cube(3.5,13.12,0,.9,.045,2.2,'ivory')
wall_y(18.05,.35,13.88,3.5,[(1.1,4.2,.75,2.35),(6.6,9.6,.75,2.35),(10.5,12.5,1.12,2.35)], glazed=(1.1,6.6,10.5))
face([(.35,13.15,0),(.35,18.05,0),(.35,18.05,3.5),(.35,15.6,ceiling(15.6)),(.35,13.15,3.5)],'ivory')
wall_y(15.33,13.88,17.75,ceiling(15.33),[(16.65,17.6,0,2.2)])
wall_y(18.05,13.88,19.03,2.6)
face([(22.45,9.46,0),(22.45,13.58,0),(22.45,13.58,2.6),(22.45,9.46,2.6)],'ivory')
for a,b in [(15.33,15.6),(15.6,16.05),(16.95,18.05)]:
    face([(13.88,a,0),(13.88,b,0),(13.88,b,ceiling(b)),(13.88,a,ceiling(a))],'ivory')
face([(13.88,16.05,2.2),(13.88,16.95,2.2),(13.88,16.95,ceiling(16.95)),(13.88,16.05,ceiling(16.05))],'ivory')
# Ceiling faces follow the same footprint as the shared-room floor.
for x0,x1,ymax in [(.35,13.88,18.05),(13.88,17.75,15.33)]:
    cuts = [13.15]+([15.6] if ymax>15.6 else [])+[ymax]
    for y,yy in zip(cuts,cuts[1:]):
        face([(x0,y,ceiling(y)),(x1,y,ceiling(y)),(x1,yy,ceiling(yy)),(x0,yy,ceiling(yy))],'ivory')
# Courtyard backdrop and retained garden room openings.
face([(8.2,3,-.03),(16.2,3,-.03),(16.2,13.15,-.03),(8.2,13.15,-.03)],'garden')
face([(8.2,3,0),(8.2,12.8,0),(8.2,12.8,3.2),(8.2,3,3.2)],'stone')
for y in [4.8,9.2]: face([(8.205,y,.75),(8.205,y+2,.75),(8.205,y+2,2.35),(8.205,y,2.35)],'glass')
wall_y(9.65,12.55,16.55,2.85,[(13,15.8,0,2.35)], glazed=(13,))
for a,b,lo,hi in [(9.65,10.4,0,2.85),(11.9,13.15,0,3.1),(10.4,11.9,0,.65),(10.4,11.9,2.35,2.9)]:
    face([(12.55,a,lo),(12.55,b,lo),(12.55,b,hi),(12.55,a,hi)],'ivory')
face([(12.55,10.4,.65),(12.55,11.9,.65),(12.55,11.9,2.35),(12.55,10.4,2.35)],'glass')
wall_y(9.46,16.55,17.75,2.6,[(16.7,17.6,0,2.2)])
cube(16.7,9.465,0,.9,.04,2.2,'oak')
for a,b in [(9.46,10.35),(11.25,12.4)]:
    face([(17.75,a,0),(17.75,b,0),(17.75,b,2.6),(17.75,a,2.6)],'ivory')
face([(17.75,13.15,0),(17.75,15.33,0),(17.75,15.33,ceiling(15.33)),(17.75,13.15,3.5)],'ivory')
face([(16.55,9.46,2.6),(17.75,9.46,2.6),(17.75,13.15,2.6),(16.55,13.15,2.6)],'ivory')
face([(16.55,9.65,2.6),(16.55,12.8,2.6),(16.55,12.8,3.45),(16.55,9.65,2.91)],'ivory')
glass = lambda y: 2.85+(y-9.3)*.6/3.5
face([(12.55,9.65,glass(9.65)),(16.55,9.65,glass(9.65)),(16.55,12.8,3.45),(12.55,12.8,3.45)],'sky')
for x in [12.55,13.55,14.55,15.55,16.55]:
    face([(x-.025,9.65,glass(9.65)-.07),(x+.025,9.65,glass(9.65)-.07),(x+.025,12.8,3.38),(x-.025,12.8,3.38)],'bronze')
for y in [9.65,11.2,12.8]: cube(12.55,y,glass(y)-.07,4,.04,.04,'bronze')
face([(12.55,12.8,3.1),(16.55,12.8,3.1),(16.55,13.15,3.1),(12.55,13.15,3.1)],'ivory')
cube(*RUG[:2],.004,*RUG[2:],.006,'rug')
cube(*HEARTH[:2],.006,*HEARTH[2:],.025,'stone')


def legs(x,y,w,d,top,material,thick=.045):
    for xx in [x+.06,x+w-.06-thick]:
        for yy in [y+.06,y+d-.06-thick]: cube(xx,yy,0,thick,thick,top,material)


for f in items:
    x,y,w,d=f['rect']; h=f['height']; mat=f['material']; kind=f['kind']
    if kind in ['table','stool','diningchair']:
        seat = .46 if kind=='diningchair' else h
        legs(x,y,w,d,seat-.05,mat)
        cube(x,y,seat-.05,w,d,.05,mat)
        if kind=='diningchair':
            back={'west':(x+w-.05,y,.05,d),'east':(x,y,.05,d),'north':(x,y+d-.05,w,.05),'south':(x,y,w,.05)}[f['facing']]
            cube(back[0],back[1],.48,back[2],back[3],h-.48,mat)
    elif kind in ['sofa','chair']:
        legs(x,y,w,d,.18,'oak')
        cube(x,y,.16,w,d,.27,mat)
        b=.18
        back={'west':(x+w-b,y,b,d),'east':(x,y,b,d),'north':(x,y+d-b,w,b),'south':(x,y,w,b)}[f['facing']]
        cube(back[0],back[1],.43,back[2],back[3],h-.43,mat)
        if f['facing'] in ['west','east']:
            for yy in [y,y+d-.13]: cube(x,yy,.43,w,.13,.17,mat)
        else:
            for xx in [x,x+w-.13]: cube(xx,y,.43,.13,d,.17,mat)
    elif kind=='island':
        cube(x+.04,y+.3,.10,w-.08,d-.34,h-.14,'green')
        cube(x,y,h-.04,w,d,.04,'worktop')
        for xx in [x+.05,x+.98,x+1.91]:
            cube(xx,y+d-.026,.20,.85,.024,.56,'green')
            cube(xx+.30,y+d,.70,.23,.018,.016,'bronze')
    elif kind in ['kitchen','tall']:
        cube(x+.015,y+.015,.10,w-.03,d-.015,h-(.14 if kind=='kitchen' else .10),mat)
        if kind=='kitchen': cube(x,y,h-.035,w,d,.035,'worktop')
        cube(x+.06,y-.003,.20,w-.12,.018,(h-.30 if kind=='tall' else .59),mat)
        cube(x+w-.11,y-.027,.62,.018,.025,.16,'bronze')
        if f['name']=='Oven tower': cube(x+.055,y-.03,.85,w-.11,.035,.60,'charcoal')
    elif kind=='stove':
        cube(x,y,.16,w,d,h-.16,mat)
        cube(x+w,y+.06,.32,.012,d-.12,.5,'charcoal')
        cube(x+w+.013,y+.15,.40,.014,d-.3,.12,'bronze')
        # Flue centre is located; diameter and installation assembly are illustrative.
        flue=((x+.26,y+.29,h),(x+.26,y+.29,ceiling(y+.29)))
    else:
        cube(x,y,.10,w,d,h-.10,mat)
        if kind=='cabinet':
            for yy in np.arange(y+.05,y+d,.55): cube(x+w,yy,.14,.006,.014,h-.2,'bronze')
# TV, kitchen fittings and dining light are located objects, not extra floor furniture.
cube(.37,15.76,.94,.055,1.35,.77,'charcoal')
cube(*HOB[:2],.925,*HOB[2:],.012,'charcoal')
cube(*SINK[:2],.925,*SINK[2:],.007,'bronze')
cube(11.2,17.96,.93,.025,.025,.30,'bronze')
cube(11.2,17.80,1.20,.025,.18,.025,'bronze')
def cylinder(a, b, radius, material, top_radius=None):
    a,b=np.array(a),np.array(b)
    axis=b-a;axis=axis/np.linalg.norm(axis)
    u=np.cross(axis, [1,0,0] if abs(axis[0])<.9 else [0,1,0]);u/=np.linalg.norm(u)
    v=np.cross(axis,u)
    ring=[cos(t)*u+sin(t)*v for t in np.linspace(0,2*pi,17)[:-1]]
    lower=[a+radius*r for r in ring]
    upper=[b+(radius if top_radius is None else top_radius)*r for r in ring]
    face(lower,material);face(upper,material)
    for i in range(16):face([lower[i],lower[(i+1)%16],upper[(i+1)%16],upper[i]],material)


cylinder(*flue,.08,'charcoal')
cylinder((8.35,15.7,2.22),(8.35,15.7,ceiling(15.7)),.013,'bronze')
for a in range(6):
    angle=a*pi/3;xx=8.35+.56*cos(angle);yy=15.7+.56*sin(angle)
    cylinder((8.35,15.7,2.23),(xx,yy,2.23),.014,'bronze')
    cylinder((xx,yy,2.24),(xx,yy,2.48),.13,'linen',.085)


def render(cam, target, destination):
    cam=np.array(cam); forward=np.array(target)-cam; forward/=np.linalg.norm(forward)
    right=np.cross([0,0,1],forward); right/=np.linalg.norm(right)
    up=np.cross(forward,right)
    basis=np.array([right,up,forward])
    width,height=2200,1020
    focal=width/(2*tan(radians(94)/2))
    zbuf=np.full((height,width),np.inf)
    pixels=np.empty((height,width,3),dtype=np.uint8); pixels[:]=[235,239,226]
    normals=np.zeros((height,width,3),dtype=np.float32)
    light=np.array([-.3,-.5,.8]);light/=np.linalg.norm(light)
    for world,material in faces:
        normal=np.cross(world[1]-world[0],world[2]-world[0])
        norm=np.linalg.norm(normal)
        if norm<1e-9: continue
        normal/=norm
        if np.dot(normal,cam-world.mean(axis=0))<0:normal=-normal
        shade=.94+.06*max(0,np.dot(normal,light))
        if material in ['sky','glass']:shade=1
        base=np.array([int(C[material][i:i+2],16) for i in [1,3,5]])
        colour=np.clip(base*shade,0,255).astype(np.uint8)
        view=(world-cam)@basis.T
        clipped=[]
        for a,b in zip(view,np.roll(view,-1,axis=0)):
            if a[2]>=.12: clipped.append(a)
            if (a[2]>=.12)!=(b[2]>=.12): clipped.append(a+(.12-a[2])/(b[2]-a[2])*(b-a))
        if len(clipped)<3:continue
        points=np.array(clipped)
        screen=np.column_stack([width/2+focal*points[:,0]/points[:,2],height/2-focal*points[:,1]/points[:,2]])
        for i in range(1,len(points)-1):
            ids=[0,i,i+1]; tri=screen[ids]; inv=1/points[ids,2]
            xmin=max(0,int(np.floor(tri[:,0].min())));xmax=min(width-1,int(np.ceil(tri[:,0].max())))
            ymin=max(0,int(np.floor(tri[:,1].min())));ymax=min(height-1,int(np.ceil(tri[:,1].max())))
            if xmin>xmax or ymin>ymax:continue
            a,b,d=tri
            denom=(b[1]-d[1])*(a[0]-d[0])+(d[0]-b[0])*(a[1]-d[1])
            if abs(denom)<1e-8:continue
            yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1]
            u=((b[1]-d[1])*(xx-d[0])+(d[0]-b[0])*(yy-d[1]))/denom
            v=((d[1]-a[1])*(xx-d[0])+(a[0]-d[0])*(yy-d[1]))/denom
            w=1-u-v
            valid=(u>=0)&(v>=0)&(w>=0)
            depth=1/np.maximum(1e-9,u*inv[0]+v*inv[1]+w*inv[2])
            region=zbuf[ymin:ymax+1,xmin:xmax+1]
            mask=valid&(depth<region)
            region[mask]=depth[mask]
            pixels[ymin:ymax+1,xmin:xmax+1][mask]=colour
            normals[ymin:ymax+1,xmin:xmax+1][mask]=normal
    edge=np.zeros((height,width),dtype=bool)
    for axis in [0,1]:
        delta=np.linalg.norm(normals-np.roll(normals,1,axis=axis),axis=2)
        edge|=delta>.45
    edge[0,:]=False;edge[:,0]=False
    pixels[edge]=(pixels[edge]*.78).astype(np.uint8)
    Image.fromarray(pixels).resize((1800,835),Image.Resampling.LANCZOS).save(destination)
    marks = []
    for marker in ([(.7,14.25,1.2),(.7,16.4,1.2)] if forward[0] < 0 else [(17.15,11.5,1.6),(14.5,11.5,1.6)]):
        q=(np.array(marker)-cam)@basis.T
        marks.append(float(q[0]/q[2]))
    assert marks[0]>marks[1], 'Interior view orientation is inverted'
    return {'orientation_marker_x_over_depth':marks,'camera_m':cam.tolist(),'target_m':list(target),'horizontal_fov_degrees':94}


views=[]
for i,(cam,target) in enumerate(CAMERAS):
    path=TMP/f'interior-{i+1}.png'
    views.append(render(cam,target,path))
    if i==0:
        header(2,'A settled lounge at the end of the vault','View A / Eye height 1.60 m, from the dining-side approach toward the media wall | Geometry-based illustration')
    else:
        header(3,'Dining, kitchen and garden sitting belong together','View B / Eye height 1.60 m, from beside dining toward the kitchen and open garden room | Geometry-based illustration')
    m.c.drawImage(ImageReader(str(path)),14*m.mm,(297-228)*m.mm,392*m.mm,181.75*m.mm)
    m.line(14,234,406,234,'line',.25)
    if i==0:
        note(20,245,'WHAT CHANGES',['The sofa stays in arrangement A, facing the same wall.', 'A shorter oak media unit makes room for the stove end.', 'The north chair moves; the rug stops short of the hearth.'])
        note(225,245,'WHAT STILL NEEDS TO FIT',['Stove, TV heat exposure, hearth build-up and roof penetration.', 'The dark flue marks a route; its assembly is not designed.', 'See HETAS installation guidance and the selected appliance manual.'])
        m.c.linkURL('https://www.hetas.co.uk/consumer/services/installers/',(225*m.mm,26*m.mm,405*m.mm,32*m.mm),relative=0)
    else:
        note(20,245,'WHAT CONNECTS THE ROOM',['Ivory vault, forest-green island, warm floor and honey oak.', 'The longer table turns toward the court; both ends stay clear.', 'The garden sitting area remains open beside the shared hall.'])
        note(225,245,'WHAT STILL NEEDS COORDINATION',['Island hob extraction, cabinet fillers and appliance openings.', 'Lighting is provisional; adjacent rooms are simplified.', 'Garden-room framing, external shading and ventilation remain open.'])
    m.c.showPage()
m.c.save()

# Extra use scenarios deliberately go beyond static furniture-fit checks.
clearances = {'island_to_rear_worktop_m':17.45-16.0,
              'island_to_tall_front_m':17.45-16.0,
              'garden_central_gap_m':15.35-14.4,
              'courtyard_table_end_m':14.2-13.15,
              'rear_table_end_m':18.05-17.2}
assert abs(clearances['island_to_rear_worktop_m']-1.45)<1e-6
pullout=[]
for f in items:
    if f['name']!='Dining chair':continue
    dx,dy={'south':(0,-.35),'north':(0,.35),'east':(-.35,0),'west':(.35,0)}[f['facing']]
    x,y,w,d=f['rect']
    pullout.append(dict(f,rect=[x+dx,y+dy,w,d]))
for chair in pullout:
    assert all(m.inside(point,m.R['KL'].poly) for point in m.box(*chair['rect']))
    assert not any(m.overlap(chair['rect'], f['rect'])>1e-7 for f in items if f['name']!='Dining chair')
for i,chair in enumerate(pullout):
    assert not any(m.overlap(chair['rect'], other['rect'])>1e-7 for other in pullout[i+1:])
clearances['dining_chairs_to_island_normal_m']=10.95-9.4
clearances['dining_chairs_to_island_pulled_out_m']=10.95-(9.4+.35)
clearances['dining_chairs_to_sofa_normal_m']=7.3-5.6
clearances['dining_chairs_to_sofa_pulled_out_m']=7.3-.35-5.6
normal_furniture=m.furniture
m.furniture=[f for f in normal_furniture if f['name']!='Dining chair']+pullout
pulled_issues=m.verify()
m.furniture=normal_furniture
assert not pulled_issues,pulled_issues
assert len(pullout)==8 and all(f['facing'] in ('east','west') for f in pullout)
for f in items:
    if f['name'] in ['Dishwasher','Oven tower','Fridge / freezer']:
        x,y,w,d=f['rect']
        reserved=[x,y-.6,w,.6]
        assert not any(m.overlap(reserved,g['rect'])>1e-7 for g in items)
for cam,target in CAMERAS:
    assert m.inside(cam[:2],m.R['KL'].poly)
    assert not any(m.inside(cam[:2],m.box(*f['rect'])) for f in items)
# A 0.60 dishwasher door projection is reserved; 0.85 remains to the island.
assert abs((17.45-.6)-16.0-.85)<1e-6
checks={'status':'Concept 08 working proposal; not a product or construction specification',
        'plan_geometry':'Concept 07 rooms and openings unchanged','gia_m2':m.GIA,
        'furniture':items,'hearth_reservation_m':HEARTH,'rug_m':RUG,'hob_m':HOB,'sink_m':SINK,
        'route_envelope_m':.70,'checked_routes':list(m.routes),'geometry_issues':issues,
        'clearances':clearances,'dining_chair_pullout_test_m':.35,
        'dining_table_length_width_m':[3.0,1.0],'dining_seat_pitch_m':.75,
        'dining_chairs_per_long_side':4,'dining_end_chairs':0,
        'all_dining_chairs_pulled_out_geometry_issues':pulled_issues,
        'dishwasher_door_projection_assumption_m':.60,'remaining_aisle_with_dishwasher_open_m':.85,
        'appliance_use_limit':'Opening a door reduces working space; does not prove comfortable simultaneous use or accessibility.',
        'cameras':views,'stove_clearance_validation':False,'structural_validation':False,'thermal_validation':False,
        'stove_reference':'https://www.hetas.co.uk/consumer/services/installers/'}
(OUT/'concept-08-study-check.json').write_text(json.dumps(checks,indent=2)+'\n')
print(PDF)
print(f'{len(m.routes)} route checks; {len(issues)} geometry issues; 1.45 m kitchen aisle')
