# Blender Pipeline Tools

[![Blender](https://img.shields.io/badge/Blender-%23F5792A.svg?logo=blender&logoColor=white)](https://www.blender.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-%233776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/github/license/ddlite92/BlenderPipelineTools)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/ddlite92/BlenderPipelineTools)](https://github.com/ddlite92/BlenderPipelineTools/commits/main)

A collection of Python scripts and utilities to streamline Blender workflows for lighting development and render pipelines.


## ✨ Features

- **Automated Asset Processing :**  Batch convert/optimize models and textures (WIP)
- **Scene Management :** Cleanup and standardization tools (WIP)
- **Version Control Integration :** Git-friendly asset handling
- **Filepath Automation :** Filepath on compisiting fill up based on the project folder

## 📦 Installation 

### As for now, this tool are NOT made to be installed. This is just a pipeline development project still in the local phase 


## 🎯 Key Functions

| Command               | Description |
|-----------------------|-------------|
| `autosavePR()`        | Automatically exports pre-render assets during test renders (F12) |
| `build()`             | Constructs light setup from benchmark configuration file |
| `purge()`             | Cleans project file by removing all unused/non-referenced data |
| `set_renderpath()`    | Automatically sets consistent output paths for all compositing nodes |

## 🗂️ Project Structure

- **/custom/** - Custom Blender Python scripts
- **/functions/** - Core Python functions and utilities
- **/operator/** - Blender operators for export/configurations  
- **/panel/** - UI panels for the add-on interface
- **/tests/** - Unit and integration tests
- **/utils/** - Helper utilities and shared tools

## 📜 License
  Distributed under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007. See LICENSE for more information.

## 📬 Contact
  GitHub: @ddlite92
