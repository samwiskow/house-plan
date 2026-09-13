"""Load the verified development snapshot without regenerating earlier studies."""
import ast
import copy
import hashlib
import json
import sys
import types
from pathlib import Path

ROOT=Path(__file__).parent

def load_model():
    data=json.loads((ROOT/'output/pdf/concept-18-study-check.json').read_text())
    for name,digest in data['model_sources'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Rebuild office_guest_study.py: snapshot source changed: {name}')
    source=ast.parse((ROOT/'plan_model.py').read_text())
    cut=next(i for i,n in enumerate(source.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PALETTE' for t in n.targets))
    m=types.ModuleType('development_plan');m.__file__=str(ROOT/'plan_model.py');sys.modules[m.__name__]=m
    geometry=[n for n in source.body[:cut] if not (
        isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)
        and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='registerFont')]
    exec(compile(ast.Module(body=geometry,type_ignores=[]),m.__file__,'exec'),m.__dict__)
    names={'color','text','line','rect','poly','Plan','paragraph'}
    helpers=[n for n in source.body[cut:] if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    exec(compile(ast.Module(body=helpers,type_ignores=[]),m.__file__,'exec'),m.__dict__)
    state=data['model'];m.rooms=[m.Room(**r) for r in state['rooms']];m.R={r.id:r for r in m.rooms}
    m.doors=[m.Door(**d) for d in state['doors']];m.windows=state['windows'];m.OUTLINE=state['outline'];m.INNER=state['inner']
    m.furniture=copy.deepcopy(data['day_furniture']);m.routes=copy.deepcopy(data['day_routes'])
    m.PW,m.PH=420,297
    m.PALETTE={'paper':'#fffdf8','ink':'#30392f','muted':'#6a6656','line':'#c9c0af','oak':'#c29b66','ivory':'#f1e7d5','green':'#376248','amber':'#af743b','family':'#f1eee6','shared':'#f2e7d5','guest':'#f1eee6','service':'#f4eddf','circulation':'#faf7ef','furniture':'#dcc8a5','wall':'#343b38','wet':'#e3e9e1','garden':'#e5eedf'}
    return m,data
