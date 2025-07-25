#!python

import csv
import numpy as np
import os
cubit.cmd('reset')

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
blubber_dessous_t = 0.25 #taille du blubber du dessous
blubber_devant_t = 0.05 #taille du blubber devant
muscle_t = 0.08 #taille du muscle
case_t = 0.07 #taille du case
cadre_t = 4  # "taille" de la mer
rotation = 5

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

def vertex(name, x, y):
 cubit.cmd('create vertex {} {} 0'.format(x, y) )
 vertex_dict.update({name: cubit.get_last_id('vertex')})
 point_c.update({name : [x , y]})
 return name

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
vertex('E5',point_c['B2'][0]-blubber_devant_t,point_c['I_Sk_B'][-1,1]-blubber_dessous_t)  
vertex('E6',point_c['D3'][0] ,point_c['I_Sk_B'][3,1]-blubber_dessous_t)  
vertex('E7',point_c['D3'][0] ,point_c['C4'][1]) 
vertex('E1',point_c['D3'][0] ,point_c['E2'][1]) 
vertex('E45',point_c['B1'][0] - blubber_devant_t ,point_c['B1'][1]) 
vertex('E41',point_c['I_B_N_1'][2,0] - blubber_devant_t ,point_c['I_B_N_1'][2,1]) 


vertex('E8',point_c['C3'][0] ,point_c['C3'][1]+0.01)  # +0.01 la plus petite valeur possible ?

#frontal
vertex('F1',point_c['A7'][0], point_c['A7'][1]-0.05)  
vertex('F2',point_c['A6'][0] +frontal_t,point_c['A6'][1])  
vertex('F3',point_c['A5'][0] +frontal_t, point_c['A5'][1])
vertex('F4',point_c['A5'][0] , point_c['B3'][1])  
vertex('F5',point_c['A5'][0] - frontal_t , point_c['F4'][1])
vertex('F6',point_c['F1'][0] - frontal_t , point_c['F1'][1])

# découpage du junk
vertex('J1',point_c['I_N_J'][9, 0] ,point_c['I_N_J'][9,1])  

#museau
vertex('M1',point_c['A1'][0] ,point_c['A3'][1]) 

# MUSCLE-MUseau
vertex('M2',point_c['I_B_N_2'][-1,0] ,point_c['I_B_N_2'][-1,1]) 
vertex('M3',point_c['A2'][0] ,point_c['M2'][1]) 
vertex('M4',point_c['A3'][0] ,point_c['A3'][1]+0.02) 

# Skull nouveau point
vertex('S1',point_c['B2'][0] - 0.02,point_c['B2'][1]) 

# NARINE ROND
vertex('N1',point_c['A4'][0] + 0.01,point_c['A4'][1]-0.025) 
vertex('N2',point_c['I_N_J'][0,0],point_c['I_N_J'][0,1]) 

###### Courbes 
# Points de jonction
vertex_dict['I_N_S'].append(vertex_dict['A4'])
vertex_dict['I_N_S'].insert(0,vertex_dict['A3'])
vertex_dict['I_N_J'].append(vertex_dict['B1'])
vertex_dict['I_N_J'].insert(0, vertex_dict['A4'])
vertex_dict['I_B_N_1'].append(vertex_dict['D1'])
vertex_dict['I_B_N_1'].insert(0, vertex_dict['B1'])
#vertex_dict['I_B_N_2'].append(vertex_dict['A1'])
vertex_dict['I_B_N_2'].insert(0, vertex_dict['D4'])
vertex_dict['I_Sk_J'].append(vertex_dict['B3'])
vertex_dict['I_Sk_J'].insert(0, vertex_dict['B2'])
vertex_dict['I_Sk_B'].append(vertex_dict['B2'])
vertex_dict['I_Sk_B'].insert(0, vertex_dict['D3'])

###### squelette rond 


lst1 = [vertex_dict['A5'], vertex_dict['A6'], vertex_dict['A7'] , vertex_dict['C1'], vertex_dict['C4'], vertex_dict['E7'], vertex_dict['F1'], vertex_dict['F2'], vertex_dict['F3'], vertex_dict['F5'], vertex_dict['F4'], vertex_dict['F6']]
lst2 = [ x for x in vertex_dict['I_Sk_J'] ]
for i, e in enumerate(vertex_dict['I_Sk_B']) :
 lst2.append(e)
