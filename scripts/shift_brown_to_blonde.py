import json
from pathlib import Path
p=Path('config.json')
conf=json.loads(p.read_text())
changed=[]
if 'hair_color_inheritance' in conf:
    for parent, inner in conf['hair_color_inheritance'].items():
        for other_parent, probs in inner.items():
            if 'brown' in probs and 'blonde' in probs and probs['brown']>0:
                shift = min(10, probs['brown'])
                probs['brown'] -= shift
                probs['blonde'] = probs.get('blonde',0) + shift
                # normalize to 100
                items=list(probs.items())
                total=sum(v for _,v in items)
                if total!=100 and total>0:
                    new={}
                    s=0
                    for k,v in items[:-1]:
                        val=int(round(v*100/total))
                        new[k]=val
                        s+=val
                    last=items[-1][0]
                    new[last]=100-s
                    inner[other_parent]=new
                changed.append((parent,other_parent))

if changed:
    p.write_text(json.dumps(conf,indent=4,ensure_ascii=False))
    print('modified rows:', changed)
else:
    print('no changes')
