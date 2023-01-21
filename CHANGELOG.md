# Changelog

1.7.8 - 2023-01-21

- changed: layer nav show 'plus' sign only on side of active layer

1.7.7 - 2023-01-21

- changed: layer nav greyed icon for off states
- fixed: jaggy corner on active layer highlight 


1.7.6 - 2023-01-20

- changed: layer nav keymap registered globally on grease pencil (meaning it's accessible from object mode)
- added: Customizable keymap exposed in `layer navigator` preferences

1.7.5 - 2023-01-19

- changed: layer navigator is still called when there is only one layer
- changed: Preferences panel use one tab per tool (was too long with added layer nav tool)

1.7.4 - 2023-01-17

- added: layer navigator respect ui scale
- added: layer navigator opacity slider height adjust proportionally to box height
- fixed: layer navigator opacity slider does not trigger fade anymore when dragging out of bounds.

1.7.3 - 2023-01-16

- fixed: layer navigator has sharper icons and centered with layer name, truncated if too long

1.7.2 - 2023-01-15

- changed: layer navigator has proper icons

1.7.1 - 2022-11-08

- added: initial set of preferences for layer navigator

1.7.0 - 2022-11-06

- added: layer navigator popup on `Y` shortcut

1.6.2 - 2022-10-01

- fixed: Error when no keyframes to draw (`gpu_extras.batch.batch_for_shader` does not accept empty lists in 3.4)

1.6.1 - 2022-04-28

- fixed: operator poll

1.6.0 - 2022-03-14

- added: Camera mirror flip operator

1.5.7 - 2022-03-14

- fix: Error using timeline scrub snap in blender 3+ (api change)

1.5.6 - 2022-02-14

- changed: brush bundle url to https

1.5.5 - 2022-02-13

- changed: brush pack download url to point to `blender.org`
- fix: Disable registers in background mode, avoid keymap error
- changed: follow new blender license convention

1.5.4 - 2022-01-26

- fix: keep viewpoint when reseting rotation within camera

1.5.3 - 2021-08-29

- feat: added a checkbox to disable *tiemline-scrub*
- fix: added `numpad_enter` to valid *box_deform* transform

1.5.2 - 2021-07-11

- feat: boxdeform not limited to active object in object mode. Affect all selected grease pencils objects.

1.5.1 - 2021-07-11

- feat: boxdeform keep lattice on confirm (use `shift` + confirm buttons)

1.5.0 - 2021-05-28

- feat: New rotate canvas pivot mode in camera view (enabled by default).
rotate by view center pivot instead of camera center.
- fix: Rotate canvas precision (wasn't rotating exactly from area center)
Now compatible with region overlap toggled off

1.4.3 - 2021-04-14

- fix: box deform working on grease pencil object with multiple instances

1.4.2 - 2021-03-30

- Enable Box deform with multi-lattice if blender version >= 2.93
- Fix error when trying to use snap with the OSD timeline deactivated

1.4.0 - 2021-03-19

- Match updates from official 1.4.0 bundled in blender (2.93)

1.1.6 - 2021-01-24:

- fix: correct keymap register

1.1.5 - 2020-10-25:

- fix: Error when querying url from linux (need ssl context)

1.1.4 - 2020-10-24:

- change brush pack installation to a gitlab web download

1.1.3 - 2020-10-06:

- Spellcheck: Capitalize words in displayed text


1.1.2 - 2020-10-02:

- Addon is now in blender Master official !
- added grease pencil team names
- fix: Typo in text displayed boxdeform modal
- UI: added box layout


1.1.1 - 2020-09-28:

- fix: incomplete brush install
- change : default rotate canvas is now on `ctrl+alt+MMB`

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