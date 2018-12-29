# -*- coding: utf-8 -*-


from ddf_utils.factory import OECDLoader


if __name__ == '__main__':
    oecd = OECDLoader()
    oecd.bulk_download('../source/', 'TABLE5')
    print('Done.')
