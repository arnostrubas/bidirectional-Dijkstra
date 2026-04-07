import networkx as nx
from custom_classes import *
import algorithms_implementation as alg
from functools import partial
import math

#region Graphs
st_node_start = Node("-1", "START")
st_node_target = Node("0", "TARGET")
st_node_1 = Node("1", "1")
st_node_2 = Node("2", "2")
st_node_3 = Node("3", "3")
st_node_4 = Node("4", "4")
st_node_5 = Node("5", "5")
st_node_6 = Node("6", "6")
st_node_7 = Node("7", "7")
st_node_8 = Node("8", "8")
st_node_9 = Node("9", "9")
st_node_10 = Node("10", "10")
st_node_11 = Node("11", "11")
st_node_12 = Node("12", "12")
st_node_13 = Node("13", "13")
st_node_14 = Node("14", "14")

Start_graph = nx.DiGraph()

Start_graph.add_node(st_node_start)
Start_graph.add_node(st_node_target)
Start_graph.add_node(st_node_1)
Start_graph.add_node(st_node_2)
Start_graph.add_node(st_node_3)
Start_graph.add_node(st_node_4)
Start_graph.add_node(st_node_5)
Start_graph.add_node(st_node_6)
Start_graph.add_node(st_node_7)
Start_graph.add_node(st_node_8)
Start_graph.add_node(st_node_9)
Start_graph.add_node(st_node_10)
Start_graph.add_node(st_node_11)
Start_graph.add_node(st_node_12)
Start_graph.add_node(st_node_13)
Start_graph.add_node(st_node_14)

Start_graph.add_edges_from([
    (st_node_start, st_node_1, {'weight': 4, 'id': 'e1'}),
    (st_node_start, st_node_4, {'weight': 5, 'id': 'e2'}),
    (st_node_start, st_node_5, {'weight': 1, 'id': 'e3'}),
    (st_node_start, st_node_3, {'weight': 5, 'id': 'e4'}),
    (st_node_1, st_node_2, {'weight': 12, 'id': 'e6'}),
    (st_node_1, st_node_8, {'weight': 4, 'id': 'e7'}),
    (st_node_2, st_node_7, {'weight': 1, 'id': 'e9'}),
    (st_node_3, st_node_2, {'weight': 12, 'id': 'e10'}),
    (st_node_4, st_node_1, {'weight': 3, 'id': 'e11'}),
    (st_node_4, st_node_14, {'weight': 7, 'id': 'e12'}),
    (st_node_5, st_node_4, {'weight': 3, 'id': 'e13'}),
    (st_node_5, st_node_6, {'weight': 4, 'id': 'e14'}),
    (st_node_6, st_node_3, {'weight': 3, 'id': 'e15'}),
    (st_node_6, st_node_12, {'weight': 1, 'id': 'e16'}),
    (st_node_7, st_node_11, {'weight': 1, 'id': 'e17'}),
    (st_node_8, st_node_9, {'weight': 3, 'id': 'e18'}),
    (st_node_9, st_node_10, {'weight': 6, 'id': 'e19'}),
    (st_node_10, st_node_target, {'weight': 2, 'id': 'e20'}),
    (st_node_10, st_node_11, {'weight': 3, 'id': 'e21'}),
    (st_node_12, st_node_13, {'weight': 5, 'id': 'e22'}),
    (st_node_13, st_node_2, {'weight': 4, 'id': 'e23'}),
    (st_node_14, st_node_8, {'weight': 1, 'id': 'e24'}),
    (st_node_target, st_node_8, {'weight': 4, 'id': 'e25'}),
    (st_node_9, st_node_target, {'weight': 7, 'id': 'e26'}),
    (st_node_target, st_node_7, {'weight': 7, 'id': 'e27'})
])

Start_graph.shortest_path = [st_node_start, st_node_1, st_node_8, st_node_9, st_node_target]
Start_graph.shortest_path_length = 18
Start_graph.start = st_node_start
Start_graph.target = st_node_target


first_encounter_wrong = nx.DiGraph()

few_node_start = Node("-1", "START")
few_node_1 = Node("1", "1")
few_node_2 = Node("2", "2")
few_node_3 = Node("3", "3")
few_node_4 = Node("4", "4")
few_node_5 = Node("5", "5")
few_node_target = Node("0", "TARGET")

