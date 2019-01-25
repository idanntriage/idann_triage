import matplotlib.pyplot as plt
import numpy as np
import sankey #which is a modified version of pysankey


def fill_zero_size(totals,ESI_list):
    list = []
    for esi in ESI_list:
        if (totals["ESI"] == esi).any() :
            list.append(totals[totals["ESI"] == esi]['pct'].values[0])
        else:
            list.append(0)
    return list  
    

def plot_co_esi(type, Mortality_pct, or_cath_pct, ICU_pct, None_pct,sei_distribution):
    ind = range(len(sei_distribution))
    width = 0.5       # the width of the bars: can also be len(x) sequence
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(7,7)
    #mortality
    mortality_list = fill_zero_size(Mortality_pct,sei_distribution["ESI"])
    mortality = plt.bar(ind, mortality_list, width, color='red',align='center')
    b =mortality_list
    #or_cath
    or_cath_list = fill_zero_size(or_cath_pct,sei_distribution["ESI"])
    or_cath = plt.bar(ind, or_cath_list, width, color='purple', align='center', bottom= b)
    b = np.array(b) + np.array(or_cath_list)
    #icu
    icu_list= fill_zero_size(ICU_pct,sei_distribution["ESI"])
    icu = plt.bar(ind, icu_list, width, color='orange',  align='center',bottom= b)
    b = np.array(b) + np.array(icu_list)
    #None
    none_list = fill_zero_size(None_pct,sei_distribution["ESI"])
    none  = plt.bar(ind, none_list, width, color='gray', align='center', bottom= b)
    plt.grid(True)
    plt.ylabel('Percentage', fontsize=18)
    plt.xlabel('ESI',fontsize=18)
    plt.title(type  +' Critical Outcomes by New ESI', fontsize=18)
    plt.xticks(ind, sei_distribution ['ESI'], fontsize=16)
    plt.legend((mortality[0], or_cath[0], icu[0], none[0]), ('Mortality', 'OR_CATH', 'ICU', 'None'), fontsize=18)
    return fig, plt

def ESI_CO_distribution_viz (cinput,sei_distribution, type = "",zoom=False):
    CO_esi_distribution = cinput.groupby(['ESI', 'co_type']).size().reset_index(name='counts')
    CO_esi_distribution ['pct'] = CO_esi_distribution ['counts'] / len(cinput)
    print(CO_esi_distribution)
    Mortality_pct = CO_esi_distribution[CO_esi_distribution['co_type'] =='Mortality']
    or_cath_pct = CO_esi_distribution[CO_esi_distribution['co_type'] =='OR_CATH']
    ICU_pct = CO_esi_distribution[CO_esi_distribution['co_type'] =='ICU']
    None_pct = CO_esi_distribution[CO_esi_distribution['co_type'] =='None']
    fig,plt = plot_co_esi(type, Mortality_pct, or_cath_pct, ICU_pct, None_pct,sei_distribution)
    name = 'Critical_Outcome_ESI_distribution_' + type + '.png'
    if zoom:
        plt.ylim(0,0.04) 
        name = 'Critical_Outcome_ESI_distribution_Zoomed' + type + '.png'
    plt.show()
    fig.savefig("../../reports/figures/graphs/compare_esi/" + name)
    


def plot_esi_distributions(old_ecounts, new_ecounts, ylim =0, c1 ='r', c2='b', title = ""):
    
    categories = [1, 2, 3, 4, 5]
    N = 5
    ind = np.arange(N)  # the x locations for the groups
    width = 0.40       # the width of the bars

    fig = plt.figure()
    fig.set_size_inches(10,7)
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, old_ecounts, width, color=c1)
    rects2 = ax.bar(ind+width, new_ecounts, width, color=c2)
    
    ax.tick_params(axis='x', labelsize=18)
    ax.set_ylabel('Count')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(categories)
    ax.legend( (rects1[0], rects2[0]), ('Original ESI', 'IDANN') )
    ax.grid(True)
    
    if ylim> 0:
        ax.set_ylim(0,ylim)
    else:
        max_value = max( max(old_ecounts), max(new_ecounts) )
        ax.set_ylim(0,max_value + max_value/9 )

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                    ha='center', va='bottom', fontsize = 12)

    autolabel(rects1)
    autolabel(rects2)
    
    plt.title(title, fontsize=18)

    plt.show()
    
