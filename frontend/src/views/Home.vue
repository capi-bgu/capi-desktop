<template>
  <div>
    <main
      class="my-16 grid grid-flow-col grid-rows-6, grid-cols-6 gap-x-8 gap-y-16 md:mx-20 lg:mx-40 2xl:mx-80"
    >
      <Card
        v-if="$root.store.running"
        :title="'Runtime'"
        class="col-start-1 col-span-2"
      >
        <h1>{{ runtime + " " + runtimeUnits }}</h1>
      </Card>

      <Card v-if="$root.store.running" :title="'Next Label'" class="col-span-2">
        <h1>{{ nextLabel }}</h1>
      </Card>

      <Card :title="'CPU Usage'" class="col-span-2">
        <h1>{{ $root.store.cpu }}%</h1>
      </Card>

      <Card :title="'RAM Usage'" class="col-start-1 col-span-2">
        <h1>{{ $root.store.ram }}</h1>
      </Card>

      <Card v-if="$root.store.running" :title="'Mood'" class="col-span-2">
        <h1>{{ $root.store.lastMood }}</h1>
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
      runtimeUnits: "seconds",
      runtimeInterval: null,
      nextLabelInterval: null,
      nextLabel: "",
      timeToLabel: 0
    };
  },
  mounted() {
    if (this.$root.store.running) {
      this.$root.events.onStart("onStartHome", () => {});
      this.$root.events.onStop("onStopHome", this.onStopHome());
      this.onStartHome();
    } else {
      this.$root.events.onStart("onStartHome", this.onStartHome);
      this.$root.events.onStop("onStopHome", this.onStopHome());
    }
  },
  beforeDestroy() {
    this.onStopHome();
    this.$root.events.onStart("onStartHome", () => {});
    this.$root.events.onStop("onStopHome", () => {});
  },
  methods: {
    onStartHome() {
      this.onStopHome();
      this.runtimeInterval = setInterval(this.updateRuntime, 1000);
      this.nextLabelInterval = setInterval(this.updateNextLabel, 1000);
      this.updateRuntime();
      this.updateNextLabel();
    },
    onStopHome() {
      clearInterval(this.runtimeInterval);
      clearInterval(this.nextLabelInterval);
    },
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
      if (runtime_index < 0) return;

      if (
        units[runtime_index] === "minutes" &&
        this.runtimeUnits !== "minutes"
      ) {
        clearInterval(this.runtimeInterval);
        this.runtimeInterval = setInterval(this.updateRuntime, 1000 * 60);
      }

      if (units[runtime_index] === "seconds") {
        clearInterval(this.runtimeInterval);
        this.runtimeInterval = setInterval(this.updateRuntime, 1000);
      }

      this.runtime = times[runtime_index];
      this.runtimeUnits = units[runtime_index];
    },
    updateNextLabel() {
      if (this.$root.store.scheduledLabel) {
        this.nextLabel = "00:00";
        return;
      }

      const labelInterval =
        this.$root.store.settings.label_frequency *
        this.$root.store.settings.session_duration;

      const notificationInterval = 5;

      const ttl =
        labelInterval -
        Math.floor((Date.now() - this.$root.store.lastScheduledLabel) / 1000);
      if (ttl === notificationInterval)
        this.$root.events.notification({
          title: "Submit Label",
          subtitle: "Please Tell Us How You Feel",
          body: `In a few seconds you will be prompted with the CAPI app to fill in a form in order to label your current emotional state.`
        });

      if (ttl <= 0) this.nextLabel = "In a Moment";
      else this.nextLabel = `${Math.floor(ttl / 60)}:${ttl % 60}`;
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
