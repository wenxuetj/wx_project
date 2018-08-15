<template>
    <el-form model="loginFrom" rules="rules" ref="loginForm" label-position="left" class="login-contranier">
      <h3 class="title">系统登录</h3>
      <el-form-item prop="userName">
          <el-input type="text" v-model="loginForm.userName" placeholder="账号"></el-input>
      </el-form-item>
      <el-form-item prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="密码"></el-input>
      </el-form-item>
      <el-checkbox v-model="checked">记住密码</el-checkbox>
      <el-form-item>
          <el-button type="primary" style="width:45%;" @click.native.prevent="loginAction">登录</el-button>
          <el-button type="warning" style="width:45%;" @click.native.prevent="resetForm">取消</el-button>
      </el-form-item>
    </el-form>
</template>

<script>

  export default {
    data () {
            return {
                isLogining : false,
                loginForm:{
                    userName: '',
                    password: ''
                },
                rules : {
                    userName:[
                      {required:true, message:'请输入账号', trigger:'blur'}
                    ],
                    password:[
                      {required:true, message:'密码不能为空', trigger:'blur'}
                    ]
                },
                checked:true
          }
        },
        methods: {
            resetForm() {
                this.$refs.loginForm.resetFields();
            },
            loginAction() {
                var lp = {
                    userName: this.loginForm.userName,
                    password: this.loginForm.password
                };
                var _this = this;
                _this.$router.push({path: '/home'});
                // this.$axios.get('/monitor/loginHandler', lp).then(function (data) {
                //     var res = data.data;
                //     if(res.success == true){
                //         _this.$router.push({path: '/home'});
                //     }
                // }).catch(function (data) {
                //     _this.$message('请求异常！');
                // })
            }
        }
    }
</script>

<style lang="scss" scoped>
  .login-contranier{
    padding:3%;
    width: 25%;
    margin:0 auto;
    border:1px solid #eaeaea;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #eaeaea;
  }

</style>
