import sys,difflib
a=open(sys.argv[1],encoding='utf-8').read().encode().split(b'\n')
b=open(sys.argv[2],encoding='utf-8').read().encode().split(b'\n')
import re
ta=[x for l in a for x in re.findall(rb'\S+|\s+',l+b'\n')]
tb=[x for l in b for x in re.findall(rb'\S+|\s+',l+b'\n')]
sm=difflib.SequenceMatcher(None,ta,tb,autojunk=False)
add=dele=0
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op!='equal':
        dele+=sum(map(len,ta[i1:i2])); add+=sum(map(len,tb[j1:j2]))
print('added',add,'deleted',dele,'size',sum(map(len,tb)))
