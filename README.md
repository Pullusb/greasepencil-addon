# Grease pencil tools

Blender addon - Pack of tools for grease pencil drawing.

## [Download latest](https://github.com/Pullusb/greasepencil-addon/archive/master.zip)

<!-- Want to support me? [Check this page](http://www.samuelbernou.fr/donate) -->

---  

Add option in Tab Grease Pencil

## Box deform on `Ctrl+T`

Exemple with lattice subdiv and spline deformations.

![box demo](https://github.com/Pullusb/images_repo/raw/master/box_deform_demo.gif)

### [Box deform youtube demo](https://youtu.be/gY9Ni5r6bc8)

**How to use**: (same tutorial in addon preferences)  
Use the shortcut `Ctrl + T` in available modes  
The lattice box is generated facing your view so be sure to face canvas to avoid unintentional anamorphosis offset  
Then use following shortcuts (also displayed in topbar):  

**Modes and deformation target**:

- Object mode : The whole GP object is deformed
- GPencil Edit mode : Deform Selected points
- Gpencil Paint : Deform last Strokes
<!-- - Lattice edit : Revive the modal after a ctrl+Z (special case) -->

**Shortcuts** (also displayed in topbar):

- `Spacebar` / `Enter` : **Confirm**  
- `Delete` / `Backspace` / `ctrl+T` / `Tab`(twice) : **Cancel**  
- `M` : **Toggle Linear and Spline** mode at any moment  
- `1-9 top row number` : Shortcut to **subdivide box**  
- `Ctrl + arrows-keys` : **Subdivide** the box incrementally in **individual X/Y axis**  

Notes :

If you return in box deform after applying with a ctrl+Z, you need to hit ctrl+T again to revive the modal.

A cancel warning will be displayed the first time you hit Tab (to avoid mis-canceling)

Multiframe edit selection works but you will only see the current frame during the modal


## Rotate canvas

![demo canvas rotate gif](https://raw.githubusercontent.com/Pullusb/images_repo/master/RC_rotate_canvas_demo_view_and_cam.gif)

Customise shortcut in addons preferences, Default `ctrl + alt + right-Click`.  
Shortcut changed are refreshed upon modifications.

![preferences canvas rotate gif](https://raw.githubusercontent.com/Pullusb/images_repo/master/RC_rotate_canvas_pref_shortcut.png)

**Use Hud**: Show angle value and lines.

**Reset view** (free navigation only): Click and release immediately without rotation to reset (up view point to world Z).


## Straight stroke

Straighten the stroke between first ans last point, keeping the points proportionally.  
You can affect influence in the redo panel.  
Influence amount is remembered for next use (You can shift+click on the button to reset to 100% influence)


## Import textured brush pack

Download and append online [Grease pencil textured brush pack]((https://cloud.blender.org/p/gallery/5f235cc297f8815e74ffb90b)) made by [pepeland (Daniel Martinez Lara)](https://www.pepe-school-land.com/pepeland)  
This is available in the sidebar > Tool > Brushes panel int the brush dropdown menu (where you can reset brush)  
/!\ this will be removed once blender official asset manager will be active

---

## Changelog

1.1.0 - 2020-09-27:

- brush pack included in addon
- change tab UI name (category) in sidebar in addon prefs. 

1.0.3 - 2020-09-20:

- fix: redownload brush pack when using operator to get update (but dl url is in a container and change at every upload)...

1.0.2 - 2020-09-15:

- Integrated [rotate canvas](https://github.com/Pullusb/rotate_canvas)
- fix: some brush pack import ops bug
- fix: brush pack download failing on linux (needed specific method of `urllib` import and `ssl` certificate)
- code: slight refactor for get_addonpref function (placed and loaded from `prefs.py` file)

0.1.1 - 2020-09-14:

- added operator to download and append [pepeland (Daniel Martinez Lara) public brushpack](https://cloud.blender.org/p/gallery/5f235cc297f8815e74ffb90b)

0.0.5 - 2020-07-04:

- fix: Bug throwing error when trying modal revival after ctrl+Z back to lattice.
- refactor: Cleaner use of `is_running` variable, attached to WM variable instead of prefs (Thanks to [Antonio Vasquez](https://twitter.com/antonioya_blend?lang=en))

0.0.4 - 2020-07-04:

- fix: added a property in pref to detect if modal is already running so pressing the UI button again will not crash.

0.0.3 - 2020-07-04:

- syntax: correction on HUD text, Preferences, Title cased all words in buttons to fit blenders UI.

0.0.2 - 2020-06-23:

- box deform:

  - fix: paint mode deforming strokes on another layer
  - fix: force view overlay during modal to avoid losing sight of lattice
  - feature: autoswap mode between Linear and Bspline
  - UI: preference checkbox to disable new autoswap feature
  - code: refactor, deleted useless property group

0.0.1 - 2020-06-21:

- Initial version from standalone Box_deform 0.2.4
- sligth code refactor
- Deleted/changed funny info messages in box deform (when pressing 'H' or trying to ctrl+T on object having already a Lattice)
- Deleted some useless comments
- CamelCased the classes
- Changed id_names to avoid collisions
- added licence in each files
- Changed straight_stroke from GP_refine_stroke to work according to context ('PAINT' / 'EDIT')
- added `box deform` to VIEW3D_MT_transform_object menu (with condition to appear only if context object exists and is GP)
- added `box deform` to VIEW3D_MT_edit_gpencil_transform menu
- added `straight stroke` to VIEW3D_MT_edit_gpencil_stroke menu