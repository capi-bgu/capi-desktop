<template>
  <div
    class="bg-gradient-to-tr from-gray-200 to-white shadow-lg rounded-xl p-4 text-center"
  >
    <h1 v-if="title" class="text-lg font-light">{{ title }}</h1>
    <slot />
  </div>
</template>

<script>
export default {
  props: {
    title: String
  }
};
</script>