first_encounter_wrong.add_node(few_node_start)
first_encounter_wrong.add_node(few_node_1)
first_encounter_wrong.add_node(few_node_2)
first_encounter_wrong.add_node(few_node_3)
first_encounter_wrong.add_node(few_node_4)
first_encounter_wrong.add_node(few_node_5)
first_encounter_wrong.add_node(few_node_target)

first_encounter_wrong.add_edges_from([
    (few_node_start, few_node_1, {'weight': 1, 'id': 'e1'}),
    (few_node_start, few_node_target, {'weight': 1000, 'id': 'e2'}),
    (few_node_start, few_node_4, {'weight': 40, 'id': 'e3'}),
    (few_node_1, few_node_2, {'weight': 1, 'id': 'e4'}),
    (few_node_2, few_node_3, {'weight': 1, 'id': 'e5'}),
    (few_node_3, few_node_4, {'weight': 1, 'id': 'e6'}),
    (few_node_4, few_node_5, {'weight': 1, 'id': 'e7'}),
    (few_node_5, few_node_target, {'weight': 1, 'id': 'e8'})
])

first_encounter_wrong.shortest_path = [few_node_start, few_node_1, few_node_2, few_node_3, few_node_4, few_node_5, few_node_target]
first_encounter_wrong.shortest_path_length = 6
first_encounter_wrong.start = few_node_start
first_encounter_wrong.target = few_node_target

path = nx.DiGraph()

p_node_start = Node("-1", "START")
p_node_target = Node("0", "TARGET")
p_node_1 = Node("1", "1")
p_node_2 = Node("2", "2")
p_node_3 = Node("3", "3")
p_node_4 = Node("4", "4")
p_node_5 = Node("5", "5")
p_node_6 = Node("6", "6")
p_node_7 = Node("7", "7")

path.add_node(p_node_start)
path.add_node(p_node_target)
path.add_node(p_node_1)
path.add_node(p_node_2)
path.add_node(p_node_3)
path.add_node(p_node_4)
path.add_node(p_node_5)
path.add_node(p_node_6)
path.add_node(p_node_7)

path.add_edges_from([
    (p_node_start, p_node_1, {'weight': 5, 'id': 'e1'}),
    (p_node_1, p_node_2, {'weight': 4, 'id': 'e2'}),
    (p_node_2, p_node_3, {'weight': 8, 'id': 'e3'}),
    (p_node_3, p_node_4, {'weight': 5, 'id': 'e4'}),
    (p_node_4, p_node_5, {'weight': 2, 'id': 'e5'}),
    (p_node_5, p_node_6, {'weight': 3, 'id': 'e6'}),
    (p_node_6, p_node_7, {'weight': 7, 'id': 'e7'}),
    (p_node_7, p_node_target, {'weight': 2, 'id': 'e8'})
])

path.shortest_path = [p_node_start, p_node_1, p_node_2, p_node_3, p_node_4, p_node_5, p_node_6, p_node_7, p_node_target]
path.shortest_path_length = 36
path.start = p_node_start
path.target = p_node_target

df_node_start = Node("-1", "START")
df_node_target = Node("0", "TARGET")
df_node_1 = Node("1", "1")
df_node_2 = Node("2", "2")
df_node_3 = Node("3", "3")
df_node_4 = Node("4", "4")
df_node_5 = Node("5", "5")
df_node_6 = Node("6", "6")
df_node_8 = Node("8", "8")
df_node_9 = Node("9", "9")
df_node_10 = Node("10", "10")
df_node_11 = Node("11", "11")

