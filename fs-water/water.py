# -*- coding:utf-8 -*-
import logging
import json
import requests
import setting
import traceback
import math
import datetime
import time
import pymssql
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

#业务库数据库连接
ywkDb = create_engine(setting.sjzq_ywk_conn_str)

#获取水务局数据库连接
def get_connection():
    try:
        sw_conn = pymssql.connect(host=setting.sw_host,user=setting.sw_user,password=setting.sw_password,database=setting.sw_database)
    except Exception as e:
        error_info = traceback.format_exc()
        logging.error('''获取数据库连接失败,{0}'''.format(error_info))
    return sw_conn

#MI_RAIN_R 雨情表
def insert_mi_rain_r():
    #查询业务库中最新的一条记录插入时间
    try:
        sql = '''select count(*) from to_rain_r'''
        rp = ywkDb.execute(sql)
        count = rp.fetchone()[0]
        if count > 0:
            sql = '''select systm from to_rain_r order by systm desc limit 1'''
            rp = ywkDb.execute(sql)
            list = rp.fetchall()
            for row in list:
                systm = row[0]
        conn = get_connection() 
        cur = conn.cursor()
        if cur:
            if count == 0:
                beginTime = '2018-01-01 00:00:00'
                sql = "select stcd,tm,systm,drp from MI_RAIN_R where systm > '{0}'"
                #sql = '''select stcd,tm,systm,drp from MI_RAIN_R'''
                sql = sql.format(beginTime)
                print("sql=%s" % (sql))
                cur.execute(sql)
                list = cur.fetchall()
            else:
                str_time = systm.strftime('%Y-%m-%d %H:%M:%S')
                sql = "select stcd,tm,systm,drp from MI_RAIN_R where systm > '{0}'"
                sql = sql.format(str_time)
                print("sql=%s" % (sql))
                cur.execute(sql)
                list = cur.fetchall()
            for row in list:
                sql = '''insert into to_rain_r(stcd,tm,systm,drp) values ('{0}','{1}','{2}','{3}')'''
                sql = sql.format(row[0], row[1],row[2], row[3])
                rp = ywkDb.execute(sql)
            cur.close()
        else:
            logging.error('水务数据库连接失败')
        conn.commit()
        conn.close()
    except Exception as e:
        error_info = traceback.format_exc()
        logging.error('''雨情表同步发生异常,异常={0}'''.format(error_info))

#MI_RIVER_R 河道表
def insert_mi_river_r():
#查询业务库中最新的一条记录插入时间
    try:
        sql = '''select count(*) from to_river_r'''
        rp = ywkDb.execute(sql)
        count = rp.fetchone()[0]
        if count > 0:
            sql = '''select systm from to_river_r order by systm desc limit 1'''
            print("sql=%s" % (sql))
            rp = ywkDb.execute(sql)
            systm = rp.fetchone()[0]
        conn = get_connection()
        cur = conn.cursor()
        if cur:
            if count == 0:
                beginTime = '2018-01-01 00:00:00'
                sql = "select stcd,tm,systm,z,wptn from MI_RIVER_R WHERE systm > '{0}'"
                #sql = '''select stcd,tm,systm,z,wptn from MI_RIVER_R'''
                sql = sql.format(beginTime)
                cur.execute(sql)
                list = cur.fetchall()
            else:
                str_time = systm.strftime('%Y-%m-%d %H:%M:%S')
                sql = "select stcd,tm,systm,z,wptn from MI_RIVER_R where systm > '{0}'"
                sql = sql.format(str_time)
                print("sql=%s" % (sql))
                cur.execute(sql)
                list = cur.fetchall()
            for row in list:
                p3 = row[3]
                if p3 is None:
                    p3 = ''
                p4 = row[4]
                if p4 is None:
                    p4 = ''
                #print("stcd=%s, tm=%s,system=%s,z=%s,wptn=%s" % (row[0], row[1],row[2], row[3],row[4]))
                sql = '''insert into to_river_r(stcd,tm,systm,z,wptn) values('{0}','{1}','{2}','{3}','{4}')'''
                sql = sql.format(row[0], row[1],row[2], p3, p4)
                rp = ywkDb.execute(sql)
            cur.close()
            conn.commit()
            conn.close()
        else:
            logging.error('水务数据库连接失败')
    except Exception as e:
        error_info = traceback.format_exc()
        logging.error('''河道表同步发生异常,异常={0}'''.format(error_info))


