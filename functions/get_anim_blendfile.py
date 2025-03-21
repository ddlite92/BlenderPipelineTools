import bpy
import os
import sys
import ast
import addon_utils
import subprocess
from bpy.types import PropertyGroup, Scene, Panel, Operator, Space
from math import ceil
from os import path, listdir
from bpy.app.handlers import persistent
from bpy.utils import previews, register_class, unregister_class
from pathlib import Path


# Finds the animation blend file based on the current file's location.
# Code edited to read windows path and return as raw string

context = bpy.context
bpath = bpy.path
filepath = bpy.data.filepath

def get_anim_blendfile():
  current_path = bpy.data.filepath
  anim_file_dir = os.path.dirname(current_path)
  for file in os.listdir(anim_file_dir):
    if file.endswith("_ANIM.blend"):
      anim_file = os.path.join(anim_file_dir, r"./" + file)  # Use raw string for Windows path
      return anim_file
