# -*- coding:utf-8 -*-
import logging
import json
import requests
import traceback
#import xlsxwriter
from io import BytesIO
import os
import uuid
#from PIL import Image
import setting
import time
import datetime
from ftplib import FTP
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%b-%d %H:%M:%S',
                filename='log.txt',
                filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s:%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

engine = create_engine(setting.db_conn_str)
stat_db = create_engine(setting.stat_conn_str)

def gen_xlsx(data, day_str):
    '''
    data = [{'task_num':"201712250154",
             'event_src_name':"监督员上报",
             'sub_type_name':"测试小类",
             'address':"测试地址",
             'event_desc':"测试描述",
             'inst_time':"2017-12-28 00:30:00",
             'dispose_limit':"4小时",
             'archive_time':"2017-12-28 00:30:00",
             'event_state_name':"办结",
             'report_medias':[{'media_path':"MediaRoot/rec",
                'media_name':"1287740113521.jpg"}
             ],
             'check_medias':[{'media_path':"MediaRoot/rec",
                'media_name':"1287740113521.jpg"}
             ]}]
    day_str = '2017-12-28'
    '''
    try:
        logging.info('开始导出'+day_str+'数据')
        ftp = ftpLogin()
        file = 'stat'+os.path.sep+day_str+".xlsx"
        workbook = xlsxwriter.Workbook(file)
        sheet = workbook.add_worksheet('查询结果')
        #border：边框，align:对齐方式，bg_color：背景颜色，font_size：字体大小，bold：字体加粗
        row1_style = workbook.add_format({'border':1,'align':'center','bg_color':'cccccc','font_size':12,'bold':True})
        sheet.merge_range(0,0,0,13,'查询结果',row1_style)
        row2_style = workbook.add_format({'border':1,'align':'center','bg_color':'dddddd','font_size':10,'bold':True})
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.merge_range(1,0,1,13,'完成时间:'+now_str,row2_style)
        sheet.write(2,0,'案件编号',row2_style)
        sheet.write(2,1,'问题来源',row2_style)
        sheet.write(2,2,'案件小类',row2_style)
        sheet.write(2,3,'案件地点',row2_style)
        sheet.write(2,4,'案件描述',row2_style)
        sheet.write(2,5,'立案时间',row2_style)
        sheet.write(2,6,'处置时限',row2_style)
        sheet.write(2,7,'完成时间',row2_style)
        sheet.write(2,8,'处置结果',row2_style)
        sheet.merge_range(2,9,2,11,'处置前图片',row2_style)
        sheet.merge_range(2,12,2,13,'处置后图片',row2_style)
        #row height col width
        sheet.set_row(0,15)
        sheet.set_column(0,0,22)
        sheet.set_column(1,1,17)
        sheet.set_column(2,2,20)
        sheet.set_column(3,3,90)
        sheet.set_column(4,4,120)
        sheet.set_column(5,5,32)
        sheet.set_column(6,6,15)
        sheet.set_column(7,7,32)
        sheet.set_column(8,8,15)
        sheet.set_column(9,9,35)
        sheet.set_column(10,10,35)
        sheet.set_column(11,11,35)
        sheet.set_column(12,12,35)
        sheet.set_column(13,13,35)
        
        data_style = workbook.add_format({'border':1,'align':'left','font_size':15})
        data_row_index = 3
        for item in data:
            sheet.set_row(data_row_index,127)
            sheet.write(data_row_index,0,item.get('task_num'),data_style)
            sheet.write(data_row_index,1,item.get('event_src_name'),data_style)
            sheet.write(data_row_index,2,item.get('sub_type_name'),data_style)
            sheet.write(data_row_index,3,item.get('address'),data_style)
            sheet.write(data_row_index,4,item.get('event_desc'),data_style)
            sheet.write(data_row_index,5,item.get('inst_time'),data_style)
            sheet.write(data_row_index,6,item.get('dispose_limit'),data_style)
            sheet.write(data_row_index,7,item.get('archive_time'),data_style)
            sheet.write(data_row_index,8,item.get('event_state_name'),data_style)
            #插入上报图片
            report_medias = item.get('report_medias')
            col_index = 9
            for media in report_medias:
                if col_index>11:
                    break
                media_url = setting.http_server+'/'+media['media_path']+'/'+media['media_name']
                pic = requests.get(media_url)
                if pic.status_code==200:
                    img = Image.open(BytesIO(pic.content))
                    newSize = (int(img.size[0]*setting.compression_ratio), int(img.size[1]*setting.compression_ratio))
                    out = img.resize(newSize,Image.ANTIALIAS)
                    localpath = 'temp/'+str(uuid.uuid1())+'.png'
                    out.save(localpath, 'jpeg')
                    col_w = 35
                    x_scale = (col_w/4.62) / ( newSize[0] / 37.7928949)* 0.89
                    row_h = 127
                    y_scale = (row_h/28.54) / ( newSize[1] / 37.796)
                    sheet.insert_image(data_row_index,col_index,localpath, {'positioning': 1,'x_scale':  x_scale,'y_scale':  y_scale})
                    col_index = col_index + 1
            #插入核查图片
            check_medias = item.get('check_medias')
            col_index = 12
            for media in check_medias:
                if col_index>13:
                    break
                media_url = setting.http_server+'/'+media['media_path']+'/'+media['media_name']
                pic = requests.get(media_url)
                if pic.status_code==200:
                    img = Image.open(BytesIO(pic.content))
                    newSize = (int(img.size[0]*setting.compression_ratio), int(img.size[1]*setting.compression_ratio))
                    out = img.resize(newSize,Image.ANTIALIAS)
                    localpath = 'temp/'+str(uuid.uuid1())+'.png'
                    out.save(localpath, 'jpeg')
                    col_w = 35
                    x_scale = (col_w/4.62) / ( newSize[0] / 37.7928949)* 0.89
                    row_h = 127
                    y_scale = (row_h/28.54) / ( newSize[1] / 37.796)
                    sheet.insert_image(data_row_index,col_index,localpath, {'positioning': 1,'x_scale':  x_scale,'y_scale':  y_scale})
                    col_index = col_index + 1
            data_row_index = data_row_index+1 
            logging.info("导出----"+str(data_row_index-3)+"----条记录")
        workbook.close()
        rmdir('temp')
        filename = day_str + '.xlsx'
        xlsxData = {}
        xlsxData['create_time'] = datetime.datetime.now()
        xlsxData['media_name'] = filename
        xlsxData['media_path'] = setting.ftp_dir
        xlsxData['relation_id'] = int(day_str.replace('-',''))
        xlsxData['relation_type_id'] = 9999
        xlsxData['store_type_id'] = 3
        xlsxData['relation_main_id'] = len(data)
        xlsxData['relation_sub_id'] = os.path.getsize(file)/float(1024)
        insert_to_db(xlsxData)
        upload(ftp,file,filename)
        logging.info("执行完毕--------------------")
    except Exception as e:
        logging.error(traceback.format_exc())   

    
