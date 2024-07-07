# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 18:10:25 2024

@author: Mathis Girard

Estimated work time : 15 hours
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd

'''Window'''
window = tk.Tk()
window.title('Calcul ACV micro-ondes')
window.geometry('1920x1080')

'''GUI Frames'''
left_frame = ttk.Frame(window, border= True, borderwidth= 10)
#Top left frames (caracteristic frames)
caracteristics_frame = ttk.Frame(left_frame)
use_time_frame = ttk.Frame(caracteristics_frame)
place_used_frame = ttk.Frame(caracteristics_frame)
power_cons_frame = ttk.Frame(caracteristics_frame)
cycle_time_frame = ttk.Frame(caracteristics_frame)
nb_cycle_frame = ttk.Frame(caracteristics_frame)

list_carac_frames = [use_time_frame,
                     place_used_frame,
                     power_cons_frame,
                     cycle_time_frame,
                     nb_cycle_frame]

#Bottom left frames (Conception and production frames)
conception_frame = ttk.Frame(left_frame)
material_frame = ttk.Frame(conception_frame)
pmma_frame = ttk.Frame(material_frame)
steel_frame = ttk.Frame(material_frame)
copper_frame = ttk.Frame(material_frame)
pcb_frame = ttk.Frame(material_frame)
loss_frame = ttk.Frame(conception_frame)
place_prod_frame = ttk.Frame(conception_frame)
power_prod_frame = ttk.Frame(conception_frame)

list_concep_frames = [material_frame,
                      pmma_frame,
                      steel_frame,
                      copper_frame,
                      pcb_frame,
                      loss_frame,
                      place_prod_frame,
                      power_prod_frame]


#Right frame 
right_frame = ttk.Frame(window)
#Results table
headers_frame = ttk.Frame(right_frame)
material_impact_frame = ttk.Frame(right_frame)
processing_impact_frame = ttk.Frame(right_frame)
use_impact_frame = ttk.Frame(right_frame)
transport_impact_frame = ttk.Frame(right_frame)
impact_sum_frame = ttk.Frame(right_frame)
micropoint_frame = ttk.Frame(right_frame)

list_right_frames = [headers_frame, 
                     material_impact_frame,
                     processing_impact_frame,
                     use_impact_frame,
                     transport_impact_frame,
                     impact_sum_frame,
                     micropoint_frame]


'''Variables'''
#GUI variables
use_time_int = tk.IntVar(value = 8)
place_used_str = tk.StringVar(value = "France")
power_cons_int = tk.IntVar(value = 800)
cycle_time_int = tk.IntVar(value = 180)
nb_cycle_int = tk.IntVar(value = 1200)

pmma_mass_float = tk.DoubleVar(value = 3.0)
steel_mass_float = tk.DoubleVar(value = 10.0)
copper_mass_float = tk.DoubleVar(value = 1.0)
pcb_mass_float = tk.DoubleVar(value = 0.1)
loss_rate_int = tk.IntVar(value = 10)
place_prod_str = tk.StringVar(value = "France")
power_prod_int = tk.IntVar(value = 1000)


#Results
material_impact_co2_float = tk.DoubleVar()
material_impact_bq_float = tk.DoubleVar()
material_impact_sb_float = tk.DoubleVar()

processing_impact_co2_float = tk.DoubleVar()
processing_impact_bq_float = tk.DoubleVar()
processing_impact_sb_float = tk.DoubleVar()

use_impact_co2_float = tk.DoubleVar()
use_impact_bq_float = tk.DoubleVar()
use_impact_sb_float = tk.DoubleVar()

transport_impact_co2_float = tk.DoubleVar()
transport_impact_bq_float = tk.DoubleVar()
transport_impact_sb_float = tk.DoubleVar()

total_impact_co2_float = tk.DoubleVar()
total_impact_bq_float = tk.DoubleVar()
total_impact_sb_float = tk.DoubleVar()

material_micropoint = tk.DoubleVar()
processing_micropoint = tk.DoubleVar()
use_micropoint = tk.DoubleVar()
transport_micropoint = tk.DoubleVar()

indic_co2_micropoint = tk.DoubleVar()
indic_bq_micropoint = tk.DoubleVar()
indic_sb_micropoint = tk.DoubleVar()


#Database
col_headers = ['PMMA', 'Acier', 'Cuivre',
               'Transport Maritime',
               'Transport ferroviaire',
               'Transport en camion', 
               'Transport aérien',
               'France - Mix electrique',
               'Chine - Mix electrique']
row_headers = ['kg eq. CO2', 'eq. kBq U235', 'kg eq. Sb']

