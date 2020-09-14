import bpy

def get_addon_prefs():
    import os
    addon_name = os.path.splitext(__name__)[0]
    addon_prefs = bpy.context.preferences.addons[addon_name].preferences
    return (addon_prefs)