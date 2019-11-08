<template>
  <div class="home">
    <div class="sql-header">
      <el-row>
        <el-button type='primary' @click="post_query">Query</el-button>
      </el-row>
    </div>
    <div class="sql-content">
      <el-input
        type:="textarea"
        :rows="10"
        placeholder="Sql..."
        v-model="textarea"
      >
      </el-input>
    </div>
    <div class="sql-result" v-loading='loading'>
      <el-table
      v-if="res"
      :data="res.slice((currentPage-1)*pagesize, currentPage*pagesize)"
      border
      style="width:100%"
      @sort-change='sort_change'
      >
        <el-table-column v-for="col in header"
        :prop="col[0]"
        :label="col[0]"
        sortable='custom'
        >
        </el-table-column>
      </el-table>
      <div class="paginator" v-if="res">
        <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        @current-change="current_change"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "home",
  components: {
  },
  data() {
    return {
      textarea: '',
      res: null,
      header: null,
      total: 0,
      pagesize: 10,
      currentPage: 1,
      loading: false
    }
  },
  methods: {
    //向后端发起请求，查询sql语句
    post_query() {
      this.loading = true
      var path = '/sql'
      console.log("POST: ", this.textarea)
      this.$axios.post(path,{
        sql_line: this.textarea
      }).then( (response) => {
        this.loading = false
        this.res = response.data.res.data
        this.header = response.data.res.header
        this.total = this.res.length
        console.log("RESPONSE.length: ", this.res.length);
      })
    },
    current_change(currentPage) {
      this.currentPage = currentPage;
    },
    //sort_change参数: column:{prop: 'xxx', order: 'ascending'/'descending'}
    sort_change(column) {
      if ("descending" == column.order) {
        this.res = this.sortDescByKey(this.res, column.prop)
      } else {
        this.res = this.sortAscByKey(this.res, column.prop)
      }
    },
    //降序排列
    sortDescByKey(arr, key) {
      return arr.sort(function(a, b){
        let x = a[key]
        let y = b[key]
        return ((x>y) ? -1 : (x<y) ? 1 : 0)
      })
    },
    //升序排列
    sortAscByKey(arr, key) {
      return arr.sort(function(a, b){
        let x = a[key]
        let y = b[key]
        return ((x>y) ? 1 : (x<y) ? -1 : 0)
      })
    }
  }
};
</script>

<style lang="less">
.sql-header {
  text-align: left;
  margin: 10px;
}
.sql-content {
  margin: 10px;
}
.sql-result {
  margin: 10px;
}
</style>