database = pd.DataFrame([[3.8415, 3.75071, 3.99167, 0.194995, 0.0383035, 0.153948, 1.31701, 0.0813225, 1.05738],
                         [0, -0.0780518, 2.74009, 0.00187267, 0.00967588, 0.00977822, 0.0408758, 3.23443, 0.0649514],
                          [0.00000038285, 0.000114372, 0.00330649,
                           0.00000000646764, 0.000000289056, 0.000000445153, 
                           0.0000000616211, 0.0000000485798, 0.0000000851552]], 
                        index=row_headers, 
                        columns=col_headers)

'''Functions definitions'''
def calculate_material_impact():
    '''
    Calculate the impact of the materials chosen for the product based 
    on the database values.
    '''
    useful_masses = pd.Series([pmma_mass_float.get(), 
                                steel_mass_float.get(), 
                                copper_mass_float.get()], 
                              index = ['PMMA', 'Acier', 'Cuivre'])#PCB is not taken into acount
    useful_masses = useful_masses/(1.0-(loss_rate_int.get()/100))
    material_impact = database[['PMMA', 'Acier', 'Cuivre']].dot(useful_masses)
    material_impact_co2_float.set(material_impact['kg eq. CO2'])
    material_impact_bq_float.set(material_impact['eq. kBq U235'])
    material_impact_sb_float.set(material_impact['kg eq. Sb'])
   
    
def calculate_processing_impact():
    '''
    Calculate the impact of the assembly of the product based on the 
    database values and the country chosen for assembly.
    '''
    processing_impact = (power_prod_int.get()/1000)*database[[place_prod_str.get() + ' - Mix electrique']]
    ser_processing_impact = processing_impact.iloc[:,0]
    processing_impact_co2_float.set(ser_processing_impact['kg eq. CO2'])
    processing_impact_bq_float.set(ser_processing_impact['eq. kBq U235'])
    processing_impact_sb_float.set(ser_processing_impact['kg eq. Sb'])


def calculate_use_impact():
    '''
    Calculate the impact of the use phase of the product based on the
    country where the product is used.
    '''
    total_cycles = use_time_int.get()*nb_cycle_int.get()
    total_use_time = total_cycles*cycle_time_int.get()/3600
    total_consumption = total_use_time*power_cons_int.get()/1000
    use_impact = total_consumption*database[[place_used_str.get() + ' - Mix electrique']]
    ser_use_impact = use_impact.iloc[:,0]
    use_impact_co2_float.set(ser_use_impact['kg eq. CO2'])
    use_impact_bq_float.set(ser_use_impact['eq. kBq U235'])
    use_impact_sb_float.set(ser_use_impact['kg eq. Sb'])


def calculate_transport_impact():
    '''
    Calculate the impact of the transport of the product throughout 
    its lifecycle.
    '''
    french_assembly = pd.DataFrame([[19400,0,19400,18500, 0 + 19400*(place_prod_str.get()!=place_used_str.get())],
                                     [0, 0, 0, 0, 0],
                                     [150, 150, 150, 150, 200],
                                     [0, 0, 0, 0, 0]],
                                   columns = ['PMMA', 'Acier', 'Cuivre', 'PCB', 'Total'])
    
    chinese_assembly = pd.DataFrame([[0,19400,0,900, 0 + 19400*(place_prod_str.get()!=place_used_str.get())],
                                     [0, 0, 0, 0, 0],
                                     [150, 150, 150, 150, 200],
                                     [0, 0, 0, 0, 0]],
                                    columns = ['PMMA', 'Acier', 'Cuivre', 'PCB', 'Total'])
    
    material_masses = pd.Series([pmma_mass_float.get()/(1.0-(loss_rate_int.get()/100)), 
                                 steel_mass_float.get()/(1.0-(loss_rate_int.get()/100)), 
                                 copper_mass_float.get()/(1.0-(loss_rate_int.get()/100)),
                                 pcb_mass_float.get()/(1.0-(loss_rate_int.get()/100)),
                                 pmma_mass_float.get() + steel_mass_float.get() + 
                                 copper_mass_float.get() + pcb_mass_float.get()], 
                                 index = ['PMMA', 'Acier', 'Cuivre', 'PCB', 'Total'])
    if place_prod_str.get() == 'France' :
        t_km = french_assembly.dot(material_masses)/1000
    if place_prod_str.get() == 'Chine' :
        t_km = chinese_assembly.dot(material_masses)/1000
    t_km = t_km.set_axis(['Transport Maritime','Transport ferroviaire','Transport en camion', 'Transport aérien'])
    transport_impact = database[['Transport Maritime','Transport ferroviaire','Transport en camion', 'Transport aérien']].dot(t_km)
   
    transport_impact_co2_float.set(transport_impact['kg eq. CO2'])
    transport_impact_bq_float.set(transport_impact['eq. kBq U235'])
    transport_impact_sb_float.set(transport_impact['kg eq. Sb'])
    
    
