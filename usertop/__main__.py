from libusers import mapping
import re
from datetime import datetime, timedelta
import psutil
import shutil

def main():

    user_map = mapping.get_lazy_updated().map
    shell_width = shutil.get_terminal_size((80,20)).columns
    ulen = max([len(user_map[p.username()]) for p in psutil.process_iter() if p.username() in user_map])
    pidlen = 5
    deptlen = 5
    startlen = 5
    commlen = shell_width - 12 - deptlen - ulen - pidlen - startlen
    curr_time = datetime.now()

    pinfo = [f"{'User':{ulen}} | {'Dept':{deptlen}} | {'PID':{pidlen}} | {'Start':{startlen}} | {'Command':{commlen}}"]
    pinfo += ['-'*(ulen+1) + '+' + '-'*(deptlen+2) + '+' + '-'*(pidlen+2) + '+' + '-'*(startlen+2) + '+' + '-'*(commlen+1)]
    processes = []
    for p in psutil.process_iter():
        uname = p.username()
        if uname not in user_map:
            continue
        processes.append({
            'uname': uname,
            'pid': p.pid,
            'dept': uname[:5],
            'create_time': datetime.fromtimestamp(p.create_time()),
            'command': p.cmdline()
        })

    processes.sort(key=lambda x:x['create_time'])

    for process in processes:
        
        uname = user_map[process['uname']]
        pid = str(process['pid'])
        create_time = process['create_time']
        if (curr_time - create_time > timedelta(days=1)):
            create_time = create_time.strftime('%b%d')
        else:
            create_time = create_time.strftime('%H:%M')
        command = ' '.join(process['command'])
        if len(command) > commlen:
            command = command[:commlen-3]+"..."

        dept = 'prof?'
        if re.match(r'[a-z]{2}[a-z0-9][0-9]{2}', process['dept']):
            dept = process['dept']

        pinfo.append(f'{uname:{ulen}} | {dept:{deptlen}} | {pid:{pidlen}} | {create_time:{startlen}} | {command:{commlen}}')

    print('\n'.join(pinfo))

if __name__ == "__main__":
    main()
