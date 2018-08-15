import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/components/Home'
import Monitor from '@/components/realMonitor/Monitor'
import Alarm from '@/components/alarm/Alarm'
import InvokeLog from '@/components/invokeLogs/InvokeLog'
import SysConfig from '@/components/sysConfig/SysConfig'
import SysInfo from '@/components/sysConfig/SysInfo'
import RecMonitor from '@/components/recMonitor/RecMonitor'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/login',
      hidden: true
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      hidden: true
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      hidden: true,
      leaf: false,
      children: [
        {
          path: '/home/realMonitor',
          component: Monitor,
          name: '实时监控',
          iconCls: 'el-icon-service',
          hidden: false,
          leaf: true
        },
        {
          path: '/home/alarm',
          component: Alarm,
          name: '告警信息',
          iconCls: 'el-icon-bell',
          hidden: false,
          leaf: true
        },
        {
          path: '/home/invokeLogs',
          component: InvokeLog,
          name: '接口日志',
          iconCls: 'el-icon-tickets',
          hidden: false,
          leaf: true
        },
        {
          path: '/home/recMonitor',
          component: RecMonitor,
          name: '案件监控',
          iconCls: 'el-icon-view',
          hidden: false,
          leaf: true
        },
        {
          path: '/home/SysConfig',
          component: SysConfig,
          name: '系统设置',
          iconCls: 'el-icon-setting',
          hidden: false,
          leaf: false,
          children: [
            {path: '/home/SysConfig/sysInfo', component: SysInfo, iconCls: 'el-icon-view', name: '平台配置', leaf: true}
          ]
        }
      ]
    }
    /**,
    {
      path: 'home/realMonitor',
      component: Monitor,
      name: '实时监控',
      iconCls: 'el-icon-service',
      hidden: false,
      leaf: true
    },
    {
      path: 'home/alarm',
      component: Alarm,
      name: '告警信息',
      iconCls: 'el-icon-bell',
      hidden: false,
      leaf: true
    },
    {
      path: 'home/invokeLogs',
      component: InvokeLog,
      name: '接口日志',
      iconCls: 'el-icon-tickets',
      hidden: false,
      leaf: true
    },
    {
      path: 'home/recMonitor',
      component: RecMonitor,
      name: '案件监控',
      iconCls: 'el-icon-view',
      hidden: false,
      leaf: true
    },
    {
      path: 'home/SysConfig',
      component: SysConfig,
      name: '系统设置',
      iconCls: 'el-icon-setting',
      hidden: false,
      leaf: false,
      children: [
        {path: 'home/sysInfo', component: SysInfo, iconCls: 'el-icon-view', name: '平台配置', leaf: true}
      ]
    }*/
  ]
})
