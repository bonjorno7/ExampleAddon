import bpy
import bmesh


def wireframe(obj, evaluated):
    '''
    Get coords of verts for edges of an object.

    Args:
        obj: An object that can be converted to mesh.
        evaluated: Whether to apply modifiers.

    Returns:
        points: A list of coordinates.
    '''

    points = []

    if evaluated:
        deps = bpy.context.view_layer.depsgraph
        obj = obj.evaluated_get(deps)

    mesh = obj.to_mesh()
    bm = bmesh.new()

    bm.from_mesh(mesh)
    bm.transform(obj.matrix_world)

    for edge in bm.edges:
        for vert in edge.verts:
            points.append(vert.co.xyz)

    bm.free()
    obj.to_mesh_clear()

    return points
