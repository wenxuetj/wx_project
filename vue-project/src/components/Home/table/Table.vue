<template>
  <section>
    <el-col :span="24">
      <el-form :inline=true :model="searchForm">
        <el-form-item label="部门名称">
          <el-input size="mini" type="text" v-model="searchForm.unitName"></el-input>
        </el-form-item>
        <el-form-item label="部门领导">
          <el-input size="mini" v-model="searchForm.unitLeader"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" size="mini" @click.native.prevent="query">查询</el-button>
            <el-button type="warning" size="mini" @click.native.prevent="add">新增</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    <el-table border :data="unitPageInfo.unitList" highlight-current-row style="width: 100%;" v-loading="listLoading" max-height="420" size="mini">
      <el-table-column width="150" align="center" fixed prop="unitId" label="部门ID"></el-table-column>
      <el-table-column width="200" align="center" fixed prop="unitName" label="部门名称"></el-table-column>
      <el-table-column width="200" align="center" prop="unitTypeName" label="部门类型"></el-table-column>
      <el-table-column width="200" align="center" prop="unitAttrName" label="部门属性"></el-table-column>
      <el-table-column width="400" align="center" prop="unitDesc" label="部门描述"></el-table-column>
      <el-table-column width="200" align="center" prop="createTime" label="创建时间"></el-table-column>
      <el-table-column width="100" align="center" fixed="right" label="操作">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="editUnit(scope.$index,scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="delUnit(scope.$index,scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-col :span="24">
      <el-pagination layout="prev, pager, next" background @current-change="handleCurrentChange"
                     :page-size="size" style="float:right" :total="unitPageInfo.unitTotal">
      </el-pagination>
    </el-col>
    <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false" width="35%">
      <el-form size="mini" :model="eUnitForm" :rules="eUnitFormRules" ref="eUnitForm" label-width="20%">
        <el-form-item label="部门名称" prop="unitName">
          <el-input v-model="eUnitForm.unitName" clearable></el-input>
        </el-form-item>
        <el-form-item label="上级部门" prop="unitSeniorName">
          <el-input v-model="eUnitForm.unitSeniorName" placeholder="请选择上级部门"
                    readonly="readonly" suffix-icon="el-icon-arrow-down" @click.native="isSelectShow = !isSelectShow"></el-input>
          <el-tree class="dropdown-tree" v-if="isSelectShow" :props="treeProps" :lazy="false"
                   empty-text="暂无数据" :load="loadTreeNode" :data="unitTreeList">

          </el-tree>
        </el-form-item>
        <el-form-item label="部门性质" prop="unitAttrName">
          <el-select v-model="eUnitForm.unitAttrName" class="select-max">
            <el-option label="直属部门" value="直属部门"></el-option>
            <el-option label="一级部门" value="一级部门"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="部门类型" prop="unitTypeName">
          <el-select label="部门类型" v-model="eUnitForm.unitTypeName" class="select-max">
            <el-option label="政府单位" value="政府单位"></el-option>
            <el-option label="事业单位" value="事业单位"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="创建时间">
          <el-date-picker v-model="eUnitForm.createTime" type="datetime"
                          placeholder="请选择日期时间" class="input-max">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="部门描述">
            <el-input type="textarea" v-model="eUnitForm.unitDesc" style="width:100%"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button @click="saveUnit" type="primary">保存</el-button>
        </el-form-item>

      </el-form>
    </el-dialog>
  </section>

</template>

<script>
    export default {
        data() {
          return {
            searchForm: {
              unitName: '',
              unitLeader: ''
            },
            unitPageInfo: {
              unitList: [],
              unitTotal: 0
            },
            page: 0,
            size: 10,
            unitId: 1,
            listLoading: true,
            eUnitForm: {
              unitName: '',
              unitAttrName: '',
              unitTypeName: '',
              unitDesc: '',
              createDate: '',
              createTime: '',
              unitSeniorId: '',
              unitSeniorName: ''
            },
            editFormVisible: false,
            eUnitFormRules: {
              unitName: [{required: true, message: '请输入部门名称', trigger: blur}],
              unitSeniorName: [{required: true, message: '请选择上级部门', trigger: blur}],
              unitAttrName: [{required: true, message: '请选择部门性质',trigger: blur}],
              unitTypeName: [{required: true,message: '请输入部门类型',trigger: blur}],
              createTime: [{required: true,message: '请输入创建时间',trigger: blur}]
            },
            aUnitForm: {
              unitName: '',
              unitAttrName: '',
              unitTypeName: '',
              unitDesc: ''
            },
            labelWidth: '80px',
            //上级部门下拉框树
            isSelectShow: false,
            unitTreeList: [{
              id: 1,
              label: '一级 1',
              children: [{
                id: 4,
                label: '二级 1-1',
                children: [{
                  id: 9,
                  label: '三级 1-1-1'
                }, {
                  id: 10,
                  label: '三级 1-1-2'
                }]
              }]
            }, {
              id: 2,
              label: '一级 2',
              children: [{
                id: 5,
                label: '二级 2-1'
              }, {
                id: 6,
                label: '二级 2-2'
              }]
            }, {
              id: 3,
              label: '一级 3',
              children: [{
                id: 7,
                label: '二级 3-1'
              }, {
                id: 8,
                label: '二级 3-2'
              }]
            }],
            treeProps: {
              id: 'id',
              label:'label',
              children:'children'
            }

          }
        },
        methods: {
          loadTreeNode:function () {
            var _this = this;
            this.$axios.get('api/unit/getunittree',{treeID:1}).then(
              function (res) {
                //unitTreeList = res.data.data.treeList;
                //return res.data;
              },
              function (res) {
                var data = res.data;
                this.$message.error(data.message);
              }
            )
          },
          //查询
          query:function () {
            this.page = 0;
            this.getUnitList();
          },
          //清空查询条件
          clear:function () {

          },
          //分页跳转
          handleCurrentChange(val) {
            this.page = val>1?val-1:0;
            this.getUnitList();
          },
          //查询部门分页列表处置
          getUnitList() {
            var _this = this;
            var params = {
              page: this.page,
              size: this.size,
              unitId: this.unitId
            };
            this.$axios.post('/api/unit/getunitlist',params).then(
              function (res) {
                _this.listLoading = false;
                var data = res.data;
                _this.unitPageInfo.unitList = data.rows;
                _this.unitPageInfo.unitTotal = data.total;
              }).catch(
                function (data) {
                _this.$message('查询部门列表发生异常！');
            });
          },
          //编辑部门表单
          editUnit : function (index,row) {
            this.editFormVisible = true;
            this.eUnitForm = Object.assign({}, row);
          },
          //删除部门
          delUnit: function (index,row) {

          }
        },
        mounted() {
          this.getUnitList();
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
