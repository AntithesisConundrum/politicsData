from urllib2 import urlopen
precincts = """01-CASS
02-CENTER 1
03-CENTER 2
04-CENTER 3
05-CENTER 4
06-CENTER 5
07-CLINTON
08-COOLSPRING 1
09-COOLSPRING 2
10-COOLSPRING 3
11-COOLSPRING 4
12-COOLSPRING 5
13-DEWEY
14-DUNELAND BEACH
15-GALENA 1
16-GALENA 2
17-HANNA
18-HUDSON
19-JOHNSON
20-KANKAKEE 1
21-KANKAKEE 2
22-KINGSBURY
23-KINGSFORD HEIGHTS
24-LaCROSSE
26-LINCOLN
27-LONG BEACH
28-LP25
29-LP26
30-LP27
31-LP28
32-LP29
33-LP30
34-LP31
35-LP32
36-LP33
37-LP34
38-LP35
39-LP36
40-LP37
41-LP38
42-LP39
43-LP40
44-LP41
45-LP42
46-LP43
47-LP44
48-MC01
49-MC02
50-MC03
51-MC04
52-MC05
53-MC06
54-MC07
55-MC08
56-MC09
57-MC10
58-MC11
59-MC12
60-MC13
61-MC14
62-MC15
63-MC16
64-MC17
65-MC18
66-MC19
67-MC20
68-MC21
69-MC22
70-MC23
71-MC24 NV
72-MC45
73-MICHIANA SHORES 01
74-MICHIANA SHORES 02
75-NEW DURHAM  01
76-NEW DURHAM 02
77-NOBLE
78-PLEASANT
79-POTTAWATTOMIE PARK
80-PRAIRIE
81-SCIPIO 1
82-SCIPIO 2
83-SPRINGFIELD 1
84-SPRINGFIELD 2
85-SPRINGFIELD 3
86-TRAIL CREEK 01
87-TRAIL CREEK 02
88-UNION
89-WANATAH 01
90-WANATAH 02
91-WASHINGTON
92-WESTVILLE
93-WILLS""".split("\n")
pages = {}
num_to_name = {}
for s in precincts:
    i = int(s[:2])
    num_to_name[i] = s
    s = s.replace(" ", "%20")
    url = "http://www.laportecounty.org/Elections/ElectionResults/2018General/LaportePrecSumm_"+s+".htm"
    print url
    f = urlopen(url)
    page = f.read()
    pages[i] = page
f = open("pages", "w")
f.write(repr(pages))

from re import search
def get_class_name(line):
    """
    go from laporte HTML line to the class of that line
    """
    pattern = "class=(.|_|\\t)+?( |>)"
    res = search(pattern, line)
    if res == None:
        return "None"
    return res.group()[6:-1]

def get_data_from_line(line):
    """
    go from laporte HTML line to the data of that line
    """
    pattern = ">.*<"
    if line == "</div>":
        return "close_div"
    return search(pattern, line).group()[1:-1]


def get_precinct_name(num):
    """
    Given precinct name, get precinct number
    """
    return num_to_name[num]

from csv import writer 
name = "20181107__in__general__laporte__precinct.csv"
out_f = open(name, "w")
output = writer(out_f)

# KEY: County, Precinct, Machine Ballots, Absentee Ballots, Provisional Ballots, Total Ballots, Race, Candidate
key = ["County", "Precinct", "Machine Ballots", "Absentee Ballots", "Provisional Ballots", "Total Ballots", "Race", "Candidate"]
output.writerow(key)

# s5_ is the first one we care about

# s5_.f1_ has the race name

# For each s0_ (candidate row):
#   f3_ has Machine votes
#   f4_ has Absentee votes
#   f5_ has Provisional votes
#   f23_ has Total votes
#   f6_ has candidate (WRITE HERE)

# s6_ has a break

# s2_ means we don't care anymore

county = "LaPorte"

precinct_name = "ERROR"
candidate = "ERROR"
race = "ERROR"
total = "ERROR"
provisional = "ERROR"
absentee = "ERROR"
machine = "ERROR"
for precinct in pages.keys():
    print precinct
    page = pages[precinct]
    precinct_name = get_precinct_name(precinct)
    too_early = True
    for line in page.split("\n"):
        # Ignore the ones that're too early - they mess up our system
        if too_early:
            if "s5_" in line:
                print "no longer too early"
                too_early = False
            else:
                continue
        clazz = get_class_name(line)
        if clazz == "f1_":
            race = get_data_from_line(line)
        elif clazz == "f3_":
            machine = get_data_from_line(line)
        elif clazz == "f4_":
            absentee = get_data_from_line(line)
        elif clazz == "f5_":
            provisional = get_data_from_line(line)
        elif clazz == "f23_":
            total = get_data_from_line(line)
        elif clazz == "f6_":
            candidate = get_data_from_line(line)
            row = [county, precinct_name, machine, absentee, provisional, total, race, candidate]
            output.writerow(row)
        elif clazz == "s6_":
            candidate = "ERROR"
            race = "ERROR"
            total = "ERROR"
            provisional = "ERROR"
            absentee = "ERROR"
            machine = "ERROR"
        elif clazz == "s2_":
            break
        else:
            print "not useful", clazz

# KEY: County, Precinct, Machine Ballots, Absentee Ballots, Provisional Ballots, Total Ballots, Race, Candidate

