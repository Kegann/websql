<template>
  <div class="register-container">
    <h3>注册</h3>
    <div class="register-form">
      <el-form :model="register_form" ref="register_form" :rules="rules">
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="register_form.username"
            placeholder="请输入1~20个字符"
            ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="passwd">
          <el-input
            v-model="register_form.passwd"
            placeholder="请输入1~20个字符或数字"
            ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submit_form('register_form')">
            注册
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { Message } from 'element-ui'

  export default{
    data() {
      return {
        register_form: {
          username: "",
          passwd: "",
        },
        rules: {
          username: [
            { required: true, message: "请输入要注册的用户名", trigger: 'blur'},
            { min:1, max: 20, message: "长度1~20的字符", trigger: 'blur'}
          ],
          passwd: [
            { required: true, message: "请输入密码", trigger: 'blur'},
            { min:1, max: 20, message: "长度1~20的字符或数字", trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      submit_form(form) {
        this.$refs[form].validate((valid) => {
          if (valid) {
            console.log("valid...", form);
            var path="/auth/user";
            this.$axios.post(path, {
              user: this.register_form.username,
              pwd: this.register_form.passwd
            }).then( (response) => {
              Message({
                type: "success",
                message: "Register succeed!",
                duration: 1 * 1000
              });
              this.$store.dispatch('SetUserInfo');
              this.$router.push({ path: '/' });
            })
          }
        })
      }
    }
  }
</script>

<style lang="less">
.register-container {
  margin: 10px;
  text-align: left;
  padding: 20px;
  max-width: 33%;
  .el-form {
    width: 60%;
    font-size: 16px;
    min-width: 300px;
  }
}
</style>
