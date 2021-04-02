import os
import pathlib
import re
import shutil

if __name__ == '__main__':
    path = pathlib.Path(__file__).parent.absolute().parent

    header = '''---
title: Software User Guide
  
columns: 1

search: true
---    
'''
    img_dest_path = path / 'web_docs' / 'images'
    if os.path.exists(img_dest_path):
        shutil.rmtree(img_dest_path)
    shutil.copytree(path / 'assets' / 'images', img_dest_path)

    with open(path / 'README.md', 'r') as f, open(path / 'web_docs' / 'index.md', 'w') as out:
        contents = f.read()
        contents = header + contents

        contents = re.sub('\(\./assets/images/(.*)\.(png|jpg|jpeg)\)', '(./images/\\1.\\2)', contents)
        contents = re.sub(
            '\./(.*)/README.md',
            'https://github.com/nsat/space-services-user-guide/tree/main/\\1/README.md',
            contents
        )

        # unindent headings
        contents = re.sub('\n([#]{2})', '\n#', contents)

        # remove redundant spire logo

        contents = re.sub('\n!\[Spire Space Services\]\(\./images/spire\.png\)', '', contents)

        out.write(contents)
