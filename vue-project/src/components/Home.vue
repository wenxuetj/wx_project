<template>
  <el-container class="container">
    <el-header class="header">
      <el-row class="header-row">
        <el-col :span="8" class="title"><span>接口监控平台</span></el-col>
        <el-col :span="16" class="user"></el-col>
      </el-row>
    </el-header>
    <el-container>
      <el-aside width="15%" class="aside-menu">
        <el-menu :default-active="$route.path"
                 class="ele-menu"
                 router=true
                 @open="openHandler"
                 @close="closeHandler"
                 background-color="white"
                 text-color="gray"
                 active-text-color="#ffd04b">
          <template v-for="(menu,i) in $router.options.routes" v-if="menu.name === 'home'">
            <template v-for="(item,index) in menu.children">
              <el-submenu :index="index+''" v-if="!item.leaf">
                <template slot="title">
                  <i :class="item.iconCls"></i>
                  <span>{{item.name}}</span>
                </template>
                <el-menu-item v-for="child in item.children" :index="child.path" :key="child.path" @click="$router.push(child.path)"><i :class="child.iconCls"></i>{{child.name}}</el-menu-item>
              </el-submenu>
              <el-menu-item v-if="item.leaf" :index="item.path" @click="$router.push(item.path)"><i :class="item.iconCls"></i>{{item.name}}</el-menu-item>
            </template>
          </template>
        </el-menu>
      </el-aside>
      <el-main>
        <section>
          <el-col :span="24">
            <div class="main-container">
              <router-view></router-view>
            </div>
          </el-col>
        </section>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
  export default {
    name: 'home',
    data () {
      return {
        name: 'wenxue',
        menus: []
      }
    },
    methods:{
      openHandler() {

      },
      closeHandler() {

      }
    }
    /**,
    created(){
      var routes = $router.options.routes;
      for(var i =0;i < routes.length; i++){
        if(routes[i].name === 'home'){
          menus: routes[i].children;
        }
      }
    }**/
  }
</script>

<style scoped lang="scss">

  body{
    margin: 0px;
    padding: 0px;
    font-size: 14px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    height: 100%;
    overflow: hidden;
  }
  .container {
    overflow: hidden;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;

  }
  .header {
    background-color: rgb(84, 92, 100);
    font-color:white;
  }
  .header .logo{
    height: 60px;
    /*background-image: url("../assets/logo.png");*/
  }
  .header .title{
    height: 60px;
    line-height: 60px;
    font-size: 24px;
  }
  .header-row{

  }
  .ele-menu{
    border-right: 0px;
  }
  .aside-menu{
    border-right: 1px solid #e6e6e6;
  }
  .main-container{
    min-height: 35em;
    height: 35em;
    overflow-y: auto;
    overflow-x: hidden;
  }
</style>
