<template>
    <div class="sql-resbar">
      <img src="@/static/clock0.svg" height="13">
      <span class="sql-resbar-title">Runtime {{bar_cnt}}</span>
      <img src="@/static/list0.svg" height="13">
      <span class="sql-resbar-title">Rows {{bar_rows}}</span>
    </div>
</template>

<script>
  export default {
    props: [
      'bar_cnt',
      'bar_rows'
    ],
  }
</script>

<style lang="less">
.sql-resbar {
  margin: 10px;
  padding: 15px 0;
  text-align: left;
  color: grey;
  font-size: small;
  display: flex;
  align-items: center;
  &-title {
    margin-left: 3px;
    margin-right: 10px;
  }
}

</style>
