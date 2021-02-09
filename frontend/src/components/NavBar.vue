<template>
  <nav @mouseover="expand" @mouseleave="fold" class="navbar bg-red-500">
    <ul class="nav">
      <li class="logo">
        <div class="logo-content">
          <i class="fas fa-angle-double-right"></i>
          <transition name="fade">
            <span v-if="expanded" class="logo-title">{{ title }}</span>
          </transition>
        </div>
      </li>
      <li
        v-for="link in links"
        v-bind:key="link.id"
        class="nav-item"
        :class="{ 'bg-gray-800': link.dest === selected }"
      >
        <router-link :to="{ name: link.dest }" class="nav-link">
          <i :class="link.icon" />
          <transition name="fade">
            <span v-if="expanded" class="link-text">{{ link.text }}</span>
          </transition>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    title: String,
    links: Array,
    selected: String
  },
  data() {
    return {
      expanded: false
    };
  },
  methods: {
    expand: function() {
      this.expanded = true;
      this.$emit("expand");
    },
    fold: function() {
      this.expanded = false;
      this.$emit("fold");
    }
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  @apply duration-200;
  @apply transition;
}
.fade-enter,
.fade-leave-to {
  @apply opacity-0;
}

.navbar {
  @apply w-20;
  @apply h-full;
  @apply fixed;
  @apply bg-gray-900;
  transition: 200ms ease;
}

.nav {
  @apply list-none;
  @apply flex;
  @apply h-full;
  @apply flex-col;
  @apply p-0;
  @apply m-0;
}

.logo {
  @apply font-extrabold;
  @apply uppercase;
  @apply tracking-widest;
  @apply text-3xl;
  @apply bg-black;
  @apply w-full;
}

.logo svg {
  @apply transition-transform;
  @apply ease-in-out;
  @apply duration-300;
}

.logo-content {
  @apply flex;
  @apply items-center;
  @apply justify-start;
  @apply ml-6;
  @apply h-20;
  @apply text-blue-500;
}

.logo-title {
  @apply ml-4;
}

.logo-content svg {
  min-width: 2rem;
  @apply w-8;
  @apply m-0;
}

.navbar:hover .logo svg {
  @apply transform;
  @apply -rotate-180;
}

.nav-item {
  @apply w-full;
  @apply last:mt-auto;
  @apply last:pb-4;
}

.nav-link {
  @apply flex;
  @apply items-center;
  @apply justify-start;
  @apply ml-6;
  @apply h-20;
  @apply text-gray-500;
  @apply transform;
  @apply hover:scale-110;
  @apply transition-colors;
  @apply transition-transform;
  @apply duration-300;
}

.link-text {
  @apply ml-4;
}

.nav-link svg {
  min-width: 2rem;
  @apply w-8;
  @apply m-0;
}

.nav-link:hover {
  @apply text-blue-300;
}

.nav-item:hover {
  @apply bg-gray-800;
}
</style>
