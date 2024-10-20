from compress_entity_csv import d_dict, r_dict

def avg(l):
    return sum(l)/len(l)

#polarization across specific entities
ent_pol = {}

def get_pol_ent(l1, l2):
    return abs(avg(l1) - avg(l2)) / 4

for key in d_dict:
    if (key in r_dict) and not key.isdigit():
        ent_pol[key] = [get_pol_ent(d_dict[key], r_dict[key]), len(d_dict[key])+len(r_dict[key])]

total_sentiment_d = 0
num_instances2_d = 0
total_sentiment_r = 0
num_instances2_r = 0

for key in d_dict:
    if key in r_dict:
        total_sentiment_d += avg(d_dict[key]) * len(d_dict[key])
        num_instances2_d += len(d_dict[key])
        total_sentiment_r += avg(r_dict[key]) * len(r_dict[key])
        num_instances2_r += len(r_dict[key])

total = 0
iter = 0

for v in ent_pol.values():
    total += v[0] * v[1]
    iter += v[1]

total_pol = total/iter

