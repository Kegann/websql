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
    //redirect: '/home',
    children: [{
      path: '/home',
      name: 'home',
      component: () => import('../views/Home.vue')
    }]
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Layout,
    redirect: '/about/author',
    children: [{
      path: '/about/author',
      name: 'author',
      component: () => import(/* webpackChunkName: "about" */ "../views/About.vue")
    }]
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes: constantRouterMap
});

export default router;
