<template>
  <div>
    <nav
      class="bg-gray-800 flex flex-col fixed w-full"
      style="-webkit-app-region: drag"
    >
      <div class="ml-auto flex flex-row" style="-webkit-app-region: no-drag">
        <div
          @click="$root.events.window_minimize()"
          class="text-gray-500 hover:bg-gray-700 px-2"
        >
          <i class="fas fa-minus" />
        </div>
        <div
          @click="$root.events.window_maximize()"
          class="text-gray-500 hover:bg-gray-700 px-2"
        >
          <i class="far fa-square" />
        </div>
        <div
          @click="$root.events.window_close()"
          class="text-gray-500 hover:bg-red-500 px-2"
        >
          <i class="fas fa-times" />
        </div>
      </div>
      <AppBar
        :class="{ 'ml-20': !navHover, 'ml-48': navHover }"
        :title="$route.name"
        :running="$root.store.running"
        style="-webkit-app-region: no-drag"
      />
    </nav>
    <div class="bg-gray-900">
      <NavBar
        v-on:expand="expandNav"
        v-on:fold="foldNav"
        class="navbar mt-6"
        :title="'Capi'"
        :links="links"
        :selected="$route.name"
      />
      <div class="main" :class="{ 'ml-20': !navHover, 'ml-48': navHover }">
        <router-view
          class="p-4 pt-28 bg-gray-200 overflow-y-auto"
          style="height: calc(100vh);"
        />
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import AppBar from "@/components/AppBar.vue";

export default {
  components: {
    NavBar,
    AppBar
  },
  data() {
    return {
      links: [
        { icon: ["fas", "fa-home"], text: "Home", dest: "Home" },
        { icon: ["fas", "fa-tags"], text: "Label", dest: "Label" },
        // { icon: ["fas", "fa-database"], text: "Database", dest: "Database" },
        // { icon: ["fas", "fa-download"], text: "Downloads", dest: "Downloads" },
        { icon: ["fas", "fa-question"], text: "About", dest: "About" },
        { icon: ["fas", "fa-cog"], text: "Settings", dest: "Settings" }
      ],
      navHover: false
    };
  },
  methods: {
    expandNav: function() {
      this.navHover = true;
    },
    foldNav: function() {
      this.navHover = false;
    }
  }
};
</script>

<style scoped>
.navbar:hover {
  @apply w-48;
}

.main {
  @apply transition-all;
  @apply duration-200;
}
</style>