def get_media_report(task_num):
    sql = '''select * from dlhist.to_his_media a where relation_type_id=1 and media_type='IMAGE' and media_usage='上报' 
                   and relation_id in (select rec_id from dlhist.to_his_rec where task_num='{0}')'''.format(task_num)
    rp = engine.execute(sql)
    rows = rp.fetchall()
    return rows

def get_media_check(task_num):
    sql = '''select * from dlhist.to_his_media a where relation_type_id=1 and media_type='IMAGE' and media_usage='核查' 
                   and relation_id in (select rec_id from dlhist.to_his_rec where task_num='{0}')'''.format(task_num)
    rp = engine.execute(sql)
    rows = rp.fetchall()
    return rows

def insert_to_db(data):
    sql = '''insert into dlmis.to_media(media_id,create_time,media_name,media_path,relation_type_id,relation_id,store_type_id,relation_main_id,relation_sub_id)
                values(:media_id,:create_time,:media_name,:media_path,:relation_type_id,:relation_id,:store_type_id,:relation_main_id,:relation_sub_id)'''
    seq_sql = ''' select dlmis.so_media.nextval as id from dual '''
    rp1 = engine.execute(text(seq_sql))
    new_id = rp1.fetchone()[0]
    data["media_id"] = new_id
    rp = engine.execute(text(sql),data)