lst2.append(vertex_dict['E5'])
lst2.append(vertex_dict['S1'])

######" Rotation 

cubit.cmd('Group "squelettehaut" equals vertex {}'+" ".join(str(x) for x in lst1 ))
cubit.cmd('Group "squelettebas" equals vertex {}'+" ".join(str(x) for x in lst2 ))

cubit.cmd('rotate group 2 about origin {} {} direction 0 0 1 angle {}'.format(point_c['E6'][0], point_c['E6'][1] , rotation ))
cubit.cmd('rotate group 3 about origin {} {} direction 0 0 1 angle {}'.format(point_c['E6'][0], point_c['E6'][1], rotation/3 ))

curve_dict = dict()

def vertex_spline(name_vertex, name_curve): 
 cubit.cmd('create curve spline vertex '+" ".join(str(x) for x in vertex_dict[name_vertex] ))
 curve_dict.update({name_curve : cubit.get_last_id('curve')})
 return name_curve

def curve(name_vertex, name_curve): 
 cubit.cmd('create curve spline vertex '+" ".join(str(vertex_dict[x]) for  x in name_vertex ))
 curve_dict.update({name_curve : cubit.get_last_id('curve')})
 return name_curve


#MUSEAU
curve(['M4', 'A3'], 'museau|sac')
curve(['A1', 'A2'], 'museau|muscle')
curve(['A2', 'M4'], 'museau|case')
curve([ 'A3', 'M1', 'A1'], 'museau|narine')

curve(['A1','M2'], 'narine|muscle')
curve(['M2','M3'], 'tissus|muscle_2')
curve(['C1','C4'], 'muscle|skull')
curve(['M3', 'C6', 'C3'], 'tissus|muscle_1')
curve(['C1', 'C2'], 'case|muscle_1')
curve(['C3', 'C4'], 'blubber|muscle')
curve(['D4', 'E8'], 'tissus|blubber_1')
curve(['E8', 'C3'], 'tissus|blubber_2')
curve(['C2','C5', 'A2' ], 'case|muscle_2')
vertex_spline('I_B_N_2',  'tissus|narine')

vertex_spline('I_Sk_B',  'blubber|skull_1') 
curve(['C1','A7'],'case|skull')
curve(['D3', 'E7'],'eau|skull')
curve(['C4', 'E7'], 'blubber|skull_2')

#######Sac frontal :
curve(['F1','F2', 'F3', 'F4'], 'frontal|skull_1')
curve([ 'F4', 'F5'], 'frontal|skull_2')
vertex_spline('I_B_N_1',  'narine|blubber_1') 
curve(['D4', 'D1'], 'I_narine|blubber_2')
curve(['E6', 'D3' ], 'eau|blubber_6')
curve(['E1', 'E2'], 'eau|blubber_1')
curve(['E2', 'E3'], 'eau|blubber_2')
curve(['E7', 'E1'], 'eau|blubber_5')
curve(['E5', 'E6'], 'eau|blubber_3')
curve(['E45', 'E5'], 'eau|blubber_4')
curve([ 'E3','E4' ,'E41','E45'], 'eau|blubber_7')

##### oil junk+sac
curve(['A7','F1'], 'sac|skull_2')
curve(['F5', 'B3'], 'sac|skull_1')
vertex_spline('I_Sk_J',  'junk|skull') 
vertex_spline('I_N_J',  'narine|junk') 
vertex_spline('I_N_S',  'narine|sac_1') 
#curve( ['N2', 'N1', 'A4'], 'narine|junk_2') 
curve(['A8','A7'], 'sac|case_1')
curve(['A8', 'A9','M4' ], 'sac|case_2')
curve(['F5','A5', 'A6','F6' ], 'frontal|sac_1')
curve(['F1', 'F6'], 'frontal|sac_2')
curve(['B1','S1'],'junk|blubber_1')
curve(['S1','B2'],'junk|blubber_2')

curve(['A4','B3'],'sac|junk')


