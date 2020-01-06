<template>
<div class="nav">
  <el-menu
    background-color="aliceblue"
    text-color="grey"
    active-text-color="steelblue"
    :default-active="$route.path"
    mode="horizontal"
    class="nav-menu"
  >
    <NavItem v-for="route in permission_routers" :key="route.name" :item="route"
    :basePath="route.path"></NavItem>
    <el-dropdown class="websql-avatar">
      <div class="avatar-wrapper">
        <span class="avatar-name">{{getName}}</span>
        <img  src="@/static/websql_user3.svg" width="40" height="40" v-if="loginFlag">
        <img  src="@/static/login.svg" width="40" height="40" v-else>
      </div>
      <div class="inverted-triangle"></div>
      <el-dropdown-menu class="websql-dropdown" slot="dropdown">
        <router-link class="inlineBlock" to="/auth/login">
          <el-dropdown-item v-if="!loginFlag">
            Login
          </el-dropdown-item>
        </router-link>
        <router-link class="inlineBlock" to="/auth/register">
          <el-dropdown-item divided v-if="!loginFlag">
            Register
          </el-dropdown-item>
        </router-link>
        <router-link class="inlineBlock" to="/auth/logout">
          <el-dropdown-item v-if="loginFlag">
            Logout
          </el-dropdown-item>
        </router-link>
      </el-dropdown-menu>
    </el-dropdown>
  </el-menu>
</div>
</template>
<script>
import {mapGetters} from 'vuex'
import NavItem from './NavItem'

export default {
  components: {
    NavItem
  },
  computed: {
    loginFlag: function() {
      if (this.$store.state.user.userName) {
        return true
      } else {
        return false
      }
    },
    getName: function() {
      if (this.$store.state.user.userName) {
        return this.$store.state.user.userName
      } else {
        return "未登录"
      }
    },
    ...mapGetters([
    'permission_routers'
  ])
  }
}
</script>

<style lang="less">
.nav {
  position: sticky;
  position: -webkit-sticky;
  top: -1px;
  z-index: 999;
  font-weight: bolder;
}
a{
  text-decoration: none
}
.nav-menu {
  display: flex;
  div:last-child {
    flex-grow: 1; //子元素中只有它可以在有空余空间时可伸缩，即它占据了剩余空间
    display: flex;
    justify-content: flex-end;
    text-align: center;
  }
  backgorund-color: steelblue;
}

.websql-avatar{
  top: 8px;
  right: 25px;
}

.avatar-name {
  font-weight: lighter;
  margin: 10px;
}

.inverted-triangle {
  width: 0;
  height: 0;
  position: absolute;
  right: -15px;
  top: 30px;
  border:5px solid;
  border-color:black aliceblue aliceblue aliceblue;
}

.websql-logo{
  align-self: center;
}

</style>
