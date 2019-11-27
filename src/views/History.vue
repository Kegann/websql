<template>
  <div class="sql-history">
    <h3>History</h3>
    <div class="loading-container" v-loading='loading' :element-loading-text="loading_txt">
    </div>
    <div class="sql-history-form">
        <el-table
        v-if="sql_history"
        :data="sql_history.slice((currentPage -1)*pageSize, currentPage*pageSize)"
        border>
            <el-table-column
            label="SQL"
            >
              <template slot-scope="scope">
                <span @click="direct_detail(scope.row.sql_line, scope.row.sql_res)" class="history-form-link">
                  {{scope.row.sql_line}}
                </span>
              </template>
            </el-table-column>
            <el-table-column
            prop="create_time"
            label="创建时间"
            >
            </el-table-column>
            <el-table-column>
                <template slot-scope="scope">
                  <el-button 
                    size="mini"
                    type="danger"
                    round
                    @click="remove_his(scope.row.sql_id, scope.$index)">
                    删除
                  </el-button>
                </template>
            </el-table-column>
        </el-table>
        <div class="history-paginator" v-if="total">
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
import { Message } from 'element-ui'

export default {
    data() {
        return {
            sql_history: null,
            pageSize: 10,
            currentPage: 1,
            total: 0,
            sql_res: "",
            loading: false,
            loading_txt: "",
        }
    },
    methods: {
      current_change(currentPage) {
        this.currentPage = currentPage;
      },
      direct_detail(sqlline,sqlres) {
        // console.log("Test check...");
        this.$router.push({path: '/sql'});
        this.$store.dispatch('ActiveHis', {line: sqlline , res:sqlres}).then( response => {
        //console.log("AcitveHis succeed..")
        }).catch( error => {
          console.log("ActiveHist failed;")
        })
      },
      remove_his(sql_id, idx) {
        var path = "/sql/history/" + sql_id
        //console.log("REMOVING... ", sql_id, path, idx, this.sql_history)
        this.loading = true;
        this.loading_txt = "删除中...";
        this.$axios.delete(path,{}
        ).then( (response) => {
          this.loading = false;
          Message({
            type: "success",
            message: "delete succeed!",
            duration: 1 * 1000
          });
          this.sql_history.splice(idx,1);
        }).catch( (error) => {
          this.loading = false;
          Message({
            type: "error",
            message: "delete failed...",
            duration: 1 * 1000
          })
        })
      }
    },
    mounted() {
        var path = "/sql/history"
        this.loading = true;
        this.loading_txt = "加载中..."
        this.$axios.get(path, {}).then( (response) => {
            // console.log("Get history: ", response);
            this.loading = false
            this.loading_txt = ""
            if (response.data.sqls.length > 0) {
                this.sql_history = response.data.sqls;
                this.total = this.sql_history.length;
                this.sql_res = response.data.res;
            }
        }).catch( (error) => {
          this.loading = false;
          this.loading_txt = ""
          Message({
            type: 'error',
            message: 'Load history failed...',
            duration: 1 * 1000
          })
        })
    }
}
</script>

<style lang="less">
.sql-history {
  padding: 0 15px;
  background-color: #f5efef;
}
.sql-history h3 {
    text-align: left;
    padding: 15px 0;
    margin-bottom: 15px;
    background-color: white;
    margin-left: -15px;
    margin-right: -15px;
}
.history-paginator {
  margin: 15px -15px;
  background-color: white;
  padding-top: 5px;
}

.history-form-link:hover {
  cursor: pointer;
  color: steelblue;
  font-weight: bold;
}
</style>
