#!/usr/bin/env python3
import sqlite3
import sys
import shutil
import os

#Existing DB
exist="probe.matches.sqlite"

#To be added DB
toadd="anotherdir/probe.matches.sqlite"

#Output DB
outdb = "merged.sqlite"

#Create new merged DB (copy of "exist" DB)
if os.path.exists(outdb):
    print ("ERROR: output DB already exists: " + outdb)
    sys.exit()
shutil.copy2(exist,outdb)

try:
    conn1 = sqlite3.connect(outdb)
    c1 = conn1.cursor()
except:
    print ("ERROR: cannot open database: " + outdb)

try:
    conn2 = sqlite3.connect(toadd)
    c2 = conn2.cursor()
except:
    print ("ERROR: cannot open database: " + toadd)

#Handle new taxa
query = "SELECT * FROM matches"
taxa1 = list(map(lambda x: x[0], c1.execute(query).description))
taxa1.remove('uce')
taxa2 = list(map(lambda x: x[0], c2.execute(query).description))
taxa2.remove('uce')

new_taxa = list(set(taxa2) - set(taxa1))
if not len(new_taxa):
    print ("ERROR: no new taxa found!")
    print ("Exiting...")
    os.remove(outdb)
    sys.exit()
print ("New taxa: " + str(len(new_taxa)))

dup_taxa = list(set(taxa2) & set(taxa1))
if len(dup_taxa):
    print ("ERROR: Duplicated taxa names found: " + str(len(dup_taxa)))
    print (', '.join(map(str,dup_taxa)))
    print ("Exiting...")
    os.remove(outdb)
    sys.exit()


#Add columns for new taxa
for new_taxon in new_taxa:
    try:
        query = "ALTER TABLE matches ADD COLUMN {0} text".format(new_taxon)
        c1.execute(query)
        query = "ALTER TABLE match_map ADD COLUMN {0} text".format(new_taxon)
        c1.execute(query)
    except:
        print ("error with adding new taxon: " + new_taxon)
        os.remove(outdb)
        sys.exit()
print("...Columns for new taxa added.")


#Handle new loci
query = "SELECT uce FROM matches"
loci1 = c1.execute(query)
loci2 = c2.execute(query)
new_loci = list(set(loci2) - set(loci1))

#Add rows for new loci
if new_loci:
    print ("New loci not already in source DB:", len(new_loci))
    # try:
    all_new_loci = [(new_locus) for new_locus in new_loci]
    c1.executemany("INSERT INTO matches(uce) values (?)", all_new_loci)
    c1.executemany("INSERT INTO match_map(uce) values (?)", all_new_loci)
    print("...Rows for new loci have been added.")
    # except:
    #     print ("+++error with adding new loci")
    #     sys.exit()
else:
    print("No new loci need to be added for the taxa being added.")


#Populate new taxa
for new_taxon in new_taxa:
    # try:
    print (new_taxon)
    query = "SELECT uce, {0} FROM match_map WHERE {0} IS NOT NULL".format(new_taxon)
    for row in c2.execute(query):
        query = "UPDATE match_map SET {0} = ? WHERE uce = ?".format(new_taxon)
        c1.execute(query,[row[1],row[0]])
        query = "UPDATE matches SET {0} = 1 WHERE uce = ?".format(new_taxon)
        c1.execute(query,[row[0]])
    # except:
    #     print ("error with adding new taxon: " + new_taxon)
    #     sys.exit()
print("Data for new taxa added.")

conn1.commit()
conn1.close()