def plot_co_esi_comp(type, Mortality_ct, or_cath_ct, ICU_ct, None_ct,
                              Mortality_nct, or_cath_nct, ICU_nct, None_nct, sei_distribution):
    ind = np.arange(5)
    width = 0.4       # the width of the bars: can also be len(x) sequence
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(9,7)
    
    #mortality
    mortality = plt.bar(ind, Mortality_ct, width, color='#e2a3a8')
    b1 = Mortality_ct
    mortality2 = plt.bar(ind+width, Mortality_nct, width, color='#c40715')
    b2 = Mortality_nct
    
    #or_cath
    or_cath = plt.bar(ind, or_cath_ct, width, color='#a384b5',  bottom= b1 )
    b1 = np.array(b1) + np.array(or_cath_ct)
    or_cath2 = plt.bar(ind+width, or_cath_nct, width, color='#591087', bottom=  b2)
    b2 = np.array(b2) + np.array(or_cath_nct)
    #icu
    icu = plt.bar(ind, ICU_ct, width, color='#eda482',  bottom= b1)
    b1 = np.array(b1) + np.array(ICU_ct)
    icu2 = plt.bar(ind+width,  ICU_nct, width, color='#f1822e', bottom=  b2)
    b2 = np.array(b2) + np.array(ICU_nct)
    #None
    #none  = plt.bar(ind, None_ct, width, color='gray', align='center', bottom= b1)
    #none2  = plt.bar(ind+width, None_nct, width, color='gray', align='center', bottom= b2)
    
    
    plt.grid(True)
    plt.ylabel('Counts', fontsize=18)
    plt.xlabel('ESI / ESI-IDANN',fontsize=18)
    plt.title(type  +' CO Comparision between original and ESI IDANN', fontsize=18)
    plt.xticks(ind+width, sei_distribution ['ESI'], fontsize=16)

    
    #plt.legend((mortality[0],mortality2[0],  or_cath[0],or_cath2[0], icu[0],  icu2[0]), 
    #           ('Mortality','Mortality', 'OR_CATH','OR_CATH', 'ICU', 'ICU'), fontsize=18,bbox_to_anchor=(1, 1))
    
    plt.legend((mortality2[0], or_cath2[0],  icu2[0]), 
               ('Mortality', 'OR_CATH', 'ICU'), fontsize=18,bbox_to_anchor=(1, 1))

    return fig, plt

def ESI_CO_compare_viz (cinput, type = "",zoom=False):
    sei_distribution = cinput.groupby(['ESI']).size().reset_index(name='counts')
    sei_distribution ['pct'] = sei_distribution ['counts'] / len(cinput)


    CO_esi_distribution = cinput.groupby(['ESI', 'co_type']).size().unstack(fill_value=0).stack().reset_index(name='counts')
    #print(CO_esi_distribution)    
    CO_nesi_distribution = cinput.groupby(['new_esi', 'co_type']).size().unstack(fill_value=0).stack().reset_index(name='counts')
    #print(CO_nesi_distribution)
    
    
    Mortality_ct = CO_esi_distribution[CO_esi_distribution['co_type'] =='Mortality']['counts']


    or_cath_ct = CO_esi_distribution[CO_esi_distribution['co_type'] =='OR_CATH']['counts']
    ICU_ct = CO_esi_distribution[CO_esi_distribution['co_type'] =='ICU']['counts']
    None_ct = CO_esi_distribution[CO_esi_distribution['co_type'] =='None']['counts']
    
    Mortality_nct = CO_nesi_distribution[CO_nesi_distribution['co_type'] =='Mortality']['counts']
    or_cath_nct = CO_nesi_distribution[CO_nesi_distribution['co_type'] =='OR_CATH']['counts']
    ICU_nct = CO_nesi_distribution[CO_nesi_distribution['co_type'] =='ICU']['counts']
    None_nct = CO_nesi_distribution[CO_nesi_distribution['co_type'] =='None']['counts']

    
    
    fig,plt = plot_co_esi_comp(type, Mortality_ct, or_cath_ct, ICU_ct, None_ct,
                              Mortality_nct, or_cath_nct, ICU_nct, None_nct, sei_distribution)
    name = 'Critical_Outcome_ESI_distribution_' + type + '.png'
    if zoom:
        plt.ylim(0,1000) 
        name = 'Critical_Outcome_ESI_distribution_Zoomed' + type + '.png'
    plt.show()
    fig.savefig("../../reports/figures/graphs/compare_esi/" + name)  
    