#MI_RSVR_R水库表
def insert_mi_rsvr_r():
    #查询业务库中最新的一条记录插入时间
    try:
        sql = '''select count(*) from to_rsvr_r'''
        rp = ywkDb.execute(sql)
        count = rp.fetchone()[0]
        if count > 0:
            sql = '''select systm from to_rsvr_r order by systm desc limit 1'''
            print("sql=%s" % (sql))
            rp = ywkDb.execute(sql)
            systm = rp.fetchone()[0]
        conn = get_connection()
        cur = conn.cursor()
        if cur:
            if count == 0:
                beginTime = '2018-01-01 00:00:00'
                sql = "select stcd,tm,systm,rz from MI_RSVR_R where systm > '{0}'"
                #sql = '''select stcd,tm,systm,rz from MI_RSVR_R'''
                sql = sql.format(beginTime)
                cur.execute(sql)
                list = cur.fetchall()
            else:
                str_time = systm.strftime('%Y-%m-%d %H:%M:%S')
                sql = "select stcd,tm,systm,rz from MI_RSVR_R where systm > '{0}'"  
                sql = sql.format(str_time)
                print("sql=%s" % (sql))
                cur.execute(sql)
                list = cur.fetchall()
            for row in list:
                p3 = row[3]
                if p3 is None:
                    p3 = '' 
                sql = '''insert into to_rsvr_r(stcd,tm,systm,rz) values('{0}','{1}','{2}','{3}')'''
                sql = sql.format(row[0], row[1],row[2], p3)
                rp = ywkDb.execute(sql)
            cur.close()
        else:
            logging.error('水务数据库连接失败')
        conn.close()
    except Exception as e:
        error_info = traceback.format_exc()
        logging.error('''水库表同步发生异常,异常={0}'''.format(error_info))

#ST_STBPRP_B测站信息表
def insert_st_stbprp_b():
    #查询业务库中最新的一条记录插入时间
    try:
        sql = '''select count(*) from to_st_stbprp_b'''
        rp = ywkDb.execute(sql)
        count = rp.fetchone()[0]
        if count == 0:
            conn = get_connection()
            cur = conn.cursor()
            if cur:
                if count == 0:
                    sql = '''select stcd,stnm,lgtd,lttd,stlc,addvcd,sttp from ST_STBPRP_B'''
                    cur.execute(sql)
                    list = cur.fetchall()
                    for row in list:
                        sql = '''insert into to_st_stbprp_b(stcd,stnm,lgtd,lttd,stlc,addvcd,sttp)
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')'''
                        sql = sql.format(row[0], row[1],row[2], row[3],row[4], row[5],row[6])
                        rp = ywkDb.execute(sql)
                cur.close()
            else:
                logging.error('水务数据库连接失败')
            conn.close()
    except Exception as e:
        error_info = traceback.format_exc()
        logging.error('''测站信息表同步发生异常,异常={0}'''.format(error_info))

#执行同步操作
def run():
    while True:
        logging.info('#######同步雨情表开始########')
        insert_mi_rain_r()
        logging.info('#######同步雨情表结束########')

        logging.info('#######同步河道表开始########')
        insert_mi_river_r()
        logging.info('#######同步河道表结束########')

        logging.info('#######同步水库表开始########')
        insert_mi_rsvr_r()
        logging.info('#######同步水库表结束########')

        logging.info('#######同步测站信息开始########')
        insert_st_stbprp_b()
        logging.info('#######同步测站信息表结束########')
        # 休眠120秒
        time.sleep(setting.runIntervalTime)

if __name__ == '__main__':
    run()
#抓取操作完毕后执行相应的删除操作
        