### Surfaces
surface_dict = dict()
def surface( name_surface): 	
 id_curve = [v for k,v in curve_dict.items() if name_surface in k ] 
 print(id_curve)
 cubit.cmd('create surface curve '+" ".join(str(x) for x in id_curve ) )
 surface_dict.update({name_surface : cubit.get_last_id('surface')})
 return

surface( 'narine')  
surface( 'muscle')
surface( 'case') 
surface( 'skull') 

surface( 'frontal') 
surface( 'blubber')
surface( 'sac')
surface( 'junk')
surface('tissus')
surface( 'museau')


x = np.linspace(point_c['I_N_J'][20, 0]-0.05 , point_c['J1'][0]-0.05 , 10)
y = np.interp( list(x) , list(point_c['I_N_S'][:, 0]) ,  list(point_c['I_N_S'][:, 1]) )	
y_bas = np.interp( list(x) , list(point_c['I_Sk_J'][:, 0]) ,  list(point_c['I_Sk_J'][:, 1]) )
t_spermacetti =0.15
spermacetti_id = []

for i in range(10) :
 vertex('n', x[i], y_bas[i]+ 0.01)
 p1=cubit.get_last_id('vertex')
 vertex('n', x[i], y[i]- 0.1)
 p2=cubit.get_last_id('vertex')
 vertex('n', x[i]- t_spermacetti, y_bas[i]+ 0.01)
 p3=cubit.get_last_id('vertex')
 vertex('n', x[i]- t_spermacetti, y[i]- 0.1)
 p4=cubit.get_last_id('vertex')
 cubit.cmd('create curve vertex {} {} '.format(p1,p2))
 s1=cubit.get_last_id('curve')
 curve_dict.update( {       'spermaceti1_'+"".join(str(i)  )  : s1 })
 cubit.cmd('create curve vertex {} {} '.format(p2,p4))
 s2=cubit.get_last_id('curve')	
 curve_dict.update({ 'spermaceti2_'+"".join(str(i))    :  s2})
 cubit.cmd('create curve vertex {} {} '.format(p3,p4))
 s3=cubit.get_last_id('curve')
 curve_dict.update({ 'spermaceti3_'+"".join(str(i)):s3})	
 cubit.cmd('create curve vertex {} {} '.format(p3,p1))
 s4=cubit.get_last_id('curve')
 curve_dict.update({ 'spermaceti4_'+"".join(str(i) ) : s4})
 cubit.cmd('create surface  {} {} {} {} '.format(s1,s2,s3,s4 ) )
 spermacetti_id.append(cubit.get_last_id('surface'))

cubit.cmd('unite '+" ".join(str(x) for x in spermacetti_id) )

surface_dict.update({'spermaceti' : cubit.get_last_id('Body') })
cubit.cmd('subtract {} from 8 keep'.format( surface_dict['spermaceti']) )
surface_dict.update({'junk_last' : cubit.get_last_id('surface')})

cubit.cmd('delete surface 8')
cubit.cmd('split surface {} across location vertex {} onto curve {} '.format(surface_dict['junk_last'], vertex_dict['J1'], curve_dict['junk|skull']))
cubit.cmd('Unite {} With {} '.format(surface_dict['sac'], surface_dict['junk_last'] ))
surface_dict.update({'junk' : cubit.get_last_id('surface')})
surface_dict.pop('junk_last')
cubit.cmd('separate surface 22  body 7')
surface_dict.update({'junk': cubit.get_last_id('Body')})

######## Nouvelles courbes dans le dictionnaire de courbes manuellement ! 

curve_dict.update({'narine|sac_3': 164})
curve_dict.update({'sac|skull_3': 163})
curve_dict.update({'sac|junk': 160})

curve_dict.update({'narine|junk': 151})
curve_dict.update({'junk|skull': 162})
curve_dict.update({'narine|junk': 161})

