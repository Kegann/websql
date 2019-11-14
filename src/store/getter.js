const getters = {
    permission_routers: state => state.permission.routers,
    login_reminder: state => state.app_config.login_reminder,
    userName: state => state.user.userName
}

export default getters
