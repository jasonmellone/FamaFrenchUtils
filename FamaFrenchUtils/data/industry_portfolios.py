import pandas as pd
import requests
import zipfile
import os
import re
import datetime
import numpy as np


def unzip(arg):
    zf = zipfile.ZipFile(arg)
    return [zf.read(name) for name in zf.namelist()]


def extract_date(arg):
    arg = re.findall(string=str(arg), pattern='[0-9]{6}')[0] + '01'
    dt = pd.to_datetime(arg)

    i = 32
    next_dt = dt + datetime.timedelta(i)
    while next_dt.month != dt.month:
        next_dt = dt + datetime.timedelta(i)
        i -= 1
    return dt + datetime.timedelta(i + 1)


def industry_portfolio_csv(N_portfolios=49, cleanup=True, weighting='value'):
    """

    :param N_portfolios:
    :param cleanup:
    :return:
    """
    url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{N}_Industry_Portfolios_CSV.zip'.format(
        N=N_portfolios)

    resp = requests.get(url=url)

    fdir = os.path.expanduser('~') + '/temp/'
    fname = os.path.split(url)[1]
    fpath = fdir + fname

    f = open(fpath, 'wb')
    f.write(resp.content)
    f.close()

    uz = unzip(open(fpath, 'rb'))

    if cleanup:
        os.unlink(fpath)

    lines = str(uz[0]).split('\\r\\n')[11:]

    lines = [l.split(',') for l in lines]

    df = pd.DataFrame(lines[1:], columns=lines[0])

    first_line_break = df[df.iloc[:, 0] == ''].index[0]

    df = df.iloc[0:first_line_break, :]

    df.index = df.iloc[:, 0].apply(extract_date)
    del df['']
    df = df.replace(' -99.99', np.nan)
    df = df.astype(float)

    return df/100.


if __name__ == '__main__':
    industry_portfolio_csv()
