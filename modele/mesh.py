#!python


import csv
import numpy as np
import os
cubit.cmd('reset')

from spermaceti import *


lignes_col= np.loadtxt('lignes.csv',delimiter=',' , dtype=str)[0, :]
lignes_data= np.genfromtxt('lignes.csv',delimiter=',' )[1:, :].T
lignes_c = dict(zip(lignes_col ,lignes_data))
 
point_col= np.loadtxt('points_2.csv',delimiter=',' , dtype=str)[0,1:]
point_data = np.genfromtxt('points_2.csv', delimiter=',')[1:,1:].T
point_c = dict(zip(point_col, point_data))
lignes_c2 = {k:np.stack([v, lignes_c[k+'y']], axis=1)[:np.argmax(np.isnan(v)) if np.any(np.isnan(v)) else len(v)] for k,v in lignes_c.items() if not k.endswith('y')}
point_c.update(lignes_c2)

########♥ Dimensions tt en metre
frontal_t = 0.03  # taille du sac frontal
blubber_dessus_t = 0.15 #taille du blubber du dessus 
blubber_dessous_t = 0.1 #taille du blubber du dessus 
blubber_devant_t = 0.05 #taille du blubber devant
muscle_t = 0.08 #taille du muscle
case_t = 0.04 #taille du case

longueur = 4.7	
longueur_x =   longueur/(point_c['A6'][0] - point_c['A3'][0])  # "spermacetti tissue of sac" 

hauteur = 2.7
hauteur_y = hauteur / ((point_c['D1'][1] + blubber_dessus_t )- (point_c['B2'][1]- blubber_dessous_t)) # "Head length to jaw angle"

# Dictionnaire de vertex
vertex_dict = dict()

for k,v in point_c.items():
 if len(v) >2 :
  vertex_dict[k] = list()
  for element  in v:	
   cubit.cmd(f'create vertex { element[0] *longueur_x} {element[1]*hauteur_y} 0')
   vertex_dict[k].append(cubit.get_last_id('vertex'))
   element[0] = element[0]*longueur_x
   element[1] = element[1]*hauteur_y
 else : 
  cubit.cmd(f'create vertex {v[0] *longueur_x} {v[1]*hauteur_y} 0')
  vertex_dict[k]= cubit.get_last_id('vertex')
  v[0] = v[0]*longueur_x
  v[1] = v[1]*hauteur_y


def spermacet(x, y, y_bas, t_spermacetti, spermacetti_id = []) :
 for i in range(len(x)) :
  vertex('n', x[i], y_bas[i]+ 0.05)
  p1=cubit.get_last_id('vertex')
  vertex('n', x[i], y[i]- 0.1)
  p2=cubit.get_last_id('vertex')
  vertex('n', x[i]- t_spermacetti, y_bas[i]+ 0.05)
  p3=cubit.get_last_id('vertex')
  vertex('n', x[i]- t_spermacetti, y[i]- 0.1)
  p4=cubit.get_last_id('vertex')
  cubit.cmd('create curve vertex {} {} '.format(p1,p2))
  s1=cubit.get_last_id('curve')
  cubit.cmd('create curve vertex {} {} '.format(p2,p4))
  s2=cubit.get_last_id('curve')	
  cubit.cmd('create curve vertex {} {} '.format(p3,p4))
  s3=cubit.get_last_id('curve')	
  cubit.cmd('create curve vertex {} {} '.format(p3,p1))
  s4=cubit.get_last_id('curve')
  cubit.cmd('create surface  {} {} {} {} '.format(s1,s2,s3,s4 ) )		
  name = 'I_spermacetti_junk_'+"".join(str(i)) 
  spermacetti_id.append(cubit.get_last_id('surface'))


#case muscle points
vertex('C1',point_c['A7'][0] , point_c['A7'][1]+case_t)  
vertex('C2',point_c['A8'][0] , point_c['A8'][1]+case_t)  
vertex('C3',point_c['C2'][0] , point_c['C2'][1]+muscle_t)
vertex('C4',point_c['C1'][0], point_c['C1'][1]+muscle_t)  
vertex('C5',point_c['A9'][0] -case_t/np.sqrt(2) , point_c['A9'][1]+ case_t/np.sqrt(2) )
vertex('C6',point_c['C5'][0] -muscle_t/np.sqrt(2) , point_c['C5'][1]+muscle_t/np.sqrt(2))  	
  
  
#blubber points
vertex('E2',point_c['C3'][0] ,point_c['C3'][1]+blubber_dessus_t)  
vertex('E3',point_c['D1'][0]-blubber_devant_t/np.sqrt(2) ,point_c['D1'][1]+blubber_devant_t/np.sqrt(2))  
vertex('E4',point_c['I_B_N_1'][6,0] - blubber_devant_t,point_c['I_B_N_1'][6,1])  
vertex('E5',point_c['B2'][0],point_c['I_Sk_B'][-1,1]-blubber_dessous_t)  
vertex('E6',point_c['D3'][0] ,point_c['I_Sk_B'][3,1]-blubber_dessous_t)  
vertex('E7',point_c['D3'][0] ,point_c['C4'][1]) 
vertex('E1',point_c['D3'][0] ,point_c['E2'][1]) 

