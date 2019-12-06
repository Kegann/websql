<template>
  <div class="home">
    <div class="sql-header">
      <el-row class="sql-button">
        <el-button type='primary' 
          @click="post_query" 
          :disabled="loading" 
          :loading="loading">Query
        </el-button>
        <el-button @click="save_query" :disabled="loading">Save Sql</el-button>
        <el-tooltip effect="dark" content="导出csv是已编码格式!" placement="right-end">
          <el-button @click="export_csv" :disabled="!res">Export csv</el-button>
        </el-tooltip>
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
    <resBar-component v-bind:bar_cnt="bar_cnt" v-bind:bar_rows="bar_rows"></resBar-component>
    <div class="sql-cnt" v-show="loading">
        {{timeCnt}}
    </div>

    <div class="loading-container" :element-loading-text="loading_txt">
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
import resBar from './components/resbar'

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
      error_detail: "",
      cnt: 0,
      loading_txt: "",
      interval_id: null,
      bar_cnt: "-",
      bar_rows: "-",
    } },
  computed: {
    timeCnt() {
      return this.switch_time(this.cnt)
    },
    ...mapGetters([
        'login_reminder'
    ])
  },
  methods: {
    switch_time(timeStamp) {
      let h = parseInt(timeStamp / 3600);
      let hh = parseInt(h/10);
      let hl = h%10;
      let m = parseInt((timeStamp % 3600) / 60);
      let mh = parseInt(m/10);
      let ml = m%10;
      let s = timeStamp % 60;
      let sh = parseInt(s/10);
      let sl = s%10;
      let res = `Querying... ${hh}${hl}:${mh}${ml}:${sh}${sl}`;
      // console.log("RES: ", res);
      return res
    },
    //向后端发起请求，查询sql语句
    post_query() {
      this.bar_cnt = "running...";
      this.bar_rows = "-";
      var that = this;
      this.interval_id = setInterval(function(){
        that.cnt ++;
      }, 1000)
      let token = window.localStorage.getItem('websql-token');
      //没有token认为未登录，弹出提示框
      if (!token && this.login_reminder) {
        console.log("NO LOGIN")
      }
      this.initData()
      this.loading = true
      // this.loading_txt = "查询中..."
      var path = '/sql'
      // console.log("POST: ", this.textarea)
      this.$axios.post(path,{
        sql_line: this.textarea
      }).then( (response) => {
        this.bar_cnt = this.cnt + "s";
        // 停止计数器
        if (this.interval_id) {
          clearInterval(this.interval_id);
          this.interval_id = null;
        };
        this.cnt = 0;
        this.loading = false
        this.loading_txt = ""
        this.res = response.data.res.data
        this.bar_rows = this.res.length;
        this.header = response.data.res.header
        this.total = this.res.length
        this.res_header = response.data.res
        // console.log("LENGTH OF RES_HEADER: ", this.res_header.data.length)
      }).catch( (error) => {
        this.bar_cnt = "-";
        // 停止计数器
        if (this.interval_id) {
          clearInterval(this.interval_id);
          this.interval_id = null;
        };
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
    createDownloadClick(content, fileName) {
      const link = document.createElement("a");
      link.href = encodeURI(content);
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    save_query() {
        //console.log("SAVE QUERY...")
        var path = "/sql/history"
        this.loading = true
        this.loading_txt = "保存中..."
        // console.log("LENGTH OF RES_HEADER: ", this.res_header)
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
    export_csv() {
      try {
        let username = this.$store.state.user.userName;
        if (username) {
          let timestamp = (new Date()).valueOf().toString();
          let filename = username + '_' + timestamp
          let header = [];
          let obj = [];
          let csv = "";
          for (let i=0; i<this.header.length; i++) {
            header.push(this.header[i][0])
          }
          header = header.join(',')
          csv = header + "\n";
          for (let j=0; j<this.res.length; j++) {
            let row=""
            for (let k in this.res[j]) {
              // 转义
              row += escape(this.res[j][k]) + ','
            }
            csv = csv + row + "\n";
          }
          console.log("obj: ",csv);
          /**
          const result = json2csv.parse(obj, {
            // fields: header,
            // excelStrings: true
          });
          console.log("exporting...", result);
          **/
          let csvContent = "data:text/csv;charset=utf-8,\uFEFF" + csv;
          this.createDownloadClick(csvContent, `${filename}.csv`)
        }
      } catch (err) {
        console.log("err: ", err)
        Message({
          type: 'warning',
          message: err,
          duration: 1 * 1000
        })
      }
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
        this.header = this.$store.state.history.sql_res.header;
        this.total = this.res.length;
      };
    };
  },
  beforeDestroy() {
    this.$store.dispatch('DeactiveHis');
  },
  components: {
    'resBar-component': resBar,
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



.sql-cnt {
  background-color: rgba(33,150,243,.7);
  padding: 15px 20px;
  color: white;
  text-align: left;
  border-radius: 3px;
  font-size: 14px;
  img {
    margin: 10px;
  }
}
</style>
