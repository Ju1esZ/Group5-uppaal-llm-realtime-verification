"""Python 3标准库结构初筛。不运行UPPAAL，不改raw。"""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
base=Path(__file__).resolve().parents[1]
results=[]
for p in sorted((base/'raw').glob('P*/P*-R*/model.xml')):
    r={'sample':p.parent.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'uppaal':'NOT_RUN'}
    try:
        root=ET.fromstring(p.read_bytes())
        problems=[]
        if root.tag!='nta': problems.append('Root is not nta')
        if not root.findall('template'): problems.append('No templates')
        if not (root.findtext('system') or '').strip(): problems.append('Missing system')
        for t in root.findall('template'):
            ids=[x.get('id') for x in t.findall('location')]
            if None in ids or len(ids)!=len(set(ids)): problems.append('Invalid location IDs')
            init=t.find('init')
            if init is None or init.get('ref') not in ids: problems.append('Invalid init')
            for e in t.findall('transition'):
                for k in ['source','target']:
                    el=e.find(k)
                    if el is None or el.get('ref') not in ids: problems.append('Invalid '+k)
        r.update(xml_parse='PASS',structure_issues=problems)
    except ET.ParseError as e:r.update(xml_parse='FAIL',error=str(e))
    results.append(r)
(base/'structure_summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Checked {len(results)} models. UPPAAL not run.')