def gen_xlsx_1ately():
    now = datetime.datetime.now()
    begin_time = now + datetime.timedelta(days=-30)
    toDay_id = int(now.strftime('%Y%m%d'))
    beginDay_id = int(begin_time.strftime('%Y%m%d'))
    sql = '''select * from dlmis.to_media a where relation_type_id=9999 and relation_id < {0} and relation_id > {1}'''.format(toDay_id,beginDay_id)
    rp = engine.execute(sql)
    rows = rp.fetchall()
    id_list = [row['relation_id'] for row in rows]
    while  beginDay_id < toDay_id:
        if beginDay_id not in id_list:
            temp_str = str(beginDay_id)
            day_str = temp_str[0:4]+"-"+temp_str[4:6]+"-"+temp_str[6:]
            begin = day_str+' 00:00:00'
            end = day_str+' 23:59:59'
            sql = '''select task_num,event_src_name, sub_type_name,address,event_desc,
                to_char(INST_TIME,'yyyy-mm-dd hh24:mi:ss') as inst_time,dispose_limit,
                to_char(ARCHIVE_TIME,'yyyy-mm-dd hh24:mi:ss') as archive_time,event_state_name
                 from UMSTAT.TO_STAT_INFO  where archive_time between to_date('{0}','yyyy-mm-dd hh24:mi:ss') and to_date('{1}','yyyy-mm-dd hh24:mi:ss') '''.format(begin,end)
            rp = stat_db.execute(sql)
            rows = rp.fetchall()
            for row in rows:
                report_medias = get_media_report(row.get('task_num'))
                row["report_medias"] = report_medias
                check_medias = get_media_check(item.get('task_num'))
                row["check_medias"] = check_medias
            gen_xlsx(rows,day_str)
            begin_time = begin_time + datetime.timedelta(days=1)
            beginDay_id = int(begin_time.strftime('%Y%m%d'))
            
def gen_xlsx_yesterday():
    now = datetime.datetime.now()
    yes_time = now + datetime.timedelta(days=-1)
    yes_time_str = yes_time.strftime('%Y-%m-%d')
    begin = yes_time_str+' 00:00:00'
    end = yes_time_str+' 23:59:59'
    sql = '''select task_num,event_src_name, sub_type_name,address,event_desc,
        to_char(INST_TIME,'yyyy-mm-dd hh24:mi:ss') as inst_time,dispose_limit,
        to_char(ARCHIVE_TIME,'yyyy-mm-dd hh24:mi:ss') as archive_time,event_state_name
         from UMSTAT.TO_STAT_INFO  where archive_time between to_date('{0}','yyyy-mm-dd hh24:mi:ss') and to_date('{1}','yyyy-mm-dd hh24:mi:ss') '''.format(begin,end)    
    rp = stat_db.execute(sql)
    rows = rp.fetchall()
    for row in rows:
        report_medias = get_media_report(row.get('task_num'))
        row["report_medias"] = report_medias
        check_medias = get_media_check(item.get('task_num'))
        row["check_medias"] = check_medias
    gen_xlsx(rows,yes_time_str)
    
