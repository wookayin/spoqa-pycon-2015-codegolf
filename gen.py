#!/usr/bin/env python3

from __future__ import print_function

OFFSET_MAGIC = 38
SPLIT_MAGIC = 54

PUPU = """
                                                   *******
                                                  **********
                                                 ***********
                                                *************
                                                ********************
                                                ************************
                                                *************************
                                                 *************************
                                  ********        *************************
                                **********          **********************
                             *************           *********************
                             *************          ********************
                       ************************    *******************
                   **************************************
                ****************************************
              ********************************************
             **********************************************
            ************************************************
           *************************************************
          ***************************************************
          ****************************************************
         *************   ***************   *******************
         **********   ****  *********  ****  *****************
         **************************  *************************
          ***********************************  ***************
          ****************************************************
          ****************************************************
        ********************************************************
       ***********************************************************
      ******************************  *******  ********************
     ****************      ***********       **********************
    ***************************************************************
    ***************************************************************
    ***************************************************************
    ***************************************************************
     *************************************************************
      ***********************************************************
       **********************************************************
        ********************************************************
         *****************************************************
            ************************************************
                ***************************************
"""


def analyze_pupu(PUPU_LINES):
    b = []
    for idx, line in enumerate(PUPU_LINES):
        if not line: continue
        bi = encode_line(idx, line, True)
        b += bi

    B = OFFSET_MAGIC
    print('')
    print('Min, max = ', min(t+B for t in b), max(t+B for t in b))
    s = ''.join([chr(t + B) for t in b])
    assert not '"' in s, "quote trap"
    return s

def encode_line(line_idx, l,sep=True):
    i = 0
    n = len(l)
    a = []
    while i < n:
        j = i
        while j < n and l[i] == l[j]: j += 1
        chunk_sz = j - i
        a.append(chunk_sz)
        #print("(%d,%d)" % (chunk_sz, j),)
        i = j
    if sep and not (i > SPLIT_MAGIC): a.append(0)

    """MAGIC!!
    The first whitespaces are reduced by 1 in their size
    because the every line buffer (R) starts with ' '. (R=z trick)
    """
    a[0] -= 1

    print(a)
    return a

def validate(S):
    i = m = l = 0
    R = ''
    for c in S:
        w = ord(c) - OFFSET_MAGIC
        l += w
        R += " *"[m]*w;
        if (w < 1) | m & (l>SPLIT_MAGIC):
            l = 0; R += '\n'; i += 1
        if w : m ^= 1
    #print R

    if R.strip() != PUPU.strip():
        print(R)
        assert False, 'Invalid'
    else:
        print('Same')

PS = PUPU.split('\n')[1:-1]
S = analyze_pupu(PS[:])
#validate(S)
print(S)

# now we do not need '\n' anymore
assert not '&' in S

# write to pupu.py directly
with open('pupu.py','wb') as f:
    f.write(bytes('''\
R,z,s='  *'
for c in"{}":
 z,s=s,z;R+=s*(ord(c)-{})
 if len(R)>{}:print(R);R=z\
'''.format(S, OFFSET_MAGIC, SPLIT_MAGIC), 'utf-8'))

import subprocess, os
try:
    os.system("wc pupu.py")
    print(subprocess.check_output(['python', 'test.py']))
except subprocess.CalledProcessError:
    # just see the result
    os.system("python pupu.py")
    os.system("python test.py")
