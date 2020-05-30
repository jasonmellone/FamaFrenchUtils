import pandas as pd
import requests
import zipfile
import tempfile
import os


def unzip(arg):
    zf = zipfile.ZipFile(arg)
    return {name: zf.read(name) for name in zf.namelist()}


def industry_portfolio_csv(N_portfolios=49, cleanup=True):
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

    return uz.copy()


if __name__ == '__main__':
    industry_portfolio_csv()
