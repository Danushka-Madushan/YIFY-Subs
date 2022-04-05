import requests, webbrowser, re, os
from AjxModules import AjaxRequest

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
def main():
    _querry = input('\n Movie : ')
    if not _querry: None
    else:
        params = {
            'mov': _querry,
        }
        _data, x = {}, 0
        response = requests.get(AjaxRequest.search, headers=headers, params=params)
        if response.status_code == 200:
            for each in response.json():
                if x < 1: print('');x += 1
                else: x += 1
                _data[x] = (each['imdb'], each['movie'])
                print(" |%s| %s" % (str(x).zfill(len(str(len(response.json())))), each['movie']))
        else:
            raise RuntimeError('Error on Search [17] : %s' % response.status_code)
        d = input('\n Select Movie : ')
        if not d: None
        else:
            if not d.isdigit(): None
            else:
                if int(d) > len(_data):
                    print('\n Invalid Selection')
                else:
                    _htm = requests.get(AjaxRequest.get+_data[int(d)][0], headers=headers)
                    if _htm.status_code == 200:
                        _reghtm = re.sub('\n', '', _htm.content.decode('utf-8'))
                        '''with open('base.txt', 'w', encoding='utf-8') as f: f.write(_reghtm)'''# For Debugging Purposes
                        _tabledata = re.findall(r'<tbody>.+</tbody>', _reghtm)[0]
                        engsubs = re.findall(r'%s' % AjaxRequest.Regex['Regex01'], _tabledata)
                    else:
                        raise RuntimeError('Error on GET [34] : %s' % _htm.status_code)
                    _subs, x = {}, 0
                    valids = []
                    for each in engsubs:
                        if each[1] not in valids:
                            x += 1
                            valids.append(each[1])
                            _subs[x] = (each[0], each[1])
                        else:
                            pass
                    x = 0
                    for link in valids:
                        if x == 0: print('');x += 1
                        else: x += 1
                        print(" |%s| %s" % (str(x).zfill(len(str(len(valids)))), link))
                    a = input('\n Select Subtitle : ')
                    if not a: None
                    else:
                        if not a.isdigit(): None
                        else:
                            if int(a) > len(_subs):
                                print('\n Invalid Selection')
                            else:
                                _htm = requests.get(AjaxRequest.download+_subs[int(a)][0], headers=headers)
                                if _htm.status_code == 200:
                                    dlink = re.search(r'%s' % AjaxRequest.Regex['Regex02'], _htm.content.decode('utf-8'))
                                    if dlink:
                                        print("\n Downloading...")
                                        webbrowser.open_new_tab(AjaxRequest.download+dlink.group(1))
                                    else: None
                                else:
                                    raise RuntimeError('Error on GET [65] : %s' % _htm.status_code)
if __name__ == '__main__':
    try:
        while True:
            main()
            _choice = input('\n [Y] to Continue : ')
            if _choice.lower() == 'y': os.system('cls' if os.name == 'nt' else 'clear')
            else: break
    except requests.exceptions.ConnectionError:
        print("\n Connection Error")
    except RuntimeError as e:
        print("\n RuntimeError : %s" % e)
    except KeyboardInterrupt:
        print("\n Keyboard Interrupt Recieved!")
    except Exception as e:
        print("\n Exception : %s" % e)
