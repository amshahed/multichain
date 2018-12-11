import json
import codecs
import subprocess
from PyQt5.QtWidgets import QMessageBox


blank = '- - - - - - - - - -'


def get_name(window, chain):
    data = fetch_my_wallets(window, chain)
    for key, value in data.items():
        if '_' not in value:
            return value


def check_name(window, chain, wallet, mine_only=True):
    syms = set('!?_@#$%^&*,[]{}<>/\\|\'\"')
    if len(wallet) < 3 or syms & set(wallet):
        msg = QMessageBox.information(window, 'Invalid name', "Length should be at least 3, only alphanumeric, '.' & '-' are valid")
        return False

    if mine_only:
        name = get_name(window, chain)
        wallet = name + '_' + wallet
        wallets = fetch_my_wallets(window, chain)
    else:
        wallets = fetch_from_stream(window, chain, 'root')
    for key, val in wallets.items():
        if wallet == val:
            msg = QMessageBox.information(window, 'Not Unique!', "Name already exists!")
            return False
    return True


def execute(window, arr):
    p = subprocess.Popen(arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(timeout=2)
    if out.decode('utf-8') == '':
        if window:
            try:
                err = err.decode('utf-8').split('\n')[4]
            except:
                msg = QMessageBox.critical(window, 'Error!', 'An unexpected error occurred')
            else:
                msg = QMessageBox.critical(window, 'Error!', err)
        return False
    else:
        return out


def fetch_from_stream(window, chain, stream, keys=False):
    if not keys:
        arr = ['multichain-cli', chain, 'liststreamitems', stream, 'false', '999999999']
        data = execute(window, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            addr = {}
            for item in data:
                addr[item['key']] = codecs.decode(item['data'], 'hex').decode('ascii')
    else:
        addr = {}
        for key in keys:
            arr = ['multichain-cli', chain, 'liststreamkeyitems', stream, key, 'false', '999999999']
            data = execute(window, arr)
            if data:
                data = json.loads(data.decode('utf-8'))
                for item in data:
                    addr[item['key']] = codecs.decode(item['data'], 'hex').decode('ascii')

    return addr


def fetch_my_wallets(window, chain):
    arr = ['multichain-cli', chain, 'getaddresses']
    out = execute(window, arr)
    if out:
        keys = json.loads(out.decode('utf-8'))
        data = fetch_from_stream(window, chain, 'root', keys)
        return data


def fetch_permissions(window, chain, permissions, addr='*'):
    arr = ['multichain-cli', chain, 'listpermissions', permissions, addr]
    out = execute(window, arr)
    if out:
        data = json.loads(out.decode('utf-8'))
        return data
    else:
        return False


def fetch_wallets_with_single_permission(window, chain, permission, mine_only=False):
    if mine_only:
        addr = fetch_my_wallets(window, chain).keys()
        if not addr:
            return False
        addr = ','.join(addr)
    else:
        addr = '*'

    data = fetch_permissions(window, chain, permission, addr)
    if data:
        addresses = []
        for item in data:
            if item not in addresses:
                addresses.append(item['address'])
        wallets = fetch_from_stream(window, chain, 'root', addresses)
        return wallets
    else:
        return False


def fetch_wallets_with_multiple_permissions(window, chain, permissions):
    data = fetch_permissions(window, chain, permissions)
    wallet_names = fetch_from_stream(window, chain, 'root')
    if data:
        addresses = {}
        for item in data:
            if item['address'] in addresses:
                addresses[item['address']] = addresses[item['address']] + ', ' + item['type'].title()
            else:
                addresses[item['address']] = item['type'].title()

        wallets = {}
        for key, value in addresses.items():
            if key in wallet_names:
                wallets[wallet_names[key]] = value
        return wallets
    else:
        return False

