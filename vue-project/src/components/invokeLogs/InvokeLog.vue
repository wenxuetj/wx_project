<template>
  <section>
    <el-col :span="24">
      <el-form :inline=true :model="searchForm">
        <el-form-item label="调用时间:">
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
      <el-table-column width="400" align="center" prop="url" label="接口地址"></el-table-column>
      <el-table-column width="200" align="center" prop="param" label="参数"></el-table-column>
      <el-table-column width="200" align="center" prop="msg" label="内容"></el-table-column>
      <el-table-column width="200" align="center" prop="startTime" label="开始时间" :formatter="dateFormat"></el-table-column>
      <el-table-column width="200" align="center" prop="endTime" label="结束时间" :formatter="dateFormat"></el-table-column>
      <el-table-column width="200" align="center" prop="createTime" label="创建时间" :formatter="dateFormat"></el-table-column>
      <!--<el-table-column width="100" align="center" fixed="right" label="操作">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="editUnit(scope.$index,scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="delUnit(scope.$index,scope.row)">删除</el-button>
        </template>
      </el-table-column>-->
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
        this.$axios.get('/monitor/api/invokelog/list',{params:params}).then(
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