dijkstra_faster = nx.DiGraph()
dijkstra_faster.add_nodes_from([df_node_start, df_node_target, df_node_1, df_node_2, df_node_3, df_node_4, df_node_5, df_node_6, df_node_8, df_node_9, df_node_10, df_node_11])
dijkstra_faster.add_edges_from([
    (df_node_5, df_node_4, {'weight': 4, 'id': 'e18'}),
    (df_node_start, df_node_1, {'weight': 2, 'id': 'e1'}),
    (df_node_1, df_node_3, {'weight': 5, 'id': 'e2'}),
    (df_node_start, df_node_2, {'weight': 8, 'id': 'e3'}),
    (df_node_3, df_node_2, {'weight': 2, 'id': 'e4'}),
    (df_node_3, df_node_4, {'weight': 20, 'id': 'e5'}),
    (df_node_2, df_node_11, {'weight': 5, 'id': 'e6'}),
    (df_node_11, df_node_target, {'weight': 7, 'id': 'e7'}),
    (df_node_10, df_node_target, {'weight': 2, 'id': 'e8'}),
    (df_node_8, df_node_target, {'weight': 6, 'id': 'e9'}),
    (df_node_5, df_node_6, {'weight': 6, 'id': 'e19'}),
    (df_node_6, df_node_target, {'weight': 5, 'id': 'e11'}),
    (df_node_4, df_node_target, {'weight': 6, 'id': 'e12'}),
    (df_node_target, df_node_5, {'weight': 4, 'id': 'e13'}),
    (df_node_target, df_node_9, {'weight': 3, 'id': 'e14'}),
    (df_node_9, df_node_8, {'weight': 4, 'id': 'e15'}),
    (df_node_10, df_node_9, {'weight': 5, 'id': 'e16'}),
    (df_node_11, df_node_9, {'weight': 8, 'id': 'e17'})
])
dijkstra_faster.shortest_path = [df_node_start, df_node_2, df_node_11, df_node_target]
dijkstra_faster.shortest_path_length = 20
dijkstra_faster.start = df_node_start
dijkstra_faster.target = df_node_target

eg_node_start = Node("-1", "START")
eg_node_target = Node("0", "TARGET")

empty_graph = nx.DiGraph()
empty_graph.add_nodes_from([eg_node_start, eg_node_target])
empty_graph.shortest_path = None
empty_graph.shortest_path_length = math.inf
empty_graph.start = eg_node_start
empty_graph.target = eg_node_target

svce_node_start = Node("-1", "START")
svce_node_target = Node("0", "TARGET")
svce_node_1 = Node("1", "1")
svce_node_2 = Node("2", "2")
svce_node_3 = Node("3", "3")
svce_node_4 = Node("4", "4")
svce_node_5 = Node("5", "5")

same_vertex_closed_example = nx.DiGraph()
same_vertex_closed_example.add_nodes_from([svce_node_start, svce_node_target, svce_node_1, svce_node_2, svce_node_3, svce_node_4, svce_node_5])
same_vertex_closed_example.add_edges_from([
    (svce_node_3, svce_node_target, {'weight': 3, 'id': 'e1'}),
    (svce_node_4, svce_node_target, {'weight': 6, 'id': 'e2'}),
    (svce_node_start, svce_node_1, {'weight': 3, 'id': 'e3'}),
    (svce_node_1, svce_node_2, {'weight': 3, 'id': 'e4'}),
    (svce_node_2, svce_node_3, {'weight': 3, 'id': 'e5'}),
    (svce_node_start, svce_node_4, {'weight': 5, 'id': 'e6'}),
    (svce_node_2, svce_node_5, {'weight': 4, 'id': 'e7'}),
    (svce_node_5, svce_node_3, {'weight': 5, 'id': 'e8'})
])
same_vertex_closed_example.shortest_path = [svce_node_start, svce_node_1, svce_node_2, svce_node_3, svce_node_target]
same_vertex_closed_example.shortest_path_length = 12
same_vertex_closed_example.start = svce_node_start
same_vertex_closed_example.target = svce_node_target

