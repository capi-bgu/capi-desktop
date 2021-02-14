<template>
  <div>
    <main
      class="my-16 grid grid-flow-col grid-rows-6, grid-cols-6 gap-x-8 gap-y-16 md:mx-20 lg:mx-40 2xl:mx-80"
    >
      <Card :title="'Runtime'" class="col-start-1 col-span-2">
        <h1>{{ runtime.toString() + " " + runtime_unites }}</h1>
      </Card>

      <Card :title="'session Length'" class="col-span-2">
        <h1>{{ $root.store.settings.session_duration }}</h1>
      </Card>

      <Card :title="'CPU Usage'" class="col-span-2">
        <h1>{{ $root.store.cpu }}</h1>
      </Card>

      <Card :title="'RAM Usage'" class="col-start-1 col-span-2">
        <h1>{{ $root.store.ram }}</h1>
      </Card>

      <Card :title="'Mood'" class="col-span-2">
        <h1>{{ $root.store.mood }}</h1>
      </Card>

      <Card :title="'Disk Space'" class="col-span-2">
        <h1>{{ $root.store.disk }}</h1>
      </Card>
    </main>
  </div>
</template>

<script>
import Card from "@/components/Card.vue";

export default {
  name: "Home",
  components: {
    Card
  },
  data() {
    return {
      runtime: 1,
      runtime_unites: "seconds"
    };
  },
  mounted() {
    this.interval = setInterval(this.updateRuntime, 1000);
    this.updateRuntime();
  },
  methods: {
    updateRuntime() {
      const runtime_millis = Date.now() - this.$root.store.start_time;
      const times = [
        Math.floor(runtime_millis / (1000 * 60 * 60 * 24)),
        Math.floor(runtime_millis / (1000 * 60 * 60)),
        Math.floor(runtime_millis / (1000 * 60)),
        Math.floor(runtime_millis / 1000)
      ];
      const units = ["days", "hours", "minutes", "seconds"];

      const runtime_index = times.findIndex(t => t > 0);
      this.runtime = times[runtime_index];
      this.runtime_unites = units[runtime_index];
    }
  }
};
</script>

<style scoped>
h1 {
  @apply text-3xl;
  @apply pt-4;
  @apply font-bold;
  @apply font-mono;
  @apply text-center;
}
</style>
