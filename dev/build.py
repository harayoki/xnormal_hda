# -*- coding: utf-8 -*-

from pathlib import Path
import shutil
import os

cur_dir = Path(os.path.dirname(__file__)).absolute()
src_dir = cur_dir / Path('src')
dist_dir = cur_dir.parent / Path('dist')

# copy python files
src_path = src_dir / Path('python2.7libs')
dist_path = dist_dir / Path('python2.7libs')
if dist_path.exists():
    shutil.rmtree(dist_path)
shutil.copytree(src_path, dist_path)

# copy HDA files
src_path = src_dir / Path('hda')
dist_path = dist_dir / Path('hda')
if dist_path.exists():
    shutil.rmtree(dist_path)
shutil.copytree(src_path, dist_path)