def show_esi_compare_viz(cdc_info):

    #ESI
    old_esi_counts, new_esi_counts = get_esi_counts(cdc_info['ESI'].tolist(), cdc_info['new_esi'].tolist())
    plot_esi_distributions(old_esi_counts, new_esi_counts,  c1 ='#91b0e2', c2='#043077' , 
                       title= "Patients per ESI Category")

    #mortality
    deaths = cdc_info.loc[cdc_info['co_type'] == 'Mortality']
    old_esi_death_counts, new_esi_death_counts = get_esi_counts(deaths['ESI'].tolist(), deaths['new_esi'].tolist())
    plot_esi_distributions(old_esi_death_counts, new_esi_death_counts, 
                                       c1 ='#e2a3a8', c2='#c40715' ,      title= "Mortality per ESI Category")
    #ICU
    ICU = cdc_info.loc[cdc_info['co_type'] == 'ICU']
    old_esi_icu_counts, new_esi_icu_counts = get_esi_counts(ICU['ESI'].tolist(), ICU['new_esi'].tolist())
    plot_esi_distributions(old_esi_icu_counts, new_esi_icu_counts, 
                                        c1 ='#eda482', c2='#f2582e' ,  title= "ICU per ESI Category")
    #Get OR cases
    OR = cdc_info.loc[cdc_info['co_type'] == 'OR_CATH']
    old_esi_or_counts, new_esi_or_counts = get_esi_counts(OR['ESI'].tolist(), OR['new_esi'].tolist())
    plot_esi_distributions(old_esi_or_counts, new_esi_or_counts, 
                                          c1 ='#a384b5', c2='#591087' ,  title= "OR&Cath per  ESI Category")
    
    ESI_CO_compare_viz  (cdc_info, zoom=False)
    
# Python code to count the number of occurrences
def countX(lst, x):
    return lst.count(x)
 
def get_esi_counts(ESI, new_esi):
    categories = [1, 2, 3, 4, 5]
    old_counts = []
    new_counts = []
    for c in categories:
        old_counts.append(countX(ESI, c))
        new_counts.append(countX(new_esi, c))
    return old_counts, new_counts

def show_sankeys(new_esi, co_bin, rss, ESI):

    colorDict =  {1:'#f71b1b',2:'#f78c1b',3:'#f3f71b',4:'#12e23f',5:'#1b7ef7',0:'#12e23f'}

    #Critical Outcome to New ESI
    print("Critical Outcome to New ESI")
    unique, counts = np.unique(new_esi, return_counts=True)
    print(dict(zip(unique, counts)))

    sankey.sankey( co_bin,new_esi,aspect=10,colorDict=colorDict,fontsize=15,\
              leftLabels=[0,1], rightLabels=[5,4,3,2,1])
              
    plt.gcf().set_size_inches(20,6)
    plt.show()
    print "-" *100

    #Actual Resources to new ESI
    print("Actual Resources to new ESI")
    unique, counts = np.unique(new_esi, return_counts=True)
    print (dict(zip(unique, counts)))

    sankey.sankey(rss,new_esi,aspect=10,colorDict=colorDict,fontsize=15,leftLabels=[0,1,2], rightLabels=[5,4,3,2,1])
    plt.gcf().set_size_inches(20,6)
    plt.show()
    print "-" *100
    #Actual Resources to Previous ESI
    print ("Actual Resources to Previous ESI")
    unique, counts = np.unique(ESI, return_counts=True)
    print (dict(zip(unique, counts)))
    sankey.sankey(rss,ESI,aspect=10,colorDict=colorDict,fontsize=15,leftLabels=[0,1,2], rightLabels=[5,4,3,2,1])
    plt.gcf().set_size_inches(20,6)
    plt.show()
    print "-" *100
    
    #Previous ESI to New ESI
    print ("Previous ESI to New ESI")
    unique, counts = np.unique(ESI, return_counts=True)
    print (dict(zip(unique, counts)))
    unique, counts = np.unique(new_esi, return_counts=True)
    print (dict(zip(unique, counts)))
    
    sankey.sankey(ESI,new_esi,aspect=10,colorDict=colorDict,fontsize=15,leftLabels=[5,4,3,2,1], rightLabels=[5,4,3,2,1])
    plt.gcf().set_size_inches(20,6)
    plt.show()

