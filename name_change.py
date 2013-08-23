# see the structure of the directories,
# distinct between health and education
# for health, find delineation of LGA and STATE
# for education, state is the folder name, lga is the first few words of the 
# name
# lowecase it
# snakecase it 
# hi_how_are_you hiHowAreYou
# enugu_isi_uzo__health.pdf
# enugu_isi_uzo is the slug of the lga, unique_name
# health is the sector
# that's all we are interested in
# csv with unique_lga, state, lga
import os
from shutil import copyfile
import re
import datetime

# now let's deal with health
def sluggify(filename):
    ws = re.compile('\s+')
    new_fn = re.sub(ws, '_', filename)
    return new_fn

def clean_white_space(filename):
    ws = re.compile('(^\s+|\s+$)')
    new_fn = re.sub(ws, '', filename)
    return new_fn


def type_one(filename):
    try:
        filename = filename.lower()
        if "fct" in filename:
            filename = filename.split('.pdf')[0] + " state.pdf"
        lga, state = filename.split('state')[0].split('lga')
        lga = clean_white_space(lga)
        state = clean_white_space(state)
        new_fn = "%s_%s__health.pdf" % (sluggify(state), sluggify(lga))
        return new_fn
    except Exception:
        print "Error processing filename: %s" % filename

#print type_one('Federal District LGA FCT.pdf')


def type_two(filename):
    try:
        filename = filename.lower()
        suffix = re.compile("\.pdf")
        lga_state = re.sub(suffix, "", filename)
        tokens = lga_state.split(' ')
        if "ibom" == tokens[-1]:
            if "akwa" == tokens[-2]:
                lga = "_".join(clean_white_space(item) for item in tokens[:-2])
                state = "_".join(clean_white_space(item) for item in tokens[-2:])
            else:
                raise Exception
        elif "river" == tokens[-1]:
            if "cross" == tokens[-2]:
                lga = "_".join(clean_white_space(item) for item in tokens[:-2])
                state = "_".join(clean_white_space(item) for item in tokens[-2:])
        else:
            lga = "_".join(clean_white_space(item) for item in tokens[:-1])
            state = clean_white_space(tokens[-1])
        return "%s_%s__health.pdf" %(state, lga)

    except Exception:
        print "Error processing filename: %s" % filename

#print type_two("Enugu East Enugu.pdf")
#print type_two("Aro Akjwa Cross River.pdf")
#print type_two("Blah Akwa Ibom.pdf")

def health_convert(filename):
    # e.g. Isi Uzo LGA Enugu State.pdf
    # becomes enugu_isi_uzo__health.pdf
    # check if LGA nd State in there
    #assume where there is LGA there's State or FCT
    if "LGA" in filename:
        return type_one(filename)
    else:
        return type_two(filename)

def education_convert(filename):
    # only scrape the LGA name from the filename
    try:
        trailing_token = re.compile('\-[A-Z][A-Z]\-Ed\sGap\sSheet\.pdf')
        if re.search(trailing_token, filename):
            raw_lga = re.sub(trailing_token, '', filename)
        else:
            raise Exception
        white_or_dash = re.compile('(\s+|\-+)')
        lga = re.sub(white_or_dash, '_', clean_white_space(raw_lga.lower()))
        return lga

    except Exception:
        print "Error processing filename: %s" % filename

#print health_convert('Federal District LGA FCT.pdf')
#print health_convert("Aro Akjwa Cross River.pdf")

folders = os.listdir('.')
health_folders = [item for item in folders if "Health" in item]
education_folders = [item for item in folders if "Education" in item]

def process_health():
    timestamp = str(datetime.datetime.now())
    with open(timestamp + "_health.log", 'w+') as log:
        for folder in health_folders:
            filelist = os.listdir("./" + folder)
            for f in filelist:
                try:
                    src = "%s/%s" % (folder, f)
                    sanctioned_name = health_convert(f)
                    dst = "health/%s" % sanctioned_name
                    log.write("copying from %s to %s\n" % (src, dst))
                    copyfile(src, dst)
                except:
                    log.write("cannot copy %s/%s\n" % (folder, f))


def process_education():
    timestamp = str(datetime.datetime.now())
    with open(timestamp + "_education.log", 'w+') as log:
        for folder in education_folders:
            state_list = os.listdir('./' + folder)
            for state in state_list:
                state_slug = sluggify(state.lower())
                file_list = os.listdir('./%s/%s' % (folder, state))
                for f in file_list:
                    try:
                        lga_slug = education_convert(f)
                        sanctioned_name = "%s_%s__education.pdf" % (state_slug, lga_slug)
                        src = "%s/%s/%s" % (folder, state, f)
                        dst = "education/%s" % sanctioned_name
                        log.write("copying from %s to %s\n" % (src, dst))
                        copyfile(src, dst)
                    except:
                        log.write("cannot copy %s/%s\n" % (folder, f))

process_health()
process_education()

