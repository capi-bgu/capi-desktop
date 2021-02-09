import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/label",
    name: "Label",
    component: () => import("../views/Label.vue")
  },
  {
    path: "/database",
    name: "Database",
    component: () => import("../views/Database.vue")
  },
  {
    path: "/downloads",
    name: "Downloads",
    component: () => import("../views/Downloads.vue")
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("../views/Settings.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