hg_node_start = Node("-1", "START")
hg_node_target = Node("0", "TARGET")
hg_node_1 = Node("1", "1")
hg_node_2 = Node("2", "2")
hg_node_3 = Node("3", "3")
hg_node_4 = Node("4", "4")
hg_node_5 = Node("5", "5")
hg_node_6 = Node("6", "6")
hg_node_7 = Node("7", "7")
hg_node_8 = Node("8", "8")
hg_node_9 = Node("9", "9")
hg_node_10 = Node("10", "10")
hg_node_11 = Node("11", "11")
hg_node_12 = Node("12", "12")
hg_node_13 = Node("13", "13")
hg_node_14 = Node("14", "14")
hg_node_15 = Node("15", "15")
hg_node_16 = Node("16", "16")
hg_node_17 = Node("17", "17")
hg_node_18 = Node("18", "18")
hg_node_19 = Node("19", "19")
hg_node_20 = Node("20", "20")
hg_node_21 = Node("21", "21")
hg_node_22 = Node("22", "22")
hg_node_23 = Node("23", "23")
hg_node_24 = Node("24", "24")
hg_node_25 = Node("25", "25")
hg_node_26 = Node("26", "26")
hg_node_27 = Node("27", "27")
hg_node_28 = Node("28", "28")
hg_node_29 = Node("29", "29")
hg_node_30 = Node("30", "30")
hg_node_31 = Node("31", "31")
hg_node_32 = Node("32", "32")
hg_node_33 = Node("33", "33")
hg_node_34 = Node("34", "34")
hg_node_35 = Node("35", "35")
hg_node_36 = Node("36", "36")
hg_node_37 = Node("37", "37")
hg_node_38 = Node("38", "38")
hg_node_39 = Node("39", "39")
hg_node_40 = Node("40", "40")
hg_node_41 = Node("41", "41")
hg_node_42 = Node("42", "42")
hg_node_43 = Node("43", "43")
hg_node_44 = Node("44", "44")
hg_node_45 = Node("45", "45")
hg_node_46 = Node("46", "46")
hg_node_47 = Node("47", "47")
hg_node_48 = Node("48", "48")
hg_node_49 = Node("49", "49")
hg_node_50 = Node("50", "50")
hg_node_51 = Node("51", "51")
hg_node_52 = Node("52", "52")
hg_node_53 = Node("53", "53")
hg_node_54 = Node("54", "54")
hg_node_55 = Node("55", "55")
hg_node_56 = Node("56", "56")
hg_node_57 = Node("57", "57")
hg_node_58 = Node("58", "58")
hg_node_59 = Node("59", "59")
hg_node_60 = Node("60", "60")
hg_node_61 = Node("61", "61")
hg_node_62 = Node("62", "62")
hg_node_63 = Node("63", "63")
hg_node_64 = Node("64", "64")