## surface du cadre
xmin = point_c['E4'][0]- cadre_t
xmax = point_c['E1'][0] + 0.4
ymax = point_c['E1'][1] + cadre_t/2
ymin = point_c['E6'][1] - cadre_t/2
vertex('X1', xmax, ymax)
vertex('X2', xmax, ymin)
vertex('X3', xmin, ymin)
vertex('X4', xmin, ymax)
curve(['X1', 'X2'], 'right_bord_C')
curve(['X3', 'X4'], 'left_bord_C')
curve(['X3', 'X2'], 'bottom_bord_C')
curve(['X1', 'X4'], 'up_bord_C')
surface('bord_C')
cubit.cmd('subtract {} to {} from surface {} keep'.format(1, 22, surface_dict['bord_C']) )
cubit.cmd('delete surface {} '.format(surface_dict['bord_C']))
surface_dict.pop('bord_C')
surface_dict.update({'eau' : 24})

cubit.cmd(f'surface 25 size 0.1')
cubit.cmd(f'surface all size 0.01')

######  Block

for k, v in surface_dict.items() :
 cubit.cmd(f'block {v} surface in body {v}')
 cubit.cmd(f'block {v} element type QUAD4')
 cubit.cmd('block {} name "{}" '.format(v,k) )
 
#sideset

cubit.cmd('imprint all')
cubit.cmd('merge all')

#cubit.cmd('list curve in body 24') 
cubit.cmd('sideset 1 curve 179' )
cubit.cmd(f'sideset 1 name "xmax"')

cubit.cmd('sideset 2 curve 181' )
cubit.cmd(f'sideset 2 name "xmin"')

cubit.cmd('sideset 3 curve 180')
cubit.cmd(f'sideset 3 name "ymin"')

cubit.cmd('sideset 4 curve 178' )
cubit.cmd(f'sideset 4 name "ymax"')


def side(name, nb, el1, el2) :
 cubit.cmd('sideset {} curve {}'.format(nb , " ".join(str(v) for k,v in curve_dict.items() if el1 in k and el2 in k) ) )
 cubit.cmd('sideset {} name "{}" '.format(nb, name ))

side("eau|blubber", 5 , "eau", "blubber")
side("sac|case", 6 , "case", "sac")
side("tissus|blubber", 7 , "tissus", "blubber")
side("narine|blubber", 8 , "narine", "blubber")
side("frontal|sac", 9 , "frontal", "sac")
side("tissus|muscle", 10 , "tissus", "muscle")
side("case|muscle", 11 , "case", "muscle")
side("narine|junk", 12 , "narine", "junk")
side("sac|skull", 13 , "sac","skull")
side("junk|blubber", 14 , "blubber", "junk")
side("blubber|skull", 15 , "blubber", "skull")
side("frontal|skull", 16 , "frontal", "skull")
side("spermaceti|junk", 17 , "spermaceti", "junk")
side("narine|sac", 18 , "narine", "sac")
cubit.cmd('sideset 19 curve in body 11')
cubit.cmd('sideset 19 name "spermaceti|sac"')

s = 19
n=0
for k,v in curve_dict.items() : 
 if not list(k)[-1].isdigit() :
  s+=1
  cubit.cmd(f'sideset {s} curve {v}' )
  cubit.cmd(f'sideset {s} name "{k}"')
  print(f'sideset {s} name "{k}"')

#### Mesh
cubit.cmd('mesh surface {}'.format(surface_dict['muscle']))
cubit.cmd('mesh surface {}'.format(surface_dict['case']))
cubit.cmd('mesh surface {}'.format(surface_dict['narine']))
cubit.cmd('mesh surface {}'.format(surface_dict['skull']))
cubit.cmd('mesh surface {}'.format(surface_dict['blubber']))
cubit.cmd('mesh surface {}'.format(surface_dict['museau']))
cubit.cmd('mesh surface {}'.format(surface_dict['junk']))
cubit.cmd('mesh surface {}'.format(surface_dict['sac']))
cubit.cmd('mesh surface {}'.format(surface_dict['tissus']))
cubit.cmd('mesh surface {}'.format(surface_dict['frontal']))
cubit.cmd('mesh surface in body {}'.format(surface_dict['spermaceti']))
cubit.cmd('mesh surface in body {}'.format(surface_dict['eau']))

cubit.cmd('Set Exodus NetCDF4 On')
cubit.cmd('export mesh "mesh.e" dimension 2 overwrite')




