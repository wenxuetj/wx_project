<template>
  <section>
    <el-col :span="24">
      <el-form :inline=true :model="searchForm">
        <el-form-item label="接口应用">
          <el-select label="接口应用" v-model="searchForm.instanceId" size="mini" clearable>
            <el-option v-for="item in instanceOptions" :key="item.id" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="接口类型">
          <el-select label="接口类型" v-model="searchForm.apiTypeId" size="mini" clearable>
            <el-option v-for="item in apiTypeOptions" :key="item.id" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="mini" @click.native.prevent="query">查询</el-button>
          <el-button type="warning" icon="el-icon-plus" size="mini" @click.native.prevent="add">新增</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    <el-table border :data="pageInfo.list" highlight-current-row style="width: 100%;" v-loading="listLoading" max-height="420" size="mini">
      <el-table-column width="100" align="center" prop="id" label="ID"></el-table-column>
      <el-table-column width="200" align="center" prop="instanceName" label="接口应用"></el-table-column>
      <el-table-column width="200" align="center" prop="apiTypeName" label="接口类型"></el-table-column>
      <el-table-column width="100" align="center" prop="enabled" label="是否启用" :formatter="enableFormat"></el-table-column>
      <el-table-column width="100" align="center" prop="requestId" label="接口编码"></el-table-column>
      <el-table-column width="200" align="center" prop="requestMethod" label="接口名称"></el-table-column>
      <el-table-column width="400" align="center" prop="monitorUrl" label="接口地址"></el-table-column>
      <el-table-column width="100" align="center" prop="connectionTimeout" label="超时时间"></el-table-column>
      <el-table-column width="100" align="center" prop="frequency" label="连续提醒"></el-table-column>
      <el-table-column width="100" align="center" prop="threshold" label="阈值"></el-table-column>
      <el-table-column width="200" align="center" prop="email" label="邮箱" ></el-table-column>
      <el-table-column width="200" align="center" prop="mobile" label="短信"></el-table-column>
      <el-table-column width="100" align="center" fixed="right" label="操作">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="edit(scope.$index,scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="del(scope.$index,scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-col :span="24">
      <el-pagination layout="prev, pager, next" background @current-change="handleCurrentChange"
                     :page-size="size" style="float:right" :total="pageInfo.total">
      </el-pagination>
    </el-col>

    <!--编辑框-->
    <el-dialog title="编辑" :visible.sync="vDialog" :close-on-click-modal="false" width="40%">
      <el-form size="mini" :modal="configForm" :rules="configRules" ref="configForm" label-width="18%">
        <el-form-item label="接口应用" prop="instanceName">
          <el-select v-model="configForm.instanceName" class="select-max" @change="instanceChange" clearable>
            <el-option v-for="item in instanceOptions" :key="item.id" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="接口类型" prop="apiTypeName">
          <el-select v-model="configForm.apiTypeName" class="select-max" @change="apiTypeChange" clearable>
            <el-option v-for="item in apiTypeOptions" :key="item.id" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="接口编号" prop="requestId">
          <el-input v-model="configForm.requestId" clearable></el-input>
        </el-form-item>
        <el-form-item label="接口名称" prop="requestMethod">
          <el-input v-model="configForm.requestMethod" clearable></el-input>
        </el-form-item>
        <el-form-item label="接口地址" prop="monitorUrl">
          <el-input v-model="configForm.monitorUrl"></el-input>
        </el-form-item>
        <el-form-item label="是否启用" prop="enable">
          <el-switch v-model="configForm.enabled"></el-switch>
        </el-form-item>
        <el-form-item label="超时时间" prop="connectionTimeout">
          <el-slider v-model="configForm.connectionTimeout" show-input></el-slider>
        </el-form-item>
        <el-form-item label="告警阈值" prop="threshold">
          <el-slider v-model="configForm.threshold" show-input></el-slider>
        </el-form-item>
        <el-form-item label="连续提醒" prop="frequency">
          <el-slider v-model="configForm.frequency" show-input></el-slider>
        </el-form-item>
        <el-form-item label="邮箱地址" prop="email">
          <el-input v-model="configForm.email"></el-input>
        </el-form-item>
        <el-form-item label="短信号码" prop="moblie">
          <el-input v-model="configForm.mobile"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="save">确 定</el-button>
      </span>
    </el-dialog>
  </section>

</template>

<script>
  export default {
    data() {
      return {
        searchForm: {
          instanceId: '',
          apiTypeId: ''
        },
        pageInfo: {
          list: [],
          total: 0
        },
        page: 0,
        limit: 10,
        listLoading: true,

        vDialog: false,
        isEdit: false,
        configForm: {
          id: '',
          instanceId: '',
          instanceName: '',
          apiTypeId: '',
          apiTypeName: '',
          requestId: '',
          requestMethod: '',
          monitorUrl: '',
          enabled: '',
          connectionTimeout: 0,
          threshold: 0,
          frequency: 0,
          email: '',
          mobile: ''
        },
        defaultConfigForm: {
          id: '',
          instanceId: '',
          instanceName: '',
          apiTypeId: '',
          apiTypeName: '',
          requestId: '',
          requestMethod: '',
          monitorUrl: '',
          enabled: '',
          connectionTimeout: 10,
          threshold: 0,
          frequency: 0,
          email: '',
          mobile: ''
        },
        configRules:{
          instanceName: [{required: true, message: '请选择接口应用', trigger: blur}],
          apiTypeName: [{required: true, message: '请选择接口', trigger: blur}],
          requestId: [{required: true, message: '请输入接口编码', trigger: blur}],
          requestMethod: [{required: true, message: '请输入接口名称', trigger: blur}],
          monitorUrl: [{required: true, message: '请输入接口地址', trigger: blur}]
        },
        instanceOptions: [
          {id:1,name:'示范区接口应用'},
          {id:2,name:'睢阳区接口应用'},
          {id:3,name:'梨园区接口应用'}
        ],
        apiTypeOptions: [
          {id:1,name:'流程对接'},
          {id:2,name:'短信对接'},
          {id:3,name:'车载对接'}
        ],
        labelWidth: '80px'
      }
    },

    methods: {
      //查询按钮响应事件
      query:function () {
        this.page = 0;
        this.getConfigList();
      },
      //清空查询条件
      clear:function () {

      },
      //分页跳转
      handleCurrentChange(val) {
        this.page = val>1?val-1:0;
        this.getConfigList();
      },

      //执行查询
      getConfigList() {
        var _this = this;
        var params = {
          page: this.page,
          limit: this.limit,
          instanceId: this.searchForm.instanceId == ""?0:this.searchForm.instanceId,
          apiTypeID:this.searchForm.apiTypeId == ""?0:this.searchForm.apiTypeId
        };
        this.$axios.get('/monitor/api/instance/list',{params:params}).then(
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

      //新增按钮响应事件
      add: function () {
        this.vDialog = true;
        this.configForm = Object.assign({},this.defaultConfigForm);
      },

      //编辑按钮响应事件
      edit(index,row) {
        this.vDialog = true;
        Object.assign(this.configForm,row);
        this.configForm.enabled = this.configForm.enabled == "1" ? true : false;
      },

      //删除按钮响应事件
      del(index,row) {
        var _this = this;
        _this.$confirm('确认要删除该条记录吗？','提示',{
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(()=>{
          _this.$axios.post('/monitor/api/instance/delete',{id:row.id}).then(
            function (res) {
              var data = res.data;
              if(data.code == "0"){
                _this.$message("删除成功");
              }else{
                _this.$message("删除失败");
              }
              _this.query();
            },
            function (res) {
              _this.message("删除失败！");
            }
          )}
        ).catch(()=>{

        });
      },

      //保存表单内容
      save() {
        var _this = this;
        this.configForm.enabled = this.configForm.enabled === true ? 1 : 0;
        _this.$axios.post('/monitor/api/instance/save',this.configForm).then(
          function (res) {
            var data = res.data;
            if(data.code == "0"){
              _this.$message('保存配置成功！');
            }else{
              _this.$message('保存配置失败！');
            }
            _this.vDialog = false;
            _this.query();
          },
          function (res) {
            var data = res.data;
            _this.$message('保存配置异常！');
          }
        );
      },

      //select下拉框change触发事件
      instanceChange(value) {
        let obj = {};
        obj = this.instanceOptions.find((item)=>{
          return value === item.id;
        });
        this.configForm.instanceId = obj.id;
        this.configForm.instanceName = obj.name;
      },

      //select下拉框change触发事件
      apiTypeChange(value) {
        let obj = {};
        obj = this.apiTypeOptions.find((item)=>{
          return value === item.id;
        });
        this.configForm.apiTypeId = obj.id;
        this.configForm.apiTypeName = obj.name;
      },

      //表格formatter
      enableFormat(row,column,cellValue){
        return (cellValue == "0" || cellValue == "") ?"否":"是";
      },
    },
    mounted() {
      this.getConfigList();
    }
  }
</script>

<style scoped lang="scss">
  .select-max{
    width: 100%;
  }
</style>

