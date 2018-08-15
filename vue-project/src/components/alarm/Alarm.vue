<template>
  <section>
    <el-col :span="24">
      <el-form :inline=true :model="searchForm">
        <el-form-item label="告警时间:">
          <el-date-picker v-model="searchForm.beginTime" type="datetime" value-format="yyyy-MM-dd HH:mm:ss"
                          placeholder="请选择日期时间" size="mini">
          </el-date-picker>-
          <el-date-picker v-model="searchForm.endTime" type="datetime" value-format="yyyy-MM-dd HH:mm:ss"
                          placeholder="请选择日期时间" size="mini">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="接口类型">
          <el-select label="接口类型" v-model="searchForm.apiTypeID" size="mini">
            <el-option label="流程对接" value="1"></el-option>
            <el-option label="短信对接" value="2"></el-option>
            <el-option label="车载对接" value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="mini" @click.native.prevent="query">查询</el-button>
          <!--<el-button type="warning" size="mini" @click.native.prevent="add">新增</el-button>-->
        </el-form-item>
      </el-form>
    </el-col>
    <el-table border :data="pageInfo.list" highlight-current-row style="width: 100%;" v-loading="listLoading" max-height="420" size="mini">
      <el-table-column width="100" align="center" prop="logId" label="日志ID"></el-table-column>
      <el-table-column width="200" align="center" prop="apiTypeName" label="接口类型"></el-table-column>
      <el-table-column width="200" align="center" prop="apiName" label="接口名称"></el-table-column>
      <el-table-column width="200" align="center" prop="alarmTypeName" label="消息类型"></el-table-column>
      <el-table-column width="200" align="center" prop="alarmLevelName" label="消息类型"></el-table-column>
      <el-table-column width="200" align="center" prop="alarmContent" label="消息内容"></el-table-column>
      <el-table-column width="200" align="center" prop="alarmNotifyId" label="是否发送提醒" :formatter="notifyFormat"></el-table-column>
      <el-table-column width="200" align="center" prop="alarmNotifyTime" label="提醒发送时间" :formatter="dateFormat"></el-table-column>
      <el-table-column width="200" align="center" prop="createTime" label="创建时间" :formatter="dateFormat"></el-table-column>
    </el-table>
    <el-col :span="24">
      <el-pagination layout="prev, pager, next" background @current-change="handleCurrentChange"
                     :page-size="size" style="float:right" :total="pageInfo.total">
      </el-pagination>
    </el-col>
  </section>

</template>

<script>
  export default {
    data() {
      return {
        searchForm: {
          beginTime: '',
          endTime: '',
          apiTypeID: ''
        },
        pageInfo: {
          list: [],
          total: 0
        },
        page: 0,
        limit: 10,
        listLoading: true,


        labelWidth: '80px',
        //上级部门下拉框树
        isSelectShow: false

      }
    },

    methods: {
      //查询
      query:function () {
        this.page = 0;
        this.getLogList();
      },
      //清空查询条件
      clear:function () {

      },
      //分页跳转
      handleCurrentChange(val) {
        this.page = val>1?val-1:0;
        this.getLogList();
      },

      getLogList() {
        var _this = this;
        var params = {
          page: this.page,
          limit: this.limit,
          beginTime: this.searchForm.beginTime,
          endTime: this.searchForm.endTime,
          apiTypeID:this.searchForm.apiTypeID == ""?0:this.searchForm.apiTypeID
        };
        this.$axios.get('/monitor/api/alarmlog/list',{params:params}).then(
          function (res) {
            _this.listLoading = false;
            var data = res.data.data;
            _this.pageInfo.list = data.content;
            _this.pageInfo.total = data.totalElements;
          }).catch(
          function (data) {
            _this.$message('查询接口调用记录发生异常！');
          });
      },

      notifyFormat(row,column,cellValue) {
        return cellValue == 0 ? "否" : "是";
      },

      dateFormat(row,column,cellValue){
        if(cellValue == ""){
          return "";
        }else{
          return this.$moment(cellValue).format("YYYY-MM-DD HH:mm:ss");
        }
      }
    },
    mounted() {
      this.getLogList();
    }

  }
</script>

<style scoped lang="scss">
  .dropdown-tree{
    position: absolute;
    overflow: auto;
    z-index: 100;
    width: 100%;
    height: 200px;
    border: 1px solid #c0c4cc;
  }
  .select-max{
    width: 100%;
  }
  .input-max{
    width: 100%;
  }
</style>
