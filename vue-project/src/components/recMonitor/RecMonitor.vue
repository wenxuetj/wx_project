<template>
  <el-tabs v-model="defaultActiveTab">
    <el-tab-pane label="示范区" name="sfService">
      <el-row :gutter="30">
        <el-col :span="11"><Echarts :option="option" :style="style"></Echarts></el-col>
        <el-col :span="11"><Echarts :option="option1" :style="style"></Echarts></el-col>
        <el-col :span="11"><Echarts :option="option2" :style="style"></Echarts></el-col>
        <el-col :span="11"><Echarts :option="option3" :style="style"></Echarts></el-col>
      </el-row>
    </el-tab-pane>
    <el-tab-pane label="睢阳区" name="syService">
      <el-row :gutter="30">
        <el-col :span="11"><Echarts :option="option4" :style="style1"></Echarts></el-col>
        <el-col :span="11"><Echarts :option="option5" :style="style1"></Echarts></el-col>
      </el-row>
    </el-tab-pane>
    <el-tab-pane label="梨园区" name="lyService">
      <el-row :gutter="30">
        <el-col :span="11"><Echarts :option="option4" :style="style1"></Echarts></el-col>
        <el-col :span="11"><Echarts :option="option5" :style="style1"></Echarts></el-col>
      </el-row>
    </el-tab-pane>
  </el-tabs>

</template>

<script>
  import Echarts from 'vue-echarts-v3/src/full.js';
  export default {
    name: 'view',
    components: {
      Echarts
    },
    props: {
    },
    data: () => ({
      defaultActiveTab:'sfService',
      loading: true,
      style: {
        width:'100%',
        height: '300px'
      },
      style1: {
        width:'100%',
        height: '300px'
      },
      option: {
        title: {
          text: ''
        },
        tooltip: {
          show: true
        },
        legend: {
          data:['案件下派']
        },
        xAxis: {
          type: 'category',
          data: ['应执行', '成功', '待执行', '失败']
        },
        yAxis: {},
        series: [{
          name:"案件下派",
          type: 'bar',
          data: [124, 120, 32, 18],
          color: ['#2d8cf0'],
          itemStyle:{
            normal:{
              label:{
                show:true,
                textStyle: {
                  fontSize : '12',
                  color: '#fff',
                  fontFamily : '微软雅黑',
                }
              }
            }
          }
        }]
      },
      option1: {
        title: {
          text: ''
        },
        tooltip: {
          show: true
        },
        legend: {
          data:['核查反馈']
        },
        xAxis: {
          type: 'category',
          data: ['应执行', '成功', '待执行', '失败']
        },
        yAxis: {},
        series: [{
          name: '核查反馈',
          type: 'bar',
          data: [324, 232, 12, 2],
          color: ['#2d8cf0'],
          itemStyle:{
            normal:{
              label:{
                show:true,
                textStyle: {
                  fontSize : '12',
                  color: '#fff',
                  fontFamily : '微软雅黑',
                }
              }
            }
          }
        }]
      },
      option2: {
        title: {
          text: ''
        },
        tooltip: {
          show: true
        },
        legend: {
          data:['申请回退']
        },
        xAxis: {
          type: 'category',
          data: ['应执行', '成功', '待执行', '失败']
        },
        yAxis: {},
        series: [{
          name: '申请回退',
          type: 'bar',
          data: [124, 312, 12, 2],
          color: ['#2d8cf0'],
          itemStyle:{
            normal:{
              label:{
                show:true,
                textStyle: {
                  fontSize : '12',
                  color: '#fff',
                  fontFamily : '微软雅黑',
                }
              }
            }
          }
        }]
      },
      option3: {
        title: {
          text: ''
        },
        tooltip: {
          show: true
        },
        legend: {
          data:['结案接口']
        },
        xAxis: {
          type: 'category',
          data: ['应执行', '成功', '待执行', '失败']
        },
        yAxis: {},
        series: [{
          name: '结案接口',
          type: 'bar',
          data: [289, 280, 10, 2],
          color: ['#2d8cf0'],
          itemStyle:{
            normal:{
              label:{
                show:true,
                textStyle: {
                  fontSize : '12',
                  color: '#fff',
                  fontFamily : '微软雅黑',
                }
              }
            }
          }
        }]
      },
      option4: {
        title: {
          text: ''
        },
        tooltip: {
          show: true
        },
        legend: {
          data:['回退审批']
        },
        xAxis: {
          type: 'category',
          data: ['应执行', '成功', '待执行', '失败']
        },
        yAxis: {},
        series: [{
          name: '回退审批',
          type: 'bar',
          data: [289, 280, 10, 2],
          color: ['#2d8cf0'],
          itemStyle:{
            normal:{
              label:{
                show:true,
                textStyle: {
                  fontSize : '12',
                  color: '#fff',
                  fontFamily : '微软雅黑',
                }
              }
            }
          }
        }]
      },
      option5: {
        title: {
          text: ''
        },
        tooltip: {
          show: true
        },
        legend: {
          data:['延期审批']
        },
        xAxis: {
          type: 'category',
          data: ['应执行', '成功', '待执行', '失败']
        },
        yAxis: {},
        series: [{
          name: '延期审批',
          type: 'bar',
          data: [289, 280, 10, 2],
          color: ['#2d8cf0'],
          itemStyle:{
            normal:{
              label:{
                show:true,
                textStyle: {
                  fontSize : '12',
                  color: '#fff',
                  fontFamily : '微软雅黑',
                }
              }
            }
          }
        }]
      },
    }),
    methods: {
      query: function () {
        var _this = this;
        this.$axios.get('/monitor/api/invokestate/list',{}).then(
          function (res) {

          },
          function (res) {

          }
        );
      }
    }
  }
</script>

<style scoped>

</style>