vertex('E8',point_c['C3'][0] ,point_c['C3'][1]+0.01)  # +0.01 la plus petite valeur possible ?

#frontal
vertex('F1',point_c['A7'][0], point_c['A7'][1]-0.05)  
vertex('F2',point_c['A6'][0] +frontal_t,point_c['A6'][1])  
vertex('F3',point_c['A5'][0] +frontal_t,point_c['A5'][1])
vertex('F4',point_c['A5'][0] , point_c['A5'][1]-frontal_t)  
vertex('F5',point_c['A5'][0] - frontal_t , point_c['F4'][1])
vertex('F6',point_c['F1'][0] - frontal_t , point_c['F1'][1])

# découpage du junk
vertex('J1',point_c['I_N_J'][9, 0] ,point_c['I_N_J'][9,1])  

#museau
vertex('M1',point_c['A1'][0] ,point_c['A3'][1]) 

# Muscle en dessous de la narine ?


###### Courbes 
# Points de jonction
vertex_dict['I_N_S'].append(vertex_dict['A4'])
vertex_dict['I_N_S'].insert(0,vertex_dict['A3'])
vertex_dict['I_N_J'].append(vertex_dict['B1'])
vertex_dict['I_N_J'].insert(0, vertex_dict['A4'])
vertex_dict['I_B_N_1'].append(vertex_dict['D1'])
vertex_dict['I_B_N_1'].insert(0, vertex_dict['B1'])
vertex_dict['I_B_N_2'].append(vertex_dict['A1'])
vertex_dict['I_B_N_2'].insert(0, vertex_dict['D4'])
vertex_dict['I_Sk_J'].append(vertex_dict['B3'])
vertex_dict['I_Sk_J'].insert(0, vertex_dict['B2'])
vertex_dict['I_Sk_B'].append(vertex_dict['B2'])
vertex_dict['I_Sk_B'].insert(0, vertex_dict['D3'])

curve_dict = dict()

#MUSEAU
vertex2(['A1', 'A2'], 'I_museau_muscle')
vertex2(['A2', 'A3'], 'I_museau_case')
vertex2([ 'A3', 'M1', 'A1'], 'I_museau_narine')


vertex2(['C1','C4'], 'I_skull_muscle')
vertex2(['A1', 'C6', 'C3'], 'I_tissus_muscle')
vertex2(['C1', 'C2'], 'I_case_muscle_1')
vertex2(['C3', 'C4'], 'I_muscle_blubber_1')
vertex2(['D4', 'E8'], 'I_tissus_blubber_1')
vertex2(['E8', 'C3'], 'I_tissus_blubber_2')
vertex2(['C2','C5', 'A2' ], 'I_case_muscle_2')
vertex_spline('I_B_N_2',  'I_tissus_narine')
vertex_spline('I_N_S',  'I_narine_sac') 
vertex2(['A8','A7'], 'I_case_sac_1')
vertex2(['A8', 'A9','A3' ], 'I_case_sac_2')

vertex_spline('I_Sk_J',  'I_skull_junk') 
vertex_spline('I_Sk_B',  'I_skull_blubber_bas') 
vertex2(['C1','A7'],'I_skull_case')
vertex2(['D3', 'E7'],'I_skull')
vertex2(['C4', 'E7'], 'I_skull_blubber_haut')

#######Sac frontal :
vertex2(['F1','F2', 'F3', 'F4'], 'I_frontal_skull_1')
vertex2(['F5','A5', 'A6','F6' ], 'I_frontal_sac')
vertex2(['F1', 'F6'], 'I_frontal_sac_2')
vertex2([ 'F4', 'F5'], 'I_frontal_skull_2')
vertex2(['A7','F1'], 'I_skull_sac_2')
vertex2(['F5', 'B3'], 'I_skull_sac')
vertex2(['A4', 'B3'], 'I_junk_sac')

vertex2(['B1','B2'],'I_blubber_junk')
vertex_spline('I_B_N_1',  'I_blubber_narine_1') 
vertex2(['D4', 'D1'], 'I_narine_blubber_2')
vertex_spline('I_N_J',  'I_narine_junk') 
####Blubber :
vertex2(['E6', 'D3' ], 'blubber_bas_arriere')
vertex2([ 'E3','E4' ,'E5'], 'I_eau_blubber_avant')
vertex2(['E1', 'E2'], 'I_eau_blubber_haut_milieu_1')
vertex2(['E2', 'E3'], 'I_eau_blubber_haut_milieu_2')
vertex2(['E7', 'E1'], 'blubber_haut_arriere')
vertex2(['E5', 'E6'], 'I_eau_blubber_bas')

