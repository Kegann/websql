<template>
<div class="nav">
  <el-menu
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    :default-active="$route.path"
    mode="horizontal"
    class="nav-menu"
  >
    <NavItem v-for="route in permission_routers" :key="route.name" :item="route"
    :basePath="route.path"></NavItem>
    <el-dropdown class="websql-avatar">
      <img src="@/static/websql_user3.svg" width="40" height="40">
      <div class="inverted-triangle"></div>
      <el-dropdown-menu class="websql-dropdown" slot="dropdown">
        <router-link class="inlineBlock" to="/auth/login">
          <el-dropdown-item>
            Login
          </el-dropdown-item>
        </router-link>
        <router-link class="inlineBlock" to="/auth/logout">
          <el-dropdown-item divided>
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
  background-color: black;
  font-size: 20px;
  z-index: 999;
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
}

.websql-avatar{
  top: 8px;
  right: 25px;
}

.inverted-triangle {
  width: 0;
  height: 0;
  position: absolute;
  right: -15px;
  top: 30px;
  border:5px solid;
  border-color:#ffffff rgb(84, 92, 100) rgb(84, 92, 100) rgb(84, 92, 100);
}
</style>
