import json
from pathlib import Path
p=Path('config.json')
config=json.loads(p.read_text())
changed_items=[]
for key in ('hair_color_inheritance','eye_color_inheritance'):
    if key not in config:
        continue
    outer=config[key]
    for parent, inner in outer.items():
        for other_parent, probs in inner.items():
            total=sum(probs.values())
            if total==0:
                continue
            if total!=100:
                items=list(probs.items())
                new={}
                s=0
                for k,v in items[:-1]:
                    val=int(round(v*100/total))
                    new[k]=val
                    s+=val
                last_key=items[-1][0]
                new[last_key]=100-s
                inner[other_parent]=new
                changed_items.append((key,parent,other_parent,total))
if changed_items:
    p.write_text(json.dumps(config,indent=4,ensure_ascii=False))
    print('normalized', changed_items)
else:
    print('already balanced')
