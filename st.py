#-*- coding: utf-8 -*-
import re

file_domain = 'domain_srb.txt'
file_list = 'list_ab.txt'
file_black_list = 'black_user_list.txt' # Исключение пользователей

file_resources = 'resources.xml'
file_config = 'config.xml'

res_num = 0
user_name = ''


def delite_simbol_new_line(stroka):
    if stroka[-1] == '\n':
        return stroka[:-1]
    else:
        return stroka


with open(file_resources, 'w') as f_resources, open(file_config, 'w') as f_config, open(file_domain, 'r') as f_domain, open(file_list, 'r') as f_list, open(file_black_list, 'r') as f_black_list:
    f_resources.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<resources>\n')
    f_config.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<routes>\n')

    domain = [delite_simbol_new_line(i) for i in f_domain.readlines()]
    black_list = [delite_simbol_new_line(i) for i in f_black_list.readlines()]
    
    for line in f_list:
        flag_user_ignore = False
        line = line.strip()
        if not line:
            continue
        line_part = line.split()[0]
        
        if user_name == line_part.split('/')[-2]: # Уже обработанный юзер не нужен 
            continue

        user_name = line_part.split('/')[-2]

        for i in black_list:
            if re.search(i, user_name, re.I):
                flag_user_ignore = True
                break

        if flag_user_ignore:
            continue

        for _ in range(4):
            res_num += 1
            f_resources.write('  <resource>\n    <ID>resource' + str(res_num) + '</ID>\n    <Name>' + user_name)
            if _ % 2 == 0:
                f_resources.write('_LAN_')
            else:
                f_resources.write('_INET_')
            if _ < 2:
                f_resources.write('IN')
            else:
                f_resources.write('OUT')
            
            f_resources.write('</Name>\n    <SmbServer/>\n    <SmbPort>445</SmbPort>\n    <SmbShare>')

            i = ''
            line_part = line.split('/')
            for i in domain:
                if '/'.join(line_part[:-2]) in i:
                    i = i.split()
                    if ((not _ % 2) and i[-1] == 'INET') or ((_ % 2) and i[-1] == 'LAN'):
                        if int(i[0]) % 2:
                            i = domain[domain.index(' '.join(i)) + 1]
                        else:
                            
                            i = domain[domain.index(' '.join(i)) - 1]
                        i = i.split()
                    i = i[1]
                    f_resources.write('/' + i)
                    break
            f_resources.write('</SmbShare>\n    <SmbPath>' + user_name + '/')
            if _ < 2:
                f_resources.write('IN')
            else:
                f_resources.write('OUT')
            f_resources.write('</SmbPath>\n    <SmbDomain>' + i.split('/')[3] + '</SmbDomain>\n    ')
            f_resources.write('<SmbUser>temp</SmbUser>\n    <SmbPassword>temp</SmbPassword>\n    <SmbVersion>2.0</SmbVersion>\n    <Status>true</Status>\n    <Type>SMB</Type>\n  </resource>\n')
            
        #CONFIG.XML
        f_config.write('  <route>\n    <active>false</active>\n    <Name>')
        f_config.write(user_name + '_LAN_to_INET</Name>\n    <sourceResID>resource')
        f_config.write(str(res_num) + '</sourceResID>\n    <targetResID>resource')
        f_config.write(str(res_num-3) + '</targetResID>\n    ')
        f_config.write('<Threads>11</Threads>\n    <IncludeMaskFile></IncludeMaskFile>\n    <MaxFileSize/>\n    <Throttle>1000</Throttle>\n    <ThrottleTimePeriod>10000</ThrottleTimePeriod>\n    <IncludeMaskFolder/>\n    <Recursive>false</Recursive>\n    <ResendFileCount>10</ResendFileCount>\n    <ExcludeMaskFile/>\n    <ExcludeMaskFolder/>\n    <NeedToLog>true</NeedToLog>\n    <NeedsAVCheck>false</NeedsAVCheck>\n    <AvServerID>AVServerEntry2</AvServerID>\n    <SendToDLP>false</SendToDLP>\n    <DLPServerID>null</DLPServerID>\n    <ParseDLPResp>false</ParseDLPResp>\n    <Noop>false</Noop>\n    <ReadLock>exclusive</ReadLock>\n    <ResendMultiplyer>1</ResendMultiplyer>\n    <CalculateCheckSum>false</CalculateCheckSum>\n    <DoneFileTmplSource/>\n    <DoneFileTmplTarget/>\n    <MinDepth/>\n    <MaxDepth>1</MaxDepth>\n    <RemoveOnCommit>false</RemoveOnCommit>\n    <RemoveOnRollback>false</RemoveOnRollback>\n    <TransferFromErrorDir>5</TransferFromErrorDir>\n  </route>\n')

        f_config.write('  <route>\n    <active>false</active>\n    <Name>')
        f_config.write(user_name + '_INET_to_LAN</Name>\n    <sourceResID>resource')
        f_config.write(str(res_num-1) + '</sourceResID>\n    <targetResID>resource')
        f_config.write(str(res_num-2) + '</targetResID>\n    ')
        f_config.write('<Threads>11</Threads>\n    <IncludeMaskFile></IncludeMaskFile>\n    <MaxFileSize/>\n    <Throttle>1000</Throttle>\n    <ThrottleTimePeriod>10000</ThrottleTimePeriod>\n    <IncludeMaskFolder/>\n    <Recursive>false</Recursive>\n    <ResendFileCount>10</ResendFileCount>\n    <ExcludeMaskFile/>\n    <ExcludeMaskFolder/>\n    <NeedToLog>true</NeedToLog>\n    <NeedsAVCheck>false</NeedsAVCheck>\n    <AvServerID>AVServerEntry2</AvServerID>\n    <SendToDLP>false</SendToDLP>\n    <DLPServerID>null</DLPServerID>\n    <ParseDLPResp>false</ParseDLPResp>\n    <Noop>false</Noop>\n    <ReadLock>exclusive</ReadLock>\n    <ResendMultiplyer>1</ResendMultiplyer>\n    <CalculateCheckSum>false</CalculateCheckSum>\n    <DoneFileTmplSource/>\n    <DoneFileTmplTarget/>\n    <MinDepth/>\n    <MaxDepth>1</MaxDepth>\n    <RemoveOnCommit>false</RemoveOnCommit>\n    <RemoveOnRollback>false</RemoveOnRollback>\n    <TransferFromErrorDir>5</TransferFromErrorDir>\n  </route>\n')
        
                              
    f_resources.write('</resources>\n')
    f_config.write('</routes>')
