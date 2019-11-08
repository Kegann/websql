<template>
  <div class="menu-wrapper" v-if="!item.hidden&&item.children">

    <router-link v-if="hasOneShowingChild(item.children) &&
    !onlyOneChild.children"  :to="resolvePath(onlyOneChild.path)"
    class="menu-title">
      <el-menu-item :index="resolvePath(onlyOneChild.path)">
        <span v-if="onlyOneChild.name" slot="title">{{onlyOneChild.name}}</span>
      </el-menu-item>
    </router-link>

    <el-submenu v-else :index="item.name||item.path">
      <template slot="title">
        <span v-if="item.name" slot="title" class="menu-title">{{item.name}}</span>
      </template>

      <template v-for="child in item.children" v-if="!child.hidden">
        <NavItem :is-nest="true" class="nest-menu"
        v-if="child.children&&child.children.length>0" :item="child"
        :key="child.path" :basePath="resolvePath(child.path)" ></NavItem>

        <router-link v-else :to="resolvePath(child.path)" :key="child.name">
          <el-menu-item :index="resolvePath(child.path)">
            <span v-if="child.name" slot="title">{{child.name}}</span>
          </el-menu-item>
        </router-link>
      </template>
    </el-submenu>
  </div>
</template>

<script>
import path from 'path'

export default {
  name: 'NavItem',
  props: {
    item: {
      type: Object,
      required: true
    },
    basePath: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      onlyOneChild: null
    }
  },
  methods: {
    hasOneShowingChild(children) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false
        } else {
          this.onlyOneChild = item
          return true
        }
      })
      if (showingChildren.length === 1) {
        return true
      }
      return false
    },
    resolvePath(...paths) {
      return path.resolve(this.basePath, ...paths)
    }
  }
}

</script>

<style lang="less">
.menu-wrapper {
  display: inline-block;
  min-width: 180px;
  .el-submenu>.el-submenu__title{
    min-width: 180px !important;
  }
  el-menu-item{
    min-width: 180px !important;
  }
}
</style>