huge_graph = nx.DiGraph()
huge_graph.add_nodes_from([hg_node_start, hg_node_target, hg_node_1, hg_node_2, hg_node_3, hg_node_4, hg_node_5, hg_node_6, hg_node_7, hg_node_8, hg_node_9, hg_node_10, hg_node_11, hg_node_12, hg_node_13, hg_node_14, hg_node_15, hg_node_16, hg_node_17, hg_node_18, hg_node_19, hg_node_20, hg_node_21, hg_node_22, hg_node_23, hg_node_24, hg_node_25, hg_node_26, hg_node_27, hg_node_28, hg_node_29, hg_node_30, hg_node_31, hg_node_32, hg_node_33, hg_node_34, hg_node_35, hg_node_36, hg_node_37, hg_node_38, hg_node_39, hg_node_40, hg_node_41, hg_node_42, hg_node_43, hg_node_44, hg_node_45, hg_node_46, hg_node_47, hg_node_48, hg_node_49, hg_node_50, hg_node_51, hg_node_52, hg_node_53, hg_node_54, hg_node_55, hg_node_56, hg_node_57, hg_node_58, hg_node_59, hg_node_60, hg_node_61, hg_node_62, hg_node_63, hg_node_64])
huge_graph.add_edges_from([
    (hg_node_start, hg_node_1, {'weight': 4, 'id': 'e1'}),
    (hg_node_start, hg_node_3, {'weight': 6, 'id': 'e2'}),
    (hg_node_start, hg_node_4, {'weight': 7, 'id': 'e3'}),
    (hg_node_4, hg_node_22, {'weight': 5, 'id': 'e4'}),
    (hg_node_3, hg_node_22, {'weight': 4, 'id': 'e5'}),
    (hg_node_22, hg_node_49, {'weight': 10, 'id': 'e6'}),
    (hg_node_49, hg_node_27, {'weight': 5, 'id': 'e7'}),
    (hg_node_49, hg_node_28, {'weight': 5, 'id': 'e8'}),
    (hg_node_28, hg_node_3, {'weight': 5, 'id': 'e9'}),
    (hg_node_3, hg_node_2, {'weight': 7, 'id': 'e10'}),
    (hg_node_2, hg_node_1, {'weight': 6, 'id': 'e11'}),
    (hg_node_1, hg_node_5, {'weight': 9, 'id': 'e12'}),
    (hg_node_5, hg_node_8, {'weight': 6, 'id': 'e13'}),
    (hg_node_1, hg_node_10, {'weight': 7, 'id': 'e14'}),
    (hg_node_2, hg_node_10, {'weight': 7, 'id': 'e15'}),
    (hg_node_10, hg_node_8, {'weight': 9, 'id': 'e16'}),
    (hg_node_10, hg_node_9, {'weight': 6, 'id': 'e17'}),
    (hg_node_8, hg_node_14, {'weight': 7, 'id': 'e18'}),
    (hg_node_9, hg_node_8, {'weight': 6, 'id': 'e19'}),
    (hg_node_9, hg_node_41, {'weight': 8, 'id': 'e20'}),
    (hg_node_41, hg_node_42, {'weight': 8, 'id': 'e21'}),
    (hg_node_42, hg_node_14, {'weight': 7, 'id': 'e22'}),
    (hg_node_41, hg_node_13, {'weight': 6, 'id': 'e23'}),
    (hg_node_13, hg_node_40, {'weight': 5, 'id': 'e24'}),
    (hg_node_40, hg_node_41, {'weight': 6, 'id': 'e25'}),
    (hg_node_5, hg_node_7, {'weight': 6, 'id': 'e26'}),
    (hg_node_14, hg_node_7, {'weight': 7, 'id': 'e27'}),
    (hg_node_7, hg_node_15, {'weight': 7, 'id': 'e28'}),
    (hg_node_42, hg_node_43, {'weight': 10, 'id': 'e29'}),
    (hg_node_15, hg_node_42, {'weight': 8, 'id': 'e30'}),
    (hg_node_15, hg_node_43, {'weight': 7, 'id': 'e31'}),
    (hg_node_43, hg_node_19, {'weight': 5, 'id': 'e32'}),
    (hg_node_19, hg_node_16, {'weight': 7, 'id': 'e33'}),
    (hg_node_7, hg_node_16, {'weight': 6, 'id': 'e34'}),
    (hg_node_16, hg_node_17, {'weight': 5, 'id': 'e35'}),
    (hg_node_17, hg_node_44, {'weight': 5, 'id': 'e36'}),
    (hg_node_44, hg_node_6, {'weight': 4, 'id': 'e37'}),
    (hg_node_6, hg_node_20, {'weight': 8, 'id': 'e38'}),
    (hg_node_20, hg_node_18, {'weight': 7, 'id': 'e39'}),
    (hg_node_44, hg_node_18, {'weight': 5, 'id': 'e40'}),
    (hg_node_4, hg_node_21, {'weight': 5, 'id': 'e41'}),
    (hg_node_21, hg_node_23, {'weight': 8, 'id': 'e42'}),
    (hg_node_24, hg_node_23, {'weight': 8, 'id': 'e43'}),
    (hg_node_35, hg_node_24, {'weight': 12, 'id': 'e44'}),
    (hg_node_24, hg_node_25, {'weight': 6, 'id': 'e45'}),
    (hg_node_25, hg_node_58, {'weight': 5, 'id': 'e46'}),
    (hg_node_58, hg_node_35, {'weight': 4, 'id': 'e47'}),
    (hg_node_35, hg_node_26, {'weight': 10, 'id': 'e48'}),
    (hg_node_26, hg_node_21, {'weight': 7, 'id': 'e49'}),
    (hg_node_21, hg_node_6, {'weight': 6, 'id': 'e50'}),
    (hg_node_49, hg_node_29, {'weight': 5, 'id': 'e51'}),
    (hg_node_29, hg_node_32, {'weight': 9, 'id': 'e52'}),
    (hg_node_32, hg_node_33, {'weight': 7, 'id': 'e53'}),
    (hg_node_33, hg_node_target, {'weight': 6, 'id': 'e54'}),
    (hg_node_29, hg_node_31, {'weight': 5, 'id': 'e55'}),
    (hg_node_31, hg_node_33, {'weight': 6, 'id': 'e56'}),
    (hg_node_2, hg_node_11, {'weight': 6, 'id': 'e57'}),
    (hg_node_10, hg_node_12, {'weight': 6, 'id': 'e58'}),
    (hg_node_12, hg_node_13, {'weight': 7, 'id': 'e59'}),
    (hg_node_12, hg_node_39, {'weight': 6, 'id': 'e60'}),
    (hg_node_12, hg_node_38, {'weight': 5, 'id': 'e61'}),
    (hg_node_38, hg_node_30, {'weight': 8, 'id': 'e62'}),
    (hg_node_11, hg_node_30, {'weight': 5, 'id': 'e63'}),
    (hg_node_30, hg_node_45, {'weight': 5, 'id': 'e64'}),
    (hg_node_29, hg_node_46, {'weight': 5, 'id': 'e65'}),
    (hg_node_26, hg_node_37, {'weight': 5, 'id': 'e66'}),
    (hg_node_37, hg_node_34, {'weight': 5, 'id': 'e67'}),
    (hg_node_34, hg_node_57, {'weight': 8, 'id': 'e68'}),
    (hg_node_target, hg_node_57, {'weight': 5, 'id': 'e69'}),
    (hg_node_57, hg_node_55, {'weight': 5, 'id': 'e70'}),
    (hg_node_55, hg_node_56, {'weight': 7, 'id': 'e71'}),
    (hg_node_35, hg_node_57, {'weight': 4, 'id': 'e72'}),
    (hg_node_53, hg_node_target, {'weight': 7, 'id': 'e73'}),
    (hg_node_53, hg_node_33, {'weight': 5, 'id': 'e74'}),
    (hg_node_48, hg_node_53, {'weight': 5, 'id': 'e75'}),
    (hg_node_53, hg_node_52, {'weight': 7, 'id': 'e76'}),
    (hg_node_50, hg_node_48, {'weight': 6, 'id': 'e77'}),
    (hg_node_50, hg_node_52, {'weight': 5, 'id': 'e78'}),
    (hg_node_47, hg_node_48, {'weight': 6, 'id': 'e79'}),
    (hg_node_51, hg_node_50, {'weight': 4, 'id': 'e80'}),
    (hg_node_51, hg_node_47, {'weight': 7, 'id': 'e81'}),
    (hg_node_53, hg_node_54, {'weight': 6, 'id': 'e82'}),
    (hg_node_54, hg_node_55, {'weight': 6, 'id': 'e83'}),
    (hg_node_60, hg_node_55, {'weight': 5, 'id': 'e84'}),
    (hg_node_59, hg_node_60, {'weight': 12, 'id': 'e85'}),
    (hg_node_35, hg_node_56, {'weight': 10, 'id': 'e86'}),
    (hg_node_56, hg_node_36, {'weight': 6, 'id': 'e87'}),
    (hg_node_36, hg_node_59, {'weight': 6, 'id': 'e88'}),
    (hg_node_64, hg_node_52, {'weight': 5, 'id': 'e89'}),
    (hg_node_61, hg_node_64, {'weight': 6, 'id': 'e90'}),
    (hg_node_61, hg_node_54, {'weight': 6, 'id': 'e91'}),
    (hg_node_62, hg_node_54, {'weight': 4, 'id': 'e92'}),
    (hg_node_62, hg_node_60, {'weight': 4, 'id': 'e93'}),
    (hg_node_63, hg_node_62, {'weight': 9, 'id': 'e94'}),
    (hg_node_63, hg_node_59, {'weight': 10, 'id': 'e95'}),
    (hg_node_23, hg_node_26, {'weight': 4, 'id': 'e96'})
])
huge_graph.shortest_path = [hg_node_start, hg_node_3, hg_node_22, hg_node_49, hg_node_29, hg_node_31, hg_node_33, hg_node_target]
huge_graph.shortest_path_length = 42
huge_graph.start = hg_node_start
huge_graph.target = hg_node_target

