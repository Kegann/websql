<template>
  <div>
  </div>
</template>

<script>
export default{
    mounted() {
        this.$confirm("确认退出吗？", "提示", {
        }).then(() => {
            this.$store.dispatch('Logout');
            this.$router.push('/auth/login');
        }).catch((error)=> {
          this.$router.push('/')
        })
    }
}
</script>
