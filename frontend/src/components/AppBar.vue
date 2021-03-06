<template>
  <div class="bg-gray-900 h-20 flex flex-row px-4">
    <div class="title">{{ title }}</div>
    <button
      v-on:click="indicator_click"
      class="indicator"
      :class="{
        'bg-gray-500': !$root.store.ready,
        'bg-blue-500 hover:bg-green-400': !running && $root.store.ready,
        'bg-green-400 hover:bg-red-500': running && $root.store.ready
      }"
    >
      <span v-if="!$root.store.ready">Loading...</span>
      <span v-else-if="!running">Start</span>
      <span v-else>Stop</span>
    </button>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    running: Boolean
  },
  methods: {
    indicator_click: function() {
      if (!this.$root.store.ready) return;

      if (this.running) this.$root.events.stop();
      else this.$root.events.start();
    }
  }
};
</script>

<style scoped>
.title {
  @apply text-white;
  @apply text-2xl;
  @apply font-bold;
  @apply self-center;
}

.indicator {
  @apply uppercase;
  @apply transition-all;
  @apply duration-200;
  @apply ease-in-out;
  @apply text-white;
  @apply py-2;
  @apply px-8;
  @apply rounded-lg;
  @apply ml-auto;
  @apply self-center;
  @apply font-semibold;
}

.indicator:hover {
  @apply transform;
  @apply scale-110;
}
</style>