love_node_start = Node("-1", "START")
love_node_target = Node("0", "TARGET")
love_node_1 = Node("1", "1")
love_node_2 = Node("2", "2")
love_node_3 = Node("3", "3")
love_node_4 = Node("4", "4")
love_node_6 = Node("6", "6")
love_node_7 = Node("7", "7")
love_node_9 = Node("9", "9")
love_node_8 = Node("8", "8")
love_node_5 = Node("5", "5")
love_node_10 = Node("10", "10")
love_node_11 = Node("11", "11")
love_node_12 = Node("12", "12")

less_open_vertexes_example = nx.DiGraph()
less_open_vertexes_example.add_nodes_from([love_node_start, love_node_target, love_node_1, love_node_2, love_node_3, love_node_4, love_node_6, love_node_7, love_node_9, love_node_8, love_node_5, love_node_10, love_node_11, love_node_12])
less_open_vertexes_example.add_edges_from([
    (love_node_9, love_node_3, {'weight': 1, 'id': 'e1'}),
    (love_node_start, love_node_1, {'weight': 5, 'id': 'e2'}),
    (love_node_start, love_node_2, {'weight': 6, 'id': 'e3'}),
    (love_node_6, love_node_7, {'weight': 4, 'id': 'e4'}),
    (love_node_1, love_node_4, {'weight': 4, 'id': 'e5'}),
    (love_node_start, love_node_8, {'weight': 6, 'id': 'e6'}),
    (love_node_2, love_node_6, {'weight': 4, 'id': 'e7'}),
    (love_node_4, love_node_9, {'weight': 10, 'id': 'e8'}),
    (love_node_3, love_node_target, {'weight': 4, 'id': 'e9'}),
    (love_node_7, love_node_3, {'weight': 7, 'id': 'e10'}),
    (love_node_1, love_node_5, {'weight': 1, 'id': 'e11'}),
    (love_node_5, love_node_10, {'weight': 2, 'id': 'e12'}),
    (love_node_8, love_node_10, {'weight': 4, 'id': 'e13'}),
    (love_node_8, love_node_5, {'weight': 1, 'id': 'e14'}),
    (love_node_10, love_node_11, {'weight': 5, 'id': 'e15'}),
    (love_node_5, love_node_12, {'weight': 5, 'id': 'e16'}),
    (love_node_12, love_node_11, {'weight': 7, 'id': 'e17'}),
    (love_node_11, love_node_6, {'weight': 5, 'id': 'e18'})
])
less_open_vertexes_example.shortest_path = [love_node_start, love_node_1, love_node_4, love_node_9, love_node_3, love_node_target]
less_open_vertexes_example.shortest_path_length = 24
less_open_vertexes_example.start = love_node_start
less_open_vertexes_example.target = love_node_target

