bl_info = {
    "name": "Monsta",
    "description": "Monsta Addon",
    "author": "Monsta",
    "version": (1, 0),
    "blender": (3, 3, 3),
    "warning": "This addon is still in development",
    "tracker_url": "https://github.com/ddlite92/BlenderPipelineTools",
    "category": "Render",
}

import bpy
import os
import sys
import ast
import addon_utils
import subprocess

from .functions import *
from .operators import *
from .panel import monsta_panel

from bpy.types import PropertyGroup, Scene, Panel, Operator, Space
from math import ceil
from os import path, listdir
from bpy.app.handlers import persistent
from bpy.utils import previews, register_class, unregister_class
from pathlib import Path


classes = (
        MonstaPanel,
        PurgeSceneOperator,
        CleanOperator,
        LinkAnimFile,
        OutputPath,
        SetCamera,
        )

# register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()