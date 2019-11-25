<template>
  <div class="home">
    <div class="sql-header">
      <el-row class="sql-button">
        <el-button type='primary' @click="post_query" :disabled="loading">Query</el-button>
        <el-button @click="save_query" :disabled="loading">Save Sql</el-button>
      </el-row>
    </div>
    <div class="sql-content">
      <el-input
        type="textarea"
        :autosize="{minRows: 4, maxRows: 20}"
        placeholder="Sql..."
        v-model="textarea">
      </el-input>
    </div>
    <div class="loading-container" v-loading='loading' :element-loading-text="loading_txt">
    </div>
    <div class="sql-result"
    >
      <el-table
      v-if="res"
      :data="res.slice((currentPage-1)*pagesize, currentPage*pagesize)"
      border
      style="width:100%"
      @sort-change='sort_change'>
        <el-table-column v-for="col in header"
          :prop="col[0]"
          :label="col[0]"
          :key="col[0]"
          sortable='custom'>
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
      <div class="error-detail" v-if="error_detail">
        {{error_detail}}
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapGetters } from 'vuex'
import { Message } from 'element-ui'

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
      loading: false,
      res_header: null,
      loading_txt: "",
      error_detail: "",
    } },
  computed: {
    ...mapGetters([
        'login_reminder'
    ])
  },
  methods: {
    //向后端发起请求，查询sql语句
    post_query() {
      let token = window.localStorage.getItem('websql-token');
      //没有token认为未登录，弹出提示框
      if (!token && this.login_reminder) {
        console.log("NO LOGIN")
      }
      this.initData()
      this.loading = true
      this.loading_txt = "查询中..."
      var path = '/sql'
      // console.log("POST: ", this.textarea)
      this.$axios.post(path,{
        sql_line: this.textarea
      }).then( (response) => {
        this.loading = false
        this.loading_txt = ""
        this.res = response.data.res.data
        this.header = response.data.res.header
        this.total = this.res.length
        this.res_header = response.data.res
        console.log("LENGTH OF RES_HEADER: ", this.res_header.data.length)
      }).catch( (error) => {
        this.loading = false;
        //console.log("error: ", error.response.data.message)
        if (error.response) {
          this.error_detail = error.response.data.message;
        }
        Message({
          type: 'error',
          message: 'query failed...',
          duration: 2 * 1000
        })
      })
    },
    save_query() {
        //console.log("SAVE QUERY...")
        var path = "/sql/history"
        this.loading = true
        this.loading_txt = "保存中..."
        console.log("LENGTH OF RES_HEADER: ", this.res_header)
        this.$axios.post(path, {
            sql_line: this.textarea,
            sql_res: this.res_header
        }).then( (response) => {
            //保存成功，弹窗1s
            // console.log("save succeed...");
            this.loading = false;
            this.loading_txt = "";
            Message({
              type: 'success',
              message: 'save succeed!',
              duration: 1 * 1000
            })
        }).catch( (error) => {
          //保存失败，弹窗1s
          // console.log("save failed...")
          this.loading = false;
          this.loading_txt = "";
          Message({
            type: 'error',
            message: 'save failed...',
            duration: 1 * 1000
          })
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
    },
    initData() {
      this.res = null
      this.header = null
      this.total = 0
      this.currentPage = 1
      this.error_detail = ""
    },
  },
  mounted() {
    //console.log("Check...", this.$store.state.history.sql_res)
    if (this.$store.state.history.active) {
      this.textarea = this.$store.state.history.sql_line;
      if (this.$store.state.history.sql_res) {
        this.res = this.$store.state.history.sql_res.data;
        this.header = this.$store.state.history.sql_res.header
        this.total = this.res.length
      }
    }
  },
  beforeDestroy() {
    this.$store.dispatch('DeactiveHis');
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
.sql-button {
}

.error-detail {
  border: 1px white solid;
  border-radius: 5px;
  text-align: left;
  padding: 5px;
  color: white;
  background-color: rgba(244,67,54,.7);
}
</style>