graphs = [
    ("START GRAPH", Start_graph),
    ("FIRST ENCOUNTER WRONG", first_encounter_wrong),
    ("PATH", path),
    ("DIJKSTRA FASTER", dijkstra_faster),
    ("EMPTY GRAPH", empty_graph),
    ("HUGE GRAPH", huge_graph),
    ("LESS OPEN VERTEXES EXAMPLE",less_open_vertexes_example)
]
#endregion

algorithms = [
    ("Dijkstra", alg.Dijkstra),
    ("search: after one vertex, end : same vertex closed", alg.bidirectional_Dijkstra_1),
    ("search: after one vertex, end: first encounter", alg.bidirectional_Dijkstra_2),
    ("search: after one vertex, end: using search distance", alg.bidirectional_Dijkstra_3),
    ("search: less open vertexes, end: same vertex closed", alg.bidirectional_Dijkstra_4),
    ("search: less open vertexes, end: first encounter", alg.bidirectional_Dijkstra_5),
    ("search: less open vertexes, end: using search distance", alg.bidirectional_Dijkstra_6),
    ("search: queue with lower priority, end: same vertex closed", alg.bidirectional_Dijkstra_7),
    ("search: queue with lower priority, end: first encounter", alg.bidirectional_Dijkstra_8),
    ("search: queue with lower priority, end: using search distance", alg.bidirectional_Dijkstra_9),
    ("search: after one edge, end: same vertex closed", alg.bidirectional_Dijkstra_10),
    ("search: after one edge, end: first encounter", alg.bidirectional_Dijkstra_11),
    ("search: after one edge, end: using search distance", alg.bidirectional_Dijkstra_12),
]
print("==============================================")
print("                 Starting tests"               )
print("==============================================\n")
for graph_name, graph in graphs:

    print("-------" + graph_name + " TEST-------")
    w = partial(alg.w_function, graph)
    correct = 0
    incorrect = []
    for name, algorithm in algorithms:
        length, path = algorithm(graph, w, graph.start, graph.target)
        
        if(length == graph.shortest_path_length and path == graph.shortest_path): correct += 1
        else: 
            incorrect.append(name)

    print("Results: " )
    print("Correct: " + str(correct) + "/13")
    if(correct != 13):
        print("algorithms that didnt find shortest path and its length:")
        for name in incorrect:
            print(name)
    
    print ("-------" + graph_name + " TEST COMPLETE-------\n\n")

print("==============================================")
print("                test completed"               )
print("==============================================\n")
