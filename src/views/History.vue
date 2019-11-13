<template>
  <div class="sql-history">
    <h3>Sql History</h3>
    <div class="sql-history-form">
        <el-table 
        v-if="sql_history"
        :data="sql_history"
        border>
            <el-table-column
            prop="sql_line"
            label="SQL"
            >
            </el-table-column>
            <el-table-column
            prop="create_time"
            label="创建时间"
            >
            </el-table-column>
        </el-table>
    </div>
  </div>
</template>

<script>
export default {
    data() {
        return {
            sql_history: null
        }
    },
    mounted() {
        var path = "/sql/history"
        this.$axios.get(path, {}).then( (response) => {
            console.log("Get history: ", response);
            if (response.data.sqls.length > 0) {
                this.sql_history = response.data.sqls
            }
        })
    }
}
</script>

<style lang="less">
.sql-history h3 {
    text-align: left;
    margin: 10px 0;
}
</style>