def update_total ():
    '''
    Update the total amount of each indicator.
    '''
    total_impact_co2_float.set(material_impact_co2_float.get() + 
                               processing_impact_co2_float.get() +
                               use_impact_co2_float.get() +
                               transport_impact_co2_float.get())
    total_impact_bq_float.set(material_impact_bq_float.get() + 
                               processing_impact_bq_float.get() +
                               use_impact_bq_float.get() +
                               transport_impact_bq_float.get())
    total_impact_sb_float.set(material_impact_sb_float.get() + 
                               processing_impact_sb_float.get() +
                               use_impact_sb_float.get() +
                               transport_impact_sb_float.get())
    
    
def calculate_micropoint():
    '''
    Calculate the percentage of micropoint per indicator and per life phase of the product.
    '''
    conversion = pd.Series([28.6, 12.73, 1395510], index=['kg eq. CO2','eq. kBq U235','kg eq. Sb'])
    total_impact = pd.Series([total_impact_co2_float.get(), total_impact_bq_float.get(), total_impact_sb_float.get()],
                             index=['kg eq. CO2','eq. kBq U235','kg eq. Sb'])
    total_micropoint = conversion.dot(total_impact)
    indic_co2_micropoint.set(100*total_impact['kg eq. CO2']*conversion['kg eq. CO2']/total_micropoint)
    indic_bq_micropoint.set(100*total_impact['eq. kBq U235']*conversion['eq. kBq U235']/total_micropoint)
    indic_sb_micropoint.set(100*total_impact['kg eq. Sb']*conversion['kg eq. Sb']/total_micropoint)
    
    total_material_micropoint = material_impact_co2_float.get()*conversion['kg eq. CO2'] + material_impact_bq_float.get()*conversion['eq. kBq U235'] + material_impact_sb_float.get()*conversion['kg eq. Sb']
    total_processing_micropoint = processing_impact_co2_float.get()*conversion['kg eq. CO2'] + processing_impact_bq_float.get()*conversion['eq. kBq U235'] + processing_impact_sb_float.get()*conversion['kg eq. Sb']
    total_use_micropoint = use_impact_co2_float.get()*conversion['kg eq. CO2'] + use_impact_bq_float.get()*conversion['eq. kBq U235'] + use_impact_sb_float.get()*conversion['kg eq. Sb']
    total_transport_micropoint = transport_impact_co2_float.get()*conversion['kg eq. CO2'] + transport_impact_bq_float.get()*conversion['eq. kBq U235'] + transport_impact_sb_float.get()*conversion['kg eq. Sb']
    
    material_micropoint.set(100 * total_material_micropoint/total_micropoint)
    processing_micropoint.set(100 * total_processing_micropoint/total_micropoint)
    use_micropoint.set(100 * total_use_micropoint/total_micropoint)
    transport_micropoint.set(100 * total_transport_micropoint/total_micropoint)
    
    
def calculate_all():
    calculate_material_impact()
    calculate_processing_impact()
    calculate_use_impact()
    calculate_transport_impact()
    update_total()
    calculate_micropoint()



'''GUI widgets'''
##Caracteristic window##
#Labels
label_product_caracteristics = ttk.Label(caracteristics_frame, 
                                         text = 'Caractéristiques du micro-ondes',
                                         background='grey')
label_use_time = ttk.Label(use_time_frame, text= "Années d'utilisation")
label_place_used = ttk.Label(place_used_frame, text="Lieu d'utilisation")
label_power_cons = ttk.Label(power_cons_frame, text='Puissance (W)')
label_cycle_time = ttk.Label(cycle_time_frame, text='Temps de cycle (s)')
label_nb_cycle = ttk.Label(nb_cycle_frame, text='Nombre de cycles par an')

list_carac_labels = [label_use_time, 
                     label_place_used,
                     label_power_cons,
                     label_cycle_time,
                     label_nb_cycle]

#Widgets
entry_use_time = ttk.Entry(use_time_frame, textvariable=use_time_int)

menu_button_place_used = ttk.Menubutton(place_used_frame, textvariable=place_used_str)
place_used_button_sub_menu = tk.Menu(menu_button_place_used, tearoff= False)
place_used_button_sub_menu.add_command(label = 'France',
                                       command = lambda: place_used_str.set('France'))
place_used_button_sub_menu.add_command(label = 'Chine',
                                       command = lambda: place_used_str.set('Chine'))
