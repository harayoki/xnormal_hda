# xNormal HDA

## About

This houdini digital asset(HDA) allows you to make normal or ao texture in SOP network using xNormal(https://xnormal.net/) and 
Python-xNormal module(https://github.com/orangeduck/Python-xNormal).
Since original xNormal software is released for Windows OS only, this HDA supports also only Windows OS. 
Although I recommend using GameDev maps baker SOP or any other something new SOP, which will be included in Game Development Toolset(https://github.com/sideeffects/GameDevelopmentToolset) for general use,
but if you prefer textures baked by xNormal software, this HDA may help you.

## Requirements

* Windows 10 or higher(the HDA only supports 64 bit OS currently).
* Installing xNormal software.
* Houdini 17.5 or higher.

## Run sample hip

Double click sample.hiplc file in sample folder to open new Houdini window. It will be ready for trying xNormal HDA.
When exporting textures, if an error like 'ImportError: No module named hda_xnormal...' happened,
run code below :

```
import hou;import os;import sys;sys.path.append((os.path.dirname(hou.hipFile.path()) + '/python2.7libs'))
```

 in Python shell.

## Preparation

* Copy hda file from dist/hda folder into the place Houdini can access(e.g. My Documents/houdini17.5/otls/).
* Copy python files (dist/python2.7libs/*.py) into the place Houdini can access(e.g. My Documents/houdini17.5/python2.7libs/).

## Usage

* In SOP network, place harayoki-xNormal HDA.
* Connect low mesh node for input 1.
* Connect high mesh node for input 2.
* Modify xNormal SOP setting. 
* At least you must apply a texture file path you want to export.
* Change temp work folder setting, if you don't like default folder.
* Hit export button(Textures are not exported automatically. I designed so since it takes several seconds). 
* Then texture(s) is(are) exported and applied as new material for confirmation.

This HDA only supports exporting normal and ao map. Other textures will be support if there is demand.
For further information about each parameters, plz refer general xNormal documents.

![property panel](https://pbs.twimg.com/media/EJqgrHXUwAcskHM?format=jpg&name=medium)
Property panel : Most of xNormal properties can be set here.

## License

This HDA is under BSD Licence likewise Python-xNormal. See LICENSE.md file for details.  

## History

* v1.0 first release