def gen_xlsx_by_day(date_str):
    begin = date_str+' 00:00:00'
    end = date_str+' 23:59:59'
    oracle_sql = '''select task_num,event_src_name, sub_type_name,address,event_desc,
        to_char(INST_TIME,'yyyy-mm-dd hh24:mi:ss') as inst_time,dispose_limit,
        to_char(ARCHIVE_TIME,'yyyy-mm-dd hh24:mi:ss') as archive_time,event_state_name
         from UMSTAT.TO_STAT_INFO  where archive_time between to_date('{0}','yyyy-mm-dd hh24:mi:ss') and to_date('{1}','yyyy-mm-dd hh24:mi:ss') '''.format(begin,end)    
    sql = ''' select task_num,event_src_name, sub_type_name,address,event_desc,
            DATE_FORMAT(inst_time,'%Y-%m-%d %H:%i:%s') as inst_time,dispose_limit,
            DATE_FORMAT(archive_time,'%Y-%m-%d %H:%i:%s')  as archive_time,event_state_name
             from TO_STAT_INFO where  archive_time between {0} and {1}''' .format(begin,end)
    rp = stat_db.execute(sql)
    rows = rp.fetchall()
    for row in rows:
        report_medias = get_media_report(row.get('task_num'))
        row["report_medias"] = report_medias
        check_medias = get_media_check(item.get('task_num'))
        row["check_medias"] = check_medias
    gen_xlsx(rows,yes_time_str)

def ftpLogin():
    try:
        ftp = FTP()
        ftp.connect(setting.ftp_host, setting.ftp_port)    
        ftp.login(setting.ftp_user, setting.ftp_password)
        logging.info(ftp.welcome)
        return ftp
    except Exception as e:
        logging.error(traceback.format_exc())
 
def upload(ftp,file,filename):
    try:
        fp = open(file, 'rb')
        ftp.cwd(setting.ftp_dir)
        ftp.storbinary('STOR ' + filename, fp, 1024)
    except Exception as e:
        logging.error(traceback.format_exc())
  
def download(ftp,file):
    try:
        localpath = 'temp/'+str(uuid.uuid1())+'.png'
        fp = open(localpath, 'wb')
        ftp.retrbinary('RETR ' + file, fp.write, 1024)
        fp.close()
        return localpath
    except Exception as e:
        logging.error(traceback.format_exc())

def rmdir(dir):
    filelist=os.listdir(dir)
    for f in filelist:
        filepath = os.path.join( dir, f )
        if os.path.isfile(filepath):
            os.remove(filepath)
          
def test(date_str,count=10):  
    data = [{'task_num':"201712250154",
             'event_src_name':"监督员上报",
             'sub_type_name':"测试小类",
             'address':"测试地址",
             'event_desc':"测试描述",
             'inst_time':"2017-12-28 00:30:00",
             'dispose_limit':"4小时",
             'archive_time':"2017-12-28 00:30:00",
             'event_state_name':"办结",
             'report_medias':[{'media_path':"MediaRoot/rec",
                'media_name':"1287740113521.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"test1.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"200921015411111.jpg"}
             ],
             'check_medias':[
                {'media_path':"MediaRoot/rec",
                 'media_name':"1287740113521.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"test1.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"200921015411111.jpg"}
             ]},{'task_num':"201712250154",
             'event_src_name':"监督员上报",
             'sub_type_name':"测试小类",
             'address':"测试地址",
             'event_desc':"测试描述",
             'inst_time':"2017-12-28 00:30:00",
             'dispose_limit':"4小时",
             'archive_time':"2017-12-28 00:30:00",
             'event_state_name':"办结",
             'report_medias':[{'media_path':"MediaRoot/rec",
                'media_name':"1287740113521.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"test1.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"200921015411111.jpg"}
             ],
             'check_medias':[
                {'media_path':"MediaRoot/rec",
                 'media_name':"test1.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"test1.jpg"},
                {'media_path':"MediaRoot/rec",
                'media_name':"200921015411111.jpg"}
             ]}]
    a = 2
    count = count if count else 10
    while a < count:
        data.append(data[0])
        a = a+1
    gen_xlsx(data,date_str)
    
if __name__ == "__main__":
    #gen_xlsx_yesterday()
    #gen_xlsx_1ately()
    #test('2017-09-09')
    gen_xlsx_1ately()
    
