<template>
  <div class="Login-container">
    <div class="Login-container-form">
      <h3>用户登录</h3>
      <el-form :model="LoginForm" :rules="LoginFormRules"
      ref="LoginForm"
      class="form-container"
      >
        <el-form-item prop="username">
            <el-input
            placeholder="用户名"
            prefix-icon="el-icon-user"
            v-model="LoginForm.username"
            >
            </el-input>
            <small class="Login-Feedback"
            v-show="LoginForm.usernameError">{{LoginForm.usernameError}}</small>
        </el-form-item>
        <el-form-item prop="passwd">
            <el-input
            placeholder="密码"
            prefix-icon="el-icon-view"
            :type="pwdType"
            v-model="LoginForm.passwd"
            >
            </el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" :loading="loading" @click="submitForm('LoginForm')">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Message } from 'element-ui'

export default {
  name: 'Login',
  data() {
    return { 
      LoginForm: {
        username: "",
        passwd: "",
        usernameError: null,
        passwdError: null
      },
      LoginFormRules: {
        username: [
            { required: true, message: "请输入用户名", trigger: "blur"},
            { min: 3, max: 20, message: "请输入3-20个字符的用户名", trigger:
            "blur"}
        ],
        passwd: [
        { required: true, message: "请输入密码", trigger: "blur" },
        { min: 6, message: "密码长度至少需要6个字符", trigger: "blur"}
        ]
      },
      pwdType: 'password',
      loading: false,
    }
  },
  computed: {
    ...mapGetters([
        'userName'
    ])
  },
  methods: {
    submitForm(formName) {
        this.$refs[formName].validate((valid) => {
            if(valid) {
                this.loading = true
                var path='/auth/login';
                this.$axios.post(path, {}, {
                    auth: {
                        'username': this.LoginForm.username,
                        'password': this.LoginForm.passwd
                    }
                }).then( (response) => {
                    Message({
                        type: 'success',
                        message: 'Login Succeed!',
                        duration: 1 * 1000
                    })
                    // console.log("REPONSE: ", response)
                    this.loading = false
                    window.localStorage.setItem('websql-token', response.data.token)
                    this.$store.dispatch('SetUserInfo');
                    this.$router.push({ path: '/' });
                }).catch( (error) => {
                    // console.log("REPONSE: ", error)
                    this.loading = false;
                    if (error.response != undefined) {
                        if (error.response.status == 401) {
                            this.LoginForm.usernameError = 'Invalid username or password'
                            this.LoginForm.passwdError = error.response.msg
                        } else {
                            this.LoginForm.usernameError = "Login Failed, Unkown error"
                        }
                    }
                })
            } else {
                return false
            }
        })
    },
    showPwd() {
        if (this.pwdType === 'password'){
            this.pwdType = '';
        } else {
            this.pwdType = 'password'
        }
    }
  },
  mounted() {
    // 若已经登录，则重定向到主页面
    console.log("Username: ", this.userName)
    if (this.userName) {
        this.$router.push({ path: '/' });
    }
  }
}
</script>

<style lang="less">
.Login-container{
    height: 100%;
    //background-image: linear-gradient(141deg, #9fb8ad 0%, #1fc8db 51%, #2cb5e8 75%);
    display: flex;
    justify-content: flex-end;
    &-form {
        height: 100%;
        background-color: #E8F1F1;
        margin: 50px 200px 50px 50px;
        padding: 50px 30px;
        h3 {
            padding-bottom: 30px;
        }
        .el-input {
            width: 70%;
            font-size: 16px;
        }
        .el-button {
            width: 80%;
            font-size: 16px;
            margin-bottom: 30px;
        }
    }
}

#username, #passwd {
    border-radius: 3px;
    border: 1px solid grey;
    margin-bottom: 40px;
    line-height: 40px;
    font-size: 16px;
    &:hover {
        border: 1px solid #6DCCF8;
    }
}

.Login-Feedback {
    display: inline-block;
    color: red;
}
</style>
