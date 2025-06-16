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
vertex('E5',point_c['B2'][0]+blubber_devant_t,point_c['I_Sk_B'][-1,1]-blubber_dessous_t)  
vertex('E6',point_c['D3'][0] ,point_c['I_Sk_B'][3,1]-blubber_dessous_t)  
vertex('E7',point_c['D3'][0] ,point_c['C4'][1]) 
vertex('E1',point_c['D3'][0] ,point_c['E2'][1]) 
vertex('E45',point_c['B1'][0] - blubber_devant_t ,point_c['B1'][1]) 


vertex('E8',point_c['C3'][0] ,point_c['C3'][1]+0.01)  # +0.01 la plus petite valeur possible ?

#frontal
vertex('F1',point_c['A7'][0], point_c['A7'][1]-0.05)  
vertex('F2',point_c['A6'][0] +frontal_t,point_c['A6'][1])  
vertex('F3',point_c['A5'][0] +frontal_t,point_c['A5'][1])
vertex('F4',point_c['A5'][0] , point_c['A5'][1]-frontal_t - 0.02)  
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
lst2 = [ x for x in vertex_dict['I_Sk_J']]
for i, e in enumerate(vertex_dict['I_Sk_B']) :
 lst2.append(e)
lst2.append(vertex_dict['E5'])

######" Rotation 

cubit.cmd('Group "squelettehaut" equals vertex {}'+" ".join(str(x) for x in lst1 ))
cubit.cmd('Group "squelettebas" equals vertex {}'+" ".join(str(x) for x in lst2 ))

cubit.cmd(f'rotate group 2 about origin 5.8 0.8  direction 0 0 1 angle 5')
cubit.cmd(f'rotate group 3 about origin 5.8 0.8  direction 0 0 1 angle 0')

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

curve(['A1','M2'], 'muscle|narine')
curve(['M2','M3'], 'tissus|muscle_2')
curve(['C1','C4'], 'muscle|skull')
curve(['M3', 'C6', 'C3'], 'tissus|muscle_1')
curve(['C1', 'C2'], 'case|muscle_1')
curve(['C3', 'C4'], 'muscle|blubber')
curve(['D4', 'E8'], 'tissus|blubber_1')
curve(['E8', 'C3'], 'tissus|blubber_2')
curve(['C2','C5', 'A2' ], 'case|muscle_2')
vertex_spline('I_B_N_2',  'tissus|narine')
vertex_spline('I_N_S',  'narine|sac_1') 
curve(['A8','A7'], 'case|sac_1')
curve(['A8', 'A9','M4' ], 'case|sac_2')

vertex_spline('I_Sk_J',  'junk|skull') 
vertex_spline('I_Sk_B',  'blubber|skull_1') 
curve(['C1','A7'],'case|skull')
curve(['D3', 'E7'],'skull')
curve(['C4', 'E7'], 'blubber|skull_2')

#######Sac frontal :
curve(['F1','F2', 'F3', 'F4'], 'frontal|skull_1')
curve(['F5','A5', 'A6','F6' ], 'frontal|sac_1')
curve(['F1', 'F6'], 'frontal|sac_2')
curve([ 'F4', 'F5'], 'frontal|skull_2')
curve(['A7','F1'], 'sac|skull_3')
curve(['F5', 'B3'], 'sac|skull_1')
curve(['A4', 'B3'], 'junk|sac')

curve(['B1','S1'],'blubber|junk_1')
curve(['S1','B2'],'blubber|junk_2')

vertex_spline('I_B_N_1',  'narine|blubber_1') 
curve(['D4', 'D1'], 'I_narine|blubber_2')
vertex_spline('I_N_J',  'narine|junk_1') 
####Blubber :
curve(['E6', 'D3' ], 'blubber_bas_arriere')
curve([ 'E3','E4' ,'E45', 'E5'], 'eau|blubber_4')
curve(['E1', 'E2'], 'eau|blubber_1')
curve(['E2', 'E3'], 'eau|blubber_2')
curve(['E7', 'E1'], 'blubber_haut_arriere')
curve(['E5', 'E6'], 'eau|blubber_3')


### Surfaces
surface_dict = dict()
def surface( name_surface): 	
 id_curve = [v for k,v in curve_dict.items() if name_surface in k ] 
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
surface('tissus')
surface( 'museau')
surface( 'junk')


#####Lentilles Junk 
x = np.linspace(point_c['I_N_J'][20, 0]-0.05 , point_c['J1'][0]-0.05 , 10)
y = np.interp( list(x) , list(point_c['I_N_S'][:, 0]) ,  list(point_c['I_N_S'][:, 1]) )	
y_bas = np.interp( list(x) , list(point_c['I_Sk_J'][:, 0]) ,  list(point_c['I_Sk_J'][:, 1]) )
spermacetti_id = []

def spermacet(x, y, y_bas, t_spermacetti) :
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
  curve_dict.update( {       'junk|spermaceti1_'+"".join(str(i)  )  : s1 })
  cubit.cmd('create curve vertex {} {} '.format(p2,p4))
  s2=cubit.get_last_id('curve')	
  curve_dict.update({ 'junk|spermaceti2_'+"".join(str(i))    :  s2})
  cubit.cmd('create curve vertex {} {} '.format(p3,p4))
  s3=cubit.get_last_id('curve')
  curve_dict.update({ 'junk|spermaceti3_'+"".join(str(i)):s3})	
  cubit.cmd('create curve vertex {} {} '.format(p3,p1))
  s4=cubit.get_last_id('curve')
  curve_dict.update({ 'junk|spermaceti4_'+"".join(str(i) ) : s4})

  name = 'spermaceti'+"".join(str(i)) 
  cubit.cmd('create surface  {} {} {} {} '.format(s1,s2,s3,s4 ) )
  surface_dict.update({name : cubit.get_last_id('surface')})
  spermacetti_id.append(cubit.get_last_id('surface'))

