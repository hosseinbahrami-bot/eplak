#!/usr/bin/env python3
import re

files = [
    '/home/user/eplak/eplak-fixed/modules/dashboard.js',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/modules/dashboard.js',
    '/home/user/eplak/ios-app/Eplak/Web/modules/dashboard.js'
]

pattern = re.compile(
    r'\s*const activityWrap = document\.getElementById\(\'dashActivityWrap\'\);.*?\n    \}\n',
    re.DOTALL
)

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    c = pattern.sub('\n', c)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Cleaned dashboard.js: {fp}')
