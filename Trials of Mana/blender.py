import bpy
import re

PATH = '<YOUR PATH HERE>'

filename = ''

# Scaling
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
    if o.type != 'ARMATURE':
        o.select_set(True)
bpy.ops.transform.resize(value=(100, 100, 100))
bpy.ops.object.transform_apply(scale=True)

# Renaming
# Workaround to have the right name for the principal mesh
for mesh in bpy.data.meshes:
    if re.compile(r'SK_pc\d{2}_\d{2}.2?$').search(mesh.name):
        for material in mesh.materials:
            material.name = re.sub(r'_COLOR_0.*?$', '', material.name)
        break

for mesh in bpy.data.meshes:
    mesh.name = re.sub(r'^SK.*?Morph\d{2}_', '', mesh.name)

for o in bpy.data.objects:
    if re.compile(r'SK_pc\d{2}_\d{2}.2?\.ao').search(o.name):
        o.name = 'armature'
    o.name = re.sub(r'^SK.*?Morph\d{2}_', '', o.name)
    
    # Remove armature from Morph
    for item in o.children:
        if item.type == 'ARMATURE' and 'Armature_' in item.name :
                bpy.data.objects.remove(item)

for armature in bpy.data.armatures:
    if re.compile(r'SK_pc\d{2}_\d{2}.2?\.ad').search(armature.name):
            armature.name = armature.name[:-3]

# Join as shapes
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
    if o.name is not 'armature' and o.type != 'ARMATURE':
        o.select_set(True)
    if re.compile(r'SK_pc\d{2}_\d{2}.2?').search(o.name):
        filename = o.name
        bpy.context.view_layer.objects.active = o
bpy.ops.object.join_shapes()

for o in bpy.data.objects:
    if re.compile(r'SK_pc\d{2}_\d{2}.2?').search(o.name):
        o.parent = bpy.data.objects['armature']
        o.modifiers['Armature'].object = bpy.data.objects['armature']
        
    # Delete Morph
    elif o.name != 'armature':
        bpy.data.objects.remove(o)

# Export FBX
bpy.ops.export_scene.fbx(
    filepath='{}/{}.fbx'.format(PATH, filename),
    global_scale=0.01,
    add_leaf_bones=False,
    bake_anim=False,
    use_tspace=True
)
