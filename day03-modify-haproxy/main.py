import os

def file_handle(filename,backend_data,record_list=None,type='fetch'):
    new_file = filename + "_new"
    bak_file = filename + '_bak'
    if type=='fetch':
        r_list = []
        tag = False
        with open(filename,'r') as f:
            for line in f:
                if line.strip() == backend_data:    #循环文件找到backend www.oldboy.org
                    tag = True
                    continue
                if tag and line.startswith('backend'):    #找到下一个以backend开头的跳出for循环
                    break
                if tag and line:     #找到backend www.oldboy.org并且后面内容不为空
                    r_list.append(line.strip())     #将内容添加到r_list列表中
            for line in r_list:     #将刚刚找到backend www.oldboy.org条目内容打印
                print(line)
            return r_list
    elif type == 'append':      #如果文件中没有这个条目：backend www.oldboy.org
        with open(filename,'r') as read_file,\
                open(new_file,'w') as write_file:
            for r_line in read_file:        #将文件全部写到新文件中
                write_file.write(r_line)

            for new_line in record_list:    #在文件末尾添加用户添加的条目
                if new_line.startswith('backend'):
                    write_file.write(new_line+'\n')
                else:
                    write_file.write('%s %s\n'%(' '*8,new_line))

        if os.path.exists(bak_file):
            os.remove(bak_file)
        os.rename(filename,bak_file)
        os.rename(new_file,filename)

    elif type == 'change':
        new_file = filename + "_new"
        with open(filename,'r') as read_file,\
                open(new_file,'w') as write_file:
            tag = False
            has_write = False
            for r_line in read_file:
                if r_line.strip()==backend_data:    #2 找到backend www.oldboy.org
                    tag = True
                    continue
                if tag and r_line.startswith('backend'):    #4 找到下一个backend开头
                    tag = False
                if not tag:                     #1 没有找到backend www.oldboy.org前正常写入
                    write_file.write(r_line)     #找到下一个backend后正常写入

                else:                         #3 在下一个backend出现前写入的是record_list列表中内容
                    if not has_write:           #确定record_list还未写入
                        for new_line in record_list:
                            if new_line.startswith('backend'):  #写入backend www.oldboy.org
                                write_file.write(new_line+'\n')
                            else:
                                write_file.write('%s%s\n'%(' '*8,new_line))
                            #写入：server 1.1.1.1 1.1.1.1 weight 10 maxconn 3000
                        has_write = True    #标记已经写了
        if os.path.exists(bak_file):
            os.remove(bak_file)
        os.rename(filename,bak_file)
        os.rename(new_file,filename)

#1 查询：  www.oldboy.org
def fetch(data):
    #www.oldboy.com
    backend_data = "backend %s"%data    #拼接backend www.oldboy.org字符串
    res = file_handle('haproxy',backend_data,type='fetch')
#2 添加：{'backend':'www.oldboy.org','record':{'server':'1.1.1.4','weight':20,'maxconn':30,},}
def add(data):
    '''
    backend www.oldboy.org
        server 1.1.1.1 1.1.1.1 weight 10 maxconn 3000
    '''
    backend = data['backend']   #www.oldboy.org

    record_list = fetch(backend)    #寻找www.oldboy.org内容条目
    backend_data = "backend %s"%backend     #backend www.oldboy.org
    # server 1.1.1.1 1.1.1.1 weight 10 maxconn 3000
    current_data = "server %s %s weight %s maxconn %s"%(data['record']['server'],
                                                           data['record']['server'],
                                                           data['record']['weight'],
                                                           data['record']['maxconn'])
    if not record_list:         #能够找到www.oldboy.org条目
        record_list.append(backend_data)    #backend_data=backend www.oldboy.org
        record_list.append(current_data)
        #current_data=server 1.1.1.1 1.1.1.1 weight 10 maxconn 3000
        file_handle('haproxy',backend_data,record_list,type='append')
    else:
        record_list.insert(0,backend_data)
        if current_data not in record_list:
            record_list.append(current_data)
        file_handle('haproxy',backend_data,record_list,type='change')
#3 删除： {'backend':'www.oldboy.org','record':{'server':'1.1.1.4','weight':20,'maxconn':30,},}
def remove(data):
    backend = data['backend']
    record_list = fetch(backend)
    backend = data['backend']

    record_list = fetch(backend)

    current_data = "server %s %s weight %s maxconn %s"%(data['record']['server'],
                                                           data['record']['server'],
                                                           data['record']['weight'],
                                                           data['record']['maxconn'])
    backend_data = "backend %s"%backend
    print(record_list)
    if not record_list or current_data not in record_list:
        print('\033[33;1m无这条记录\033[0m')
        return
    else:
        record_list.insert(0,backend_data)
        record_list.remove(current_data)
        file_handle('haproxy',backend_data,record_list,type='change')

#4 修改：
def change(data):
    backend = data[0]['backend']
    record_list = fetch(backend)
    old_data = "server %s %s weight %s maxconn %s"%(data[0]['record']['server'],\
                                                           data[0]['record']['server'],\
                                                           data[0]['record']['weight'],\
                                                           data[0]['record']['maxconn'])
    new_data = "server %s %s weight %s maxconn %s"%(data[1]['record']['server'],\
                                                           data[1]['record']['server'],\
                                                           data[1]['record']['weight'],\
                                                           data[1]['record']['maxconn'])
    backend_data = "backend %s"%backend
    if not record_list or old_data not in record_list:
        print('\033[33;1m无此内容\033[0m')
        return
    else:
        record_list.insert(0,backend_data)
        index = record_list.index(old_data)
        record_list[index]=new_data
        file_handle('haproxy',backend_data,record_list,type='change')
if __name__ == '__main__':
    msg = '''
    1: 查询
    2：添加
    3：删除
    4：修改
    5：退出
    '''
    menu_dic = {
        '1':fetch,
        '2':add,
        '3':remove,
        '4':change,
        '5':exit,
    }
    while True:
        print(msg)
        choice = input('操作>>:').strip()
        if len(choice)==0 or choice not in menu_dic:continue
        if choice == '5':break

        data = input('数据>>:').strip()
        if choice !='1':
            data = eval(data)
        menu_dic[choice](data)

