import os, shutil, re, jellyfish, csv

def gap_name_slugify(orig_name):
    #define the replcaing pattern with regex
    ptrn = re.compile('__(health|education).pdf')
    clean_gap = re.sub(ptrn, '', orig_name)
    return clean_gap

def get_sector(orig_name):
    ptrn = re.compile('health|education')
    sector = re.findall(ptrn, orig_name)
    return(sector[0])

def name_replacer(cleaned_gap_names, lgas):
    score = []
    for lga in lgas:
        score.append(jellyfish.jaro_winkler(cleaned_gap_names, lga))
    candidate = lgas[score.index(max(score))]
    if max(score) != 1.0:
        #print 'Original Name: ' + cleaned_gap_names + ' |===> New Name: ' + candidate
        result = candidate
    else: 
        result = cleaned_gap_names
    
    return result

def unique_slug( ):
    with open('./lgas.csv') as infile:
        reader = csv.reader(infile)
        # drop column name
        reader.next()
        # pulling name
        unique_lgas = [row[4] for row in reader]
    return unique_lgas



def process_names(in_folder, out_folder):
    if not (os.path.exists(in_folder) & os.path.isdir(in_folder)):
        print "Error: Gap sheets file folder not exist"
    else:
        if not (os.path.exists(out_folder) & os.path.isdir(out_folder)):
            os.mkdir(out_folder)
        with open("gap_sheet_mapping_health.log", 'aw+') as log:
            health_names = os.listdir(in_folder)
            sector = get_sector(health_names[0])
            lgas = unique_slug()
            for file_name in health_names:
                gap_name = gap_name_slugify(file_name)
                corrected_name = name_replacer(gap_name, lgas)
                src = "%s/%s" % (in_folder, file_name)
                if gap_name != corrected_name:
                    log.write("%s:   Original name: %s |=====> New Name: %s \n" % (sector, gap_name, corrected_name))
                    sanctioned_name = '%s__%s.pdf' % (corrected_name, sector)
                    dst =  "%s/%s" % (out_folder, sanctioned_name)
                else:
                    dst = "%s/%s" % (out_folder, file_name)
                shutil.copyfile(src, dst)


process_names('./gap_sheet/health/', './health_mapped')
process_names('./gap_sheet/education/', './education_mapped')
