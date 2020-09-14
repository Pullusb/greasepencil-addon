import bpy

def unzip(zip_path, extract_dir_path):
    '''Get a zip path and a directory path to extract to'''
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir_path)

def simple_dl_url(url, dest):
    import urllib
    urllib.request.urlretrieve(url, dest)

def download_url(url, dest):
    '''download passed url to dest file (include filename)'''
    import urllib
    import shutil
    import time
    start_time = time.time()
    
    with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print(f"Download time {time.time() - start_time:.2f}s",)


def get_brushes(blend_fp):
    cur_brushes = [b.name for b in bpy.data.brushes]
    with bpy.data.libraries.load(str(blend_fp), link=False) as (data_from, data_to):
        # load brushes starting with 'pp' prefix if there are not already there
        data_to.brushes = [b for b in data_from.brushes if b.startswith('pp_') and not b in cur_brushes]
    
    ## force fake user for the brushes
    for b in data_to.brushes:
        b.use_fake_user = True


def install_gp_brush_pack():
    from pathlib import Path
    import tempfile
    
    dl_url = 'https://storage.googleapis.com/5649de716dcaf85da2faee95/_%2F4e433d7a7bae4491801967ee061044f3.zip?GoogleAccessId=956532172770-27ie9eb8e4u326l89p7b113gcb04cdgd%40developer.gserviceaccount.com&Expires=1600188235&Signature=jAdME8VMKGD6WsQYIs4wY26D2aBD6SenQip1%2BEi4GnhOyF29Ydkw4ZqmIa9zB2alALlkusbdggzwSpn7L4tvk%2FMAHhLnTjDwVHyDEqJKSl6Usei1%2FxlxrfNwHDDqOl9R5o5Zbdtoqp7H6LoSn9NZXwTuTh55k17wqG7yOkLHZjH4XNLurBv01y8l6ym2vuE1tvHYbR%2BOCW%2BQnmA3ojvGUNvpWJMdZi3f9u7%2FnpC37V71lGaLCfxB9vghG7eMT%2FPKuh%2F5sLsCXcfiuN60CWum3Xz5SYp%2FmxGHYN56bSOs8c%2BNi8pxjMYW0JmilLmJAQHg123oHRBdbt6lqIjx%2BNGQlg%3D%3D'
    blendname = 'Daniel Martinez Lara (pepeland)_brush_pack_V2.blend'
    zipname = 'Daniel Martinez Lara (pepeland)_brush_pack_V2.zip'

    temp = tempfile.gettempdir()
    if not temp:
        print('no os temporary directory found to download brush pack (using python tempfile.gettempdir())')
        return
    
    temp = Path(temp)
    
    brushzip = temp / zipname
    blend_fp = Path(temp) / blendname
    
    ## use blend if exists in tempdir
    if blend_fp.exists():
        get_brushes(blend_fp)
        return

    ## unzip if zip already there and use blend
    if brushzip.exists():
        unzip(brushzip, temp)
        get_brushes(blend_fp)
        return
    
    ## download, unzip, use blend
    # download_url(dl_url, str(brushzip))
    simple_dl_url(dl_url, str(brushzip))
    unzip(brushzip, temp)
    get_brushes(blend_fp)
    return


class GP_OT_install_brush_pack(bpy.types.Operator):
    bl_idname = "gp.import_brush_pack"
    bl_label = "Import grease pencil brush pack"
    bl_description = "Download and import Grease Pencil brush pack from blender cloud"
    bl_options = {"REGISTER", "INTERNAL"}

    # @classmethod
    # def poll(cls, context):
    #     return True

    def execute(self, context):
        all_brushes = [b.name for b in bpy.data.brushes]
        brushlist = ['pp_cloud_1', 'pp_grass_1', 'pp_grass_2', 'pp_leafs_1', 'pp_leafs_2', 'pp_oil_1', 'pp_oil_2', 'pp_rough_1', 'pp_sktch_1', 'pp_sktch_2', 'pp_sktch_3', 'pp_spray_1', 'pp_spray_2', 'pp_stone_1', 'pp_wet_1']
        if all([name in all_brushes for name in brushlist]):
            self.report({'WARNING'}, 'Brushes already loaded')
            return {"CANCELLED"}

        install_gp_brush_pack()
        return {"FINISHED"}


def register():
    bpy.utils.register_class(GP_OT_install_brush_pack)

def unregister():
    bpy.utils.unregister_class(GP_OT_install_brush_pack)