spermacet(x, y, y_bas, 0.12) 

cubit.cmd('subtract {} from 10 keep'.format( " ".join(str(x) for x in spermacetti_id)))
surface_dict.update({'junk_last' : cubit.get_last_id('surface')})
cubit.cmd('delete surface 10')
cubit.cmd('split surface {} across location vertex {} onto curve {} '.format(surface_dict['junk_last'], vertex_dict['J1'], curve_dict['junk|skull']))
cubit.cmd('Unite {} With {} '.format(surface_dict['sac'], surface_dict['junk_last'] ))
surface_dict.update({'junk' : cubit.get_last_id('surface')})
surface_dict.pop('junk_last')

######## Nouvelles courbes dans le dictionnaire de courbes manuellement ! 

curve_dict.update({'narine|sac_2': 160})
curve_dict.update({'skull|sac_2': 159})
curve_dict.update({'sac|junk': 156})

curve_dict.update({'junk|skull': 158})
curve_dict.update({'narine|junk': 157})


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
curve(['X1', 'X2'], 'right_bord_C')
curve(['X3', 'X4'], 'left_bord_C')
curve(['X3', 'X2'], 'bottom_bord_C')
curve(['X1', 'X4'], 'up_bord_C')
surface('bord_C')
cubit.cmd('subtract {} to {} from surface {} keep'.format(1, 20 , surface_dict['bord_C']) )
surface_dict.update({'eau' : 25})
cubit.cmd('delete surface {} '.format(surface_dict['bord_C']))

cubit.cmd('remove surface 26 noextend')
#surface_dict.update({'tissusB' : 26})


cubit.cmd(f'surface all size 0.01')
######  Block

for k, v in surface_dict.items() :
 cubit.cmd(f'block {v} surface {v}')
 cubit.cmd(f'block {v} element type QUAD4')
 cubit.cmd('block {} name "{}"'.format(v, k))

cubit.cmd(f'block 10 surface 11 to 20')
cubit.cmd(f'block 10 element type QUAD4')
cubit.cmd('block 10 name "spermaceti"')

## Sideset
cubit.cmd('imprint all')
cubit.cmd('merge all')

list_curve_xmax = [166,170, curve_dict['skull'], curve_dict['blubber_haut_arriere'] , curve_dict['blubber_bas_arriere'] ]
cubit.cmd('sideset 1 curve '+" ".join(str(x) for x in list_curve_xmax))
cubit.cmd(f'sideset 1 name "xmax" ')
curve_dict.pop('skull')
curve_dict.pop('blubber_haut_arriere') 
curve_dict.pop('blubber_bas_arriere')

cubit.cmd('sideset 2 curve 168 ')
cubit.cmd(f'sideset 2 name "xmin"')

cubit.cmd('sideset 3 curve 167')
cubit.cmd(f'sideset 3 name "ymin"')

cubit.cmd('sideset 4 curve  169')
cubit.cmd(f'sideset 4 name "ymax"')

def side(name, nb, el1, el2) :
 cubit.cmd('sideset {} curve {}'.format(nb , " ".join(str(v) for k,v in curve_dict.items() if el1 in k and el2 in k) ) )
 cubit.cmd('sideset {} name "{}" '.format(nb, name ))

side("eau|blubber", 5 , "eau", "blubber")
side("case|sac", 6 , "case", "sac")
side("tissus|blubber", 7 , "tissus", "blubber")
side("narine|blubber", 8 , "narine", "blubber")
side("frontal|sac", 9 , "frontal", "sac")
side("narine|junk", 10 , "narine", "junk")
side("case|muscle", 11 , "case", "muscle")
side("narine|sac", 12 , "narine", "sac")

side("sac|skull", 13 , "sac","skull")
side("frontal|skull", 16 , "frontal", "skull")
side("blubber|skull", 15 , "blubber", "skull")
side("junk|spermaceti", 17 , "spermaceti", "junk")
side("tissus|muscle", 18 , "tissus", "muscle")

def side_spermaceti(s, n):
 cubit.cmd('sideset {} curve {}'.format(s, " ".join(str(v) for k,v in curve_dict.items() if list(k)[-1] == str(n) and 'spermaceti' in k ) ))
 cubit.cmd('sideset {} name "junk|spermaceti{}" '.format(s,n  ))
 return

s = 19
n=0
for k,v in curve_dict.items() : 
 if not list(k)[-1].isdigit() and 'spermaceti' not in k:
  s+=1
  cubit.cmd(f'sideset {s} curve {v}' )
  cubit.cmd(f'sideset {s} name "{k}"')
  print(f'sideset {s} name "{k}"')



##### Mesh
cubit.cmd('mesh surface {}'.format(surface_dict['muscle']) )
cubit.cmd('mesh surface {}'.format(surface_dict['narine']) )
cubit.cmd('mesh surface {}'.format(surface_dict['blubber']) )

cubit.cmd('mesh surface all')

cubit.cmd('Set Exodus NetCDF4 On')
cubit.cmd('export mesh "mesh.e" dimension 2 overwrite')


