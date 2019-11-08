<template>
<div id="app-wrapper">
  <div id="header">
    <div class="header__desc">WebSql</div>
  </div>
  <Nav></Nav>
  <div id="content">
    <div class="content-view">
      <router-view></router-view>
    </div>
  </div>
</div>
</template>

<script>
import { mapGetters } from 'vuex'
import Nav from './components/nav'

export default{
  name: 'layout',
  computed: {
    ...mapGetters([
    'permission_routers'
    ])
  },
  components: {Nav}
}

</script>

<style lang="less">
#header {
  .header__desc{
    color: black;
    font-size: 32px;
    line-height: 50px;
    text-align: left;
    padding: 20px 0 20px 200px;
    font-weight: lighter;
  }
}
#app-wrapper {
  position:relative;
}

</style>

