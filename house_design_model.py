"""The book and browser use the same current, verified study snapshot."""
import copy
import hashlib
import json
from pathlib import Path

from development_model import load_model

ROOT = Path(__file__).parent
REVISION = 'Design book / 01'


def read_study(number):
    return json.loads((ROOT / f'output/pdf/concept-{number}-study-check.json').read_text())


def load_current_model(mode='Professional'):
    model, _ = load_model()
    data = read_study('24')
    for filename, key in [('library_snug.py', 'source_sha256'),
                          ('two_workspace_office.py', 'office_source_sha256'),
                          ('garden_plant_study.py', 'garden_source_sha256')]:
        assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == data[key], filename
    state = data['model']
    model.rooms = [model.Room(**room) for room in state['rooms']]
    model.R = {room.id: room for room in model.rooms}
    model.doors = [model.Door(**door) for door in state['doors']]
    model.windows = state['windows']
    model.OUTLINE, model.INNER = state['outline'], state['inner']
    model.furniture = copy.deepcopy(data['states'][mode]['furniture'])
    model.routes = copy.deepcopy(data['states'][mode]['routes'])
    return model, data


def roof_surfaces():
    roof = read_study('06b')
    glass = read_study('07b')
    light = read_study('24')['snug_rooflight_reservation_m']
    eave, ridge = roof['main_roof_eave_m'], roof['main_roof_ridge_m']
    low = roof['lower_envelope_top_m']
    surfaces = []

    def face(name, vertices, material):
        surfaces.append(dict(name=name, vertices=vertices, material=material))

    def flat(name, x0, y0, x1, y1, height, material='roof'):
        face(name, [[x0, y0, height], [x1, y0, height], [x1, y1, height], [x0, y1, height]], material)

    flat('Family wing roof envelope', 0, 0, 8.2, 12.8, low)
    x, y, w, d = light
    flat('Guest roof south', 16.2, 0, 22.8, y, low)
    flat('Guest roof north', 16.2, y+d, 22.8, 12.8, low)
    flat('Guest roof east', 16.2, y, x, y+d, low)
    flat('Guest roof west', x+w, y, 22.8, y+d, low)
    flat('Library rooflight reservation', x, y, x+w, y+d, low+.03, 'glass')
    flat('Continuous gym and rear plant roof envelope', 22.8, 8.7, 27.15, 18.4, low)
    face('Main roof courtyard slope', [[0,12.8,eave],[22.8,12.8,eave],[22.8,15.6,ridge],[0,15.6,ridge]], 'roof')
    face('Main roof arrival slope', [[0,15.6,ridge],[22.8,15.6,ridge],[22.8,18.4,eave],[0,18.4,eave]], 'roof')
    face('Garden room glazed roof', [[12.2,9.3,glass['garden_glass_low_m']], [16.2,9.3,glass['garden_glass_low_m']], [16.2,12.8,glass['garden_glass_high_m']], [12.2,12.8,glass['garden_glass_high_m']]], 'glass')
    return surfaces


if __name__ == '__main__':
    for mode in ('Professional', 'Personal', 'Night'):
        model, _ = load_current_model(mode)
        issues = model.verify()
        assert not issues, (mode, issues)
        print(f'{mode}: {len(model.routes)} routes, no issues')