menu_button_place_used.configure(menu = place_used_button_sub_menu)

slider_power_cons = tk.Scale(power_cons_frame, 
                             from_= 100,
                             to= 1500,
                             length= 200,
                             orient = 'horizontal',
                             variable= power_cons_int)

slider_cycle_time = tk.Scale(cycle_time_frame, 
                             from_= 30,
                             to= 300,
                             length= 200,
                             orient = 'horizontal',
                             variable= cycle_time_int)

entry_nb_cycle = ttk.Entry(nb_cycle_frame, textvariable=nb_cycle_int)

list_carac_widgets = [entry_use_time,
                      menu_button_place_used,
                      slider_power_cons,
                      slider_cycle_time,
                      entry_nb_cycle]



##Conception and production choice window
#Labels
label_conception =  ttk.Label(conception_frame, 
                              text = 'Choix de conception et fabrication',
                              background='grey')
label_prop_materials = ttk.Label(material_frame, text= "Proportion de matériaux (kg)")
label_pmma = ttk.Label(pmma_frame, text= "PMMA")
label_steel = ttk.Label(steel_frame, text= "Acier galva")
label_copper = ttk.Label(copper_frame, text= "Cuivre")
label_pcb = ttk.Label(pcb_frame, text= "PCB")
label_loss = ttk.Label(loss_frame, text='Taux de perte (%)')
label_place_prod = ttk.Label(place_prod_frame, text="Pays d'assemblage")
label_power_prod = ttk.Label(power_prod_frame, text="Energie d'assemblage")

list_concep_labels = [label_prop_materials,
                      label_pmma,
                      label_steel,
                      label_copper,
                      label_pcb,
                      label_loss,
                      label_place_prod,
                      label_power_prod]


#Widgets
entry_pmma = ttk.Entry(pmma_frame, textvariable=pmma_mass_float)
entry_steel = ttk.Entry(steel_frame, textvariable=steel_mass_float)
entry_copper = ttk.Entry(copper_frame, textvariable=copper_mass_float)
entry_pcb = ttk.Entry(pcb_frame, textvariable=pcb_mass_float)

slider_loss = tk.Scale(loss_frame, 
                       from_= 1,
                       to= 20,
                       length= 200,
                       orient = 'horizontal',
                       variable= loss_rate_int)

menu_button_place_prod = ttk.Menubutton(place_prod_frame, textvariable=place_prod_str)
place_prod_button_sub_menu = tk.Menu(menu_button_place_prod, tearoff= False)
place_prod_button_sub_menu.add_command(label = 'France',
                                       command = lambda: place_prod_str.set('France'))
place_prod_button_sub_menu.add_command(label = 'Chine',
                                       command = lambda: place_prod_str.set('Chine'))
menu_button_place_prod.configure(menu = place_prod_button_sub_menu)

slider_power_prod = tk.Scale(power_prod_frame, 
                             from_= 500,
                             to= 2000,
                             length= 200,
                             orient = 'horizontal',
                             variable= power_prod_int)

button_calculate = ttk.Button(left_frame, text= 'Calculer les résultats', command= calculate_all)

list_concep_widgets = [entry_pmma,
                       entry_steel,
                       entry_copper,
                       entry_pcb,
                       slider_loss,
                       menu_button_place_prod,
                       slider_power_prod]


##Results window

label_material_co2 = ttk.Label(material_impact_frame, textvariable=material_impact_co2_float)
label_material_bq = ttk.Label(material_impact_frame, textvariable=material_impact_bq_float)
label_material_sb = ttk.Label(material_impact_frame, textvariable=material_impact_sb_float)
label_micropoint_material = ttk.Label(material_impact_frame, textvariable=material_micropoint)

label_processing_co2 = ttk.Label(processing_impact_frame, textvariable=processing_impact_co2_float)
label_processing_bq = ttk.Label(processing_impact_frame, textvariable=processing_impact_bq_float)
label_processing_sb = ttk.Label(processing_impact_frame, textvariable=processing_impact_sb_float)
label_micropoint_processing = ttk.Label(processing_impact_frame, textvariable=processing_micropoint)

label_use_co2 = ttk.Label(use_impact_frame, textvariable=use_impact_co2_float)
label_use_bq = ttk.Label(use_impact_frame, textvariable=use_impact_bq_float)
label_use_sb = ttk.Label(use_impact_frame, textvariable=use_impact_sb_float)
label_micropoint_use = ttk.Label(use_impact_frame, textvariable=use_micropoint)

