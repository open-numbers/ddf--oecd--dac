# -*- coding: utf-8 -*-


from ddf_utils.factory import oecd


if __name__ == '__main__':
    oecd.bulk_download('../source/', 'TABLE5')
    print('Done.')