### Surfaces
surface_dict = dict()

surface( 'narine')  
surface( 'muscle')
surface( 'case') 
surface( 'skull') 
surface( 'frontal') 
surface( 'blubber')
surface( 'sac')
surface('tissus')
surface( 'museau')
surface( 'junk')

#####Lentilles Junk 
x = np.linspace(point_c['I_N_J'][20, 0]-0.05 , point_c['J1'][0]-0.05 , 10)
y = np.interp( list(x) , list(point_c['I_N_S'][:, 0]) ,  list(point_c['I_N_S'][:, 1]) )	
y_bas = np.interp( list(x) , list(point_c['I_Sk_J'][:, 0]) ,  list(point_c['I_Sk_J'][:, 1]) )

spermacet(x, y, y_bas, 0.07) 


cubit.cmd('subtract {} from 10 keep'.format( " ".join(str(x) for x in spermacetti_id)))
surface_dict.update({'junk_last' : cubit.get_last_id('surface')})
cubit.cmd('delete surface 10')
cubit.cmd('split surface {} across location vertex {} onto curve {} '.format(surface_dict['junk_last'], vertex_dict['J1'], curve_dict['I_skull_junk']))
cubit.cmd('Unite {} With {} '.format(surface_dict['sac'], surface_dict['junk_last'] ))
surface_dict.update({'junk' : cubit.get_last_id('surface')})
surface_dict.pop('junk_last')

######## Nouvelles courbes dans le dictionnaire de courbes manuellement ! 
lst =[x for x in range(66,105)]
curve_dict.update({'I_junk_spermacetti': lst})
curve_dict.update({'I_narine_sac_2': 151})
curve_dict.update({'I_skull_sac_2': 152})
curve_dict.update({'I_sac_junk': 150})

curve_dict.update({'I_skull_junk': 153})
curve_dict.update({'I_narine_junk': 154})


## surface du cadre
cadre_t = 0.5
xmin = point_c['E4'][0]- cadre_t
xmax = point_c['E1'][0]
ymax = point_c['E1'][1] + cadre_t
ymin = point_c['E6'][1] - cadre_t
vertex('X1', xmax, ymax)
vertex('X2', xmax, ymin)
vertex('X3', xmin, ymin)
vertex('X4', xmin, ymax)
vertex2(['X1', 'X2'], 'right_bord_C')
vertex2(['X3', 'X4'], 'left_bord_C')
vertex2(['X3', 'X2'], 'bottom_bord_C')
vertex2(['X1', 'X4'], 'up_bord_C')
surface('bord_C')
cubit.cmd('subtract {} to {} from surface {} keep'.format(1, 20 , surface_dict['bord_C']) )
surface_dict.update({'bord' : cubit.get_last_id('surface')})
cubit.cmd('delete surface {} '.format(surface_dict['bord_C']))

cubit.cmd(f'surface all size 0.01')

######  Block

for k, v in surface_dict.items() :
 cubit.cmd(f'block {v} surface {v}')
 cubit.cmd(f'block {v} element type QUAD4')
 cubit.cmd('block {} name "{}"'.format(v, k))
	
cubit.cmd(f'block 10 surface 11 to 20')
cubit.cmd(f'block 10 element type QUAD4')
cubit.cmd('block 10 name "spermacetti"')

cubit.cmd('block 11 surface {} '.format(surface_dict['bord']) )
cubit.cmd(f'block 11 element type QUAD4')
cubit.cmd('block 11 name "bord" ')

## Sideset
cubit.cmd('imprint all')
cubit.cmd('merge all')

list_curve_xmax = [164, 160, curve_dict['I_skull'], curve_dict['blubber_haut_arriere'] , curve_dict['blubber_bas_arriere'] ]
cubit.cmd('sideset 1 curve '+" ".join(str(x) for x in list_curve_xmax))
cubit.cmd(f'sideset 1 name "xmax" ')


cubit.cmd('sideset 2 curve 162 ')
cubit.cmd(f'sideset 2 name "xmin"')

cubit.cmd('sideset 3 curve 161')
cubit.cmd(f'sideset 3 name "ymin"')

cubit.cmd('sideset 4 curve  163')
cubit.cmd(f'sideset 4 name "ymax"')


s = 4
for k,v in curve_dict.items() : 
 s+=1
 cubit.cmd(f'sideset {s} curve {v}' )
 cubit.cmd(f'sideset {s} name "{k}"')
 print(f'sideset {s} name "{k}"')

cubit.cmd('mesh surface {}'.format(surface_dict['narine'])  )
cubit.cmd('mesh surface {}'.format(surface_dict['blubber'])  )


cubit.cmd('mesh surface all')
cubit.cmd('Set Exodus NetCDF4 On')
cubit.cmd('export mesh "cachalot_v4.e" dimension 2 overwrite')

