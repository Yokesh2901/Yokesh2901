#!/usr/bin/env python3
"""Compatibility entry point retained from the reference project."""
import os,subprocess,sys
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
username=sys.argv[1] if len(sys.argv)>1 else "Yokesh2901"
os.environ["GH_PROFILE_USER"]=username
subprocess.run([sys.executable,os.path.join(HERE,"render_heatmap_svg.py")],cwd=ROOT,check=True)
