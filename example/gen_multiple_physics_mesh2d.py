import numpy as np
import h5py


def match(reducer, pos, con):
    return np.argwhere((pos[con] == reducer(pos)).sum(-1) >= 2).ravel()

def make_sideset(connect1, connect2):
    ind1, inv1 = np.unique(connect1, return_inverse=True)
    ind2, inv2 = np.unique(connect2, return_inverse=True)
    _, int1, int2 = np.intersect1d(ind1, ind2, assume_unique=True, return_indices=True)
    mask1 = np.isin(inv1, int1).reshape(-1, connect1.shape[1])
    mask2 = np.isin(inv2, int2).reshape(-1, connect2.shape[1])
    ind1 = np.argwhere(mask1.any(-1)).ravel()
    ind2 = np.argwhere(mask2.any(-1)).ravel()
    mask1 = mask1[ind1]
    mask2 = mask2[ind2]
    sort1 = np.lexsort(np.sort(connect1[ind1][mask1].reshape(-1, 2)).T)
    sort2 = np.lexsort(np.sort(connect2[ind2][mask2].reshape(-1, 2)).T)

    sideset = np.stack([ind1[sort1], ind2[sort2]], axis=1).ravel()
    face_mask = np.array([1<<1 | 1<<4,
                          1<<1 | 1<<2,
                          1<<2 | 1<<3,
                          1<<3 | 1<<4])  # bit mask for each Quad corner to edges it's touching
    face_mask = np.broadcast_to(face_mask, mask1.shape)  # both mask must have the same_shape
    faces = np.stack([np.bitwise_and.reduce(face_mask[mask1].reshape(-1, 2), axis=-1),
                      np.bitwise_and.reduce(face_mask[mask2].reshape(-1, 2), axis=-1)], axis=1).ravel()
    return sideset, np.log2(faces).astype(int)


x, z = np.meshgrid(np.arange(-10, 53)*150., np.arange(-1, 11)*150.)
block = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])*75
mesh = np.stack([x.ravel(), z.ravel()], axis=1)[:, None] + block
coord, connect = np.unique(mesh.reshape(-1, 2), axis=0, return_inverse=True)
connect = connect.reshape(-1, 4)
connect_acoustic = connect[:connect.shape[0]//2]
connect_elastic = connect[connect.shape[0]//2:]

out = h5py.File("multiple_physics2d.e", 'w', track_order=True)

out.create_dataset('connect1', dtype="<i4", data=connect_acoustic+1)
out.create_dataset('connect2', dtype="<i4", data=connect_elastic+1)
out.create_dataset('coor_names', dtype="|S1", data=np.array([['x']+255*[''], ['z']+255*['']], dtype="|S1"))

out.create_dataset('coordx', dtype="<f8", data=coord[:, 0])
out.create_dataset('coordz', dtype="<f8", data=coord[:, 1])

out.create_dataset('eb_names', dtype="|S1", data=np.array([list('water'.ljust(256, '\0')),list('sediment'.ljust(256, '\0'))], dtype="|S1"))
out.create_dataset('ss_names', dtype="|S1", data=np.array([list(v.ljust(256, '\0')) for v in "xmin xmax zmin zmax water|sediment".split()], dtype="|S1"))

out.create_dataset('elem_ss1', dtype="<i4", data=(match(np.min, coord[:, 0], connect)+1).astype('<i4'))
out.create_dataset('side_ss1', dtype="<i4", data=np.full(len(out['elem_ss1']), 4, '<i4')) 
out.create_dataset('elem_ss2', dtype="<i4", data=(match(np.max, coord[:, 0], connect)+1).astype('<i4'))
out.create_dataset('side_ss2', dtype="<i4", data=np.full(len(out['elem_ss2']), 2, '<i4'))
out.create_dataset('elem_ss3', dtype="<i4", data=(match(np.min, coord[:, 1], connect)+1).astype('<i4'))
out.create_dataset('side_ss3', dtype="<i4", data=np.full(len(out['elem_ss3']), 1, '<i4'))
out.create_dataset('elem_ss4', dtype="<i4", data=(match(np.max, coord[:, 1], connect)+1).astype('<i4'))
out.create_dataset('side_ss4', dtype="<i4", data=np.full(len(out['elem_ss4']), 3, '<i4'))

elements, sides = make_sideset(connect_acoustic+1, connect_elastic+1)
out.create_dataset('elem_ss5', dtype="<i4", data=(elements+1).astype('<i4'))
out.create_dataset('side_ss5', dtype="<i4", data=sides.astype('<i4'))

out.close()

