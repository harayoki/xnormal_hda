# -*- coding: utf-8 -*-

from pathlib import Path
import shutil
import os

cur_dir = Path(os.path.dirname(__file__)).absolute()
src_dir = cur_dir / Path('src')
dist_dir = cur_dir.parent / Path('dist')
sample_dir = cur_dir.parent / Path('sample')

# copy python files
src_path = src_dir / Path('python2.7libs')
dist_path = dist_dir / Path('python2.7libs')
if dist_path.exists():
    shutil.rmtree(dist_path)
sample_path = sample_dir / Path('python2.7libs')
if sample_path.exists():
    shutil.rmtree(sample_path)
shutil.copytree(src_path, sample_path)

# copy HDA files
src_path = src_dir / Path('hda')
dist_path = dist_dir / Path('hda')
if dist_path.exists():
    shutil.rmtree(dist_path)
shutil.copytree(src_path, dist_path)
sample_path = sample_dir / Path('hda')
if sample_path.exists():
    shutil.rmtree(sample_path)
shutil.copytree(src_path, sample_path)


# copy hip(hiplc) file
src_path = src_dir / Path('sample.hiplc')
if src_path.exists():
    sample_path = sample_dir / Path('sample.hiplc')
    if sample_path.exists():
        os.remove(sample_path)
    shutil.copy(src_path, sample_path)