label_transport_co2 = ttk.Label(transport_impact_frame, textvariable=transport_impact_co2_float)
label_transport_bq = ttk.Label(transport_impact_frame, textvariable=transport_impact_bq_float)
label_transport_sb = ttk.Label(transport_impact_frame, textvariable=transport_impact_sb_float)
label_micropoint_transport = ttk.Label(transport_impact_frame, textvariable=transport_micropoint)

label_total_co2 = ttk.Label(impact_sum_frame, textvariable=total_impact_co2_float)
label_total_bq = ttk.Label(impact_sum_frame, textvariable=total_impact_bq_float)
label_total_sb = ttk.Label(impact_sum_frame, textvariable=total_impact_sb_float)
label_none_total = ttk.Label(impact_sum_frame)

label_micropoint_co2 = ttk.Label(micropoint_frame, textvariable=indic_co2_micropoint)
label_micropoint_bq = ttk.Label(micropoint_frame, textvariable=indic_bq_micropoint)
label_micropoint_sb = ttk.Label(micropoint_frame, textvariable=indic_sb_micropoint)
label_micropoint_none = ttk.Label(micropoint_frame)



label_results = ttk.Label(right_frame, 
                          text = 'RESULTATS',
                          background='grey')

label_summary = ttk.Label(headers_frame, text = 'Sommaire', background='grey')
label_head_co2 = ttk.Label(headers_frame, text = 'kg eq. CO2')
label_head_bq = ttk.Label(headers_frame, text = 'eq. kBq U235')
label_head_sb = ttk.Label(headers_frame, text = 'kg eq. Sb')
label_head_micropoint = ttk.Label(headers_frame, text = 'µPoint (%)')

label_row_material = ttk.Label(material_impact_frame, text= 'Matériaux')
label_row_processing = ttk.Label(processing_impact_frame, text= 'Processing')
label_row_use = ttk.Label(use_impact_frame, text= 'Utilisation')
label_row_transport = ttk.Label(transport_impact_frame, text= 'Transport')
label_row_total = ttk.Label(impact_sum_frame, text= 'Total')
label_row_indic_micropoint = ttk.Label(micropoint_frame, text= 'µPoint par indicateur (%)')


labels_header = [label_summary, label_head_co2, label_head_bq, label_head_sb, label_head_micropoint]

labels_material_impact = [label_row_material, label_material_co2, label_material_bq, label_material_sb, label_micropoint_material]
labels_processing_impact = [label_row_processing, label_processing_co2, label_processing_bq, label_processing_sb, label_micropoint_processing]
labels_use_impact = [label_row_use, label_use_co2, label_use_bq, label_use_sb, label_micropoint_use]
labels_transport_impact = [label_row_transport, label_transport_co2, label_transport_bq, label_transport_sb, label_micropoint_transport]
labels_total_impact = [label_row_total, label_total_co2, label_total_bq, label_total_sb, label_none_total]
labels_indic_micropoint = [label_row_indic_micropoint, label_micropoint_co2, label_micropoint_bq, label_micropoint_sb, label_micropoint_none]

list_labels = [labels_header,
               labels_material_impact,
               labels_processing_impact,
               labels_use_impact,
               labels_transport_impact,
               labels_total_impact,
               labels_indic_micropoint]

'''GUI Layout'''
label_product_caracteristics.pack(side='top', expand=True, fill='both')
for label in list_carac_labels :
    label.pack(side = 'left', expand=True, fill = 'both')
    
for widget in list_carac_widgets :
    widget.pack(side = 'left', expand= True, fill = 'both')

for frame in list_carac_frames :
    frame.pack(side = 'top', expand=True, fill = 'both')   
caracteristics_frame.pack(expand = True, fill='both', pady= 25)


label_conception.pack(side='top', expand=True, fill='both')
for label in list_concep_labels :
    label.pack(side = 'left', expand=True, fill = 'both')
    
for widget in list_concep_widgets :
    widget.pack(side = 'left', expand= True, fill = 'both')

for frame in list_concep_frames :
    frame.pack(side = 'top', expand=True, fill = 'both')   
conception_frame.pack(expand = True, fill='both', pady = 25)
button_calculate.pack(side = 'top', expand = True, fill = 'both')


label_results.pack(side = 'top', expand=True, fill= 'both')

for list_lab in list_labels : 
    for label in list_lab :
        label.pack(side='left', expand= True, fill= 'both')

for frame in list_right_frames :
    frame.pack(side = 'top', expand = True, fill = 'both')


left_frame.pack(side = 'left', expand = True, fill = 'both', padx=30, pady=50)
right_frame.pack(side ='left', expand= True, fill = 'both', padx=30, pady=50)




'''Run'''
window.mainloop()