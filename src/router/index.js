import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import Layout from '../components/Layout'

export const constantRouterMap = [
  {
    path: "/",
    name: "index",
    hidden: false,
    component: Layout,
    redirect: '/sql',
    children: [{
      path: '/sql',
      name: 'SQL',
      component: () => import('../views/Sql.vue')
    }]
  },
  {
    path: "/history",
    name: "HISTORY",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Layout,
    redirect: '/history/sql',
    children: [{
      path: '/history/sql',
      name: 'HISTORY_SQL',
      component: () => import(/* webpackChunkName: "about" */ "../views/History.vue")
    }]
  },
  {
    path: "/auth",
    name: "auth",
    component: Layout,
    hidden: true,
    children: [
    {
        path: '/auth/login',
        name: 'login',
        hidden: true,
        component: () => import("../views/Auth/Login")
    },
    {
        path: '/auth/logout',
        name: 'logout',
        hidden: true,
        component: () => import("../views/Auth/Logout")
    }
    ]
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes: constantRouterMap
});

export default router;
