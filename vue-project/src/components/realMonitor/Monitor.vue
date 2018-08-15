<template>
  <section>
    <div>
      <el-row :gutter="30">
        <el-col :span="6">
          <div class="grid-content">
            <div class="rec-num">
              <i class="el-icon-view grid-con-icon"></i>
              <div class="grid-con-num">
                <div style="font-size: 2.0em;margin-bottom: 0.2em;">1234</div>
                <div style="font-size: 1.2em;">对接案件</div>
              </div>
            </div>
            <div class="detail"><el-button type="text">点击详情</el-button></div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content">
            <div class="failure-num">
              <i class="el-icon-error grid-con-icon"></i>
              <div class="grid-con-num">
                <div style="font-size: 2.0em;margin-bottom: 0.2em;">12</div>
                <div style="font-size: 1.2em;">调用失败</div>
              </div>
            </div>
            <div class="detail"><el-button type="text">点击详情</el-button></div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content">
            <div class="exception-log">
              <i class="el-icon-document grid-con-icon"></i>
              <div class="grid-con-num">
                <div style="font-size: 2.0em;margin-bottom: 0.2em;">9</div>
                <div style="font-size: 1.2em;">异常日志</div>
              </div>
            </div>
            <div class="detail"><el-button type="text">点击详情</el-button></div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content">
            <div class="alarm-log">
              <i class="el-icon-info grid-con-icon"></i>
              <div class="grid-con-num">
                <div style="font-size: 2.0em;margin-bottom: 0.2em;">43</div>
                <div style="font-size: 1.2em;">报警信息</div>
              </div>
            </div>
            <div class="detail"><el-button type="text">点击详情</el-button></div>
          </div>
        </el-col>
      </el-row>
    </div>
    <el-collapse v-model="activeList">
      <el-collapse-item v-for="(option,index) in options" :key="index" :title="option.title" :name="option.id">
        <div class="echarts">
          <Echarts :option="option.value" :style="style"></Echarts>
        </div>
      </el-collapse-item>
    </el-collapse>
  </section>
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
      activeList:[],
      loading: true,
      style: {
        width:'900px',
        height: '260px'
      },
      options: []
    }),
    methods: {
      query: function () {
        var _this = this;
        _this.$axios.get('/monitor/api/invokestate/list',{}).then(
          function (res) {
            if(res){
              var data = res.data;
              _this.parseChartData(data);
            }
          },
          function (res) {

          }
        );
      },
      parseChartData(data) {
        var name = '';
        var id = '';
        var xAxisArr = [];
        var yAxisArr = [];
        for(var i=0,len=data.length;i<len;i++){
          if(i == 0){
            name = data[i].requestMethod;
            id = data[i].requestId;
          }
          if(name != data[i].requestMethod){
            var option =  {
              title: {
                text: ''
              },
              tooltip: {},
              xAxis: {
                type: 'category',
                data: xAxisArr
              },
              yAxis: {},
              series: [{
                name: 'value',
                type: 'line',
                data: yAxisArr
              }]
            };
            var o = {
              title:name,
              id:id,
              value:option
            }
            this.activeList.push(id);
            this.options.push(o);
            name = data[i].requestMethod;
            id = data[i].requestId;
            xAxisArr = [];
            yAxisArr = [];
          }
          xAxisArr.push(this.$moment(data[i].createTime).format("HH:mm:ss"));
          yAxisArr.push(data[i].connectTime);
          if(i+1 == len){
            var option =  {
              title: {
                text: ''
              },
              tooltip: {},
              xAxis: {
                type: 'category',
                data: xAxisArr
              },
              yAxis: {},
              series: [{
                name: 'value',
                type: 'line',
                data: yAxisArr
              }]
            };
            var o = {
              title:name,
              id:id,
              value:option
            }
            this.activeList.push(id);
            this.options.push(o);
            name = data[i].requestMethod;
            xAxisArr = [];
            yAxisArr = [];
          }
        }
      }
    },
    mounted() {
      this.query();
    }
  }
</script>

<style scoped>
  .echarts {
    width:100%;
    height:300px;
    border-top:1px solid #ebeef5;
  }
  .el-row {
    margin-bottom: 20px;
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 8em;
    overflow: hidden;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .rec-num{
    background-color: #409EFF;
    display: flex;
  }
  .failure-num{
    background-color: #E6A23C;
    display: flex;
  }
  .exception-log{
    background-color: #909399;
    display: flex;
  }
  .alarm-log{
    background-color: #F56C6C;
    display: flex;
  }
  .grid-con-icon{
    font-size:4em;
    width:40%;
    height:1.5em;
    line-height: 1.5em;
    text-align: center;
    color:#fff;
  }
  .grid-con-num{
    width:60%;
    margin-top: 1.5em;
    height:1.5em;
    line-height: 1.5em;
    color:#fff;
    text-align: center;
  }
  .detail{
    height:2em;
    width:100%;
    text-align: center;
    background-color: #f5f5f5;
  }
</style>
