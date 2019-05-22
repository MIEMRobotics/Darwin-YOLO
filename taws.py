import os
import sys



import awss3
import boto



aws_dl_object = awss3.AWSDownload()
aws_bucket = aws_dl_object.get_bucket()


test_dir = 'alina-test/'



def del_files():

    test_dir = 'alina-test/resources'
    #'alina-test/secgov-company-data-cik-id/'

    key = 'alina-test/secgov-company-data-cik-id/10-K2018/0000005272.txt'

    input_key = boto.s3.key.Key(aws_bucket)
    input_key.name = key
    html = input_key.get_contents_as_string()

    print("Extracted")
    with open('sasss_gtml.txt', 'wb') as f:
        f.write(html)

    counter = 0
    for key in aws_bucket.list(prefix=test_dir):
        #print(key.name)
        counter += 1

    print(counter)


def delete():
    c = 1
    for key in aws_bucket.list(prefix=''):
        print(c, '  ', key.name)
        c += 1
        aws_bucket.delete_key(key)


def list_tofile():
    l = []
    for key in aws_bucket.list():
        l.append(key.name)
        print(key.name)
    with open('/Users/alinacodzy/Downloads/whatsinside.txt', 'w') as f:
        f.write('\n'.join(l))


def printall():
    c = 1
    for key in aws_bucket.list('robots'):
        #if "trends-data" not in key.name:
        print(c, ' ', key.name)
        c += 1


def list_of_keys(years=[2015], s3_dir='secgov-company-data-cik-id/'):
    """
       alina-test/secgov-company-data-cik-id/10K2018/0000019745.business.clean.spacy
    """
    print("getting list of keys...")
    res = list(filter(lambda x: x.name.split('.')[-1] == 'spacy' and int(x.name.split('/')[1][-4:]) in years,
                       aws_bucket.list(prefix=s3_dir)))
    print(res)
    return len(res)



def download_file():

    for key in aws_bucket.list('alina-test/resources/'):
        if key.name.split('/')[-1][:3] == 'MVP':
            print(key.name)
            input_key = boto.s3.key.Key(aws_bucket)
            input_key.name = key.name
            text = input_key.get_contents_as_string()


            with open('../resources/{}'.format(key.name.split('/')[-1]), 'wb') as f:
                f.write(text)


def sections_info():
    #years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    years = [2010, 2011, 2012]

    for y in years:
        total = 0
        m = 0
        b = 0
        e = 0
        r = 0

        folders = ['secgov-company-data-cik-id/10K{}/'.format(y), 'secgov-company-data-cik-id/20F{}/'.format(y)]
        for dir in folders:
            for key in aws_bucket.list(dir):
                if key.name.endswith('.txt') and (len(key.name.split('.')) == 2):
                    total += 1
                if key.name.endswith('mda.txt'):
                    m += 1
                if key.name.endswith('business.txt'):
                    b += 1
                if key.name.endswith('risk.txt'):
                    r += 1
                if key.name.endswith('parsererror.txt'):
                    e += 1

        print(y, ' ', total, '  TOTAL')
        print(y, ' ', m, '  MDA')
        print(y, ' ', r, '  RISK')
        print(y, ' ', b, '  BUSINESS')
        print(y, ' ', e, '  PARSERERROR')
        print('\n------------------------\n')


def pickle_info():
    import pickle
    from functools import reduce

    years = [2010, 2011, 2013, 2014]
    #2010, 2011, 2012, 2013, 2014,
    companies_data_files = {}

    for YEAR in years:
        companies_data_files[YEAR] = '../resources/MVP-{year}-cleaned-aws-sp-cik-id.pkl'.format(year=YEAR)
    print(companies_data_files)

    for y in years:

        print("Processed: {}".format(companies_data_files[y]))
        with open(companies_data_files[y], 'rb') as handle:
            unpic = pickle.load(handle)
            print("{}  PICKLE LEN... ".format(y), len(unpic))
            print("VOLUME   ", reduce(lambda x, y: x + y, [len(val[1].split(b" ")) for val in unpic.values()]))


TRENDS_S3 = 'alina-test/trends-data/'
def upload_file():

    files = ['/Users/alinacodzy/Documents/TRENDVISION/build-core/core/source/results/new/table-format-2011-trend.xlsx']
    for f in files:
        with open(f, 'rb') as h:
            pik = h.read()
        input_key = boto.s3.key.Key(aws_bucket)
        input_key.name = 'alina-test/matrices/2011' + f.split('/')[-1]
        input_key.set_contents_from_string(pik)
        print(f)


def upload_files():
    from glob import glob

    files = glob('../resources/*')
    print(files)

    for f in files:
        with open(f, 'rb') as h:
            pik = h.read()
        input_key = boto.s3.key.Key(aws_bucket)
        input_key.name = 'alina-test/resources/' + f.split('/')[-1]
        input_key.set_contents_from_string(pik)
        print(input_key.name)


def reload_trends(files):
    #  .parsererror.txt
    for key in files:
        if aws_bucket.get_key(key) is not None:
            print("File was not renamed   ", key)
            continue

        wrongname = key.split('.')[0] + '.full.txt'
        aws_bucket.copy_key(key, bucket_name, wrongname)
        print(wrongname)


def folders():
    from boto3.session import Session
    session = Session(aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key,
                  region_name=region_name)
    _s3 = session.resource("s3")

    for obj in _s3.buckets.all():
        print(obj.name)


def copy():
    t = 'trends_vocab_experiment'

    for key in aws_bucket.list('alina-test/risk/drop-top5/'):

        a, r, d, n = key.name.split('/')
        dst_key_name = os.path.join(a, t, d, n)

        aws_bucket.copy_key(dst_key_name, bucket_name, key.name)
        aws_bucket.delete_key(key)
        if aws_bucket.get_key(dst_key_name) is not None:
            print(dst_key_name, "  del  ", key.name)
        else:
            print("FUCK!")


def trend_pkl_test():
    file = '../resources/ALL-TRENDS-59.pkl'

    import pickle

    pklf = open(file, 'rb')
    trends = pickle.load(pklf)

    print(trends.keys())
    print(trends[next(trends.keys())])





if __name__ == "__main__":
    #del_files()
    #souppp()
    #delete()
    #check()
    printall()
    #sections_info()
    #pickle_info()
    #download_file()
    #reload_trends()
    #upload_file()
    #upload_files()
    #folders()
    #list_of_keys()
    #copy()
    #list_tofile()
    #trend_pkl_test()



