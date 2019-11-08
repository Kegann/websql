<template>
<div class="nav"> 
  <el-menu
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    :default-active="$route.path"
    mode="horizontal"
  >
    <NavItem v-for="route in permission_routers" :key="route.name" :item="route"
    :basePath="route.path"></NavItem>
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
</style>
