<template>
  <div>
    <main
      class="my-8 mx-16 text-center flex flex-col justify-center items-center"
    >
      <Card class="my-4" :title="'Collection Methods'">
        <div class="mt-8 mx-4 flex flex-row flex-grow">
          <div class="s-check-group">
            <input
              class="s-check"
              type="checkbox"
              id="camera"
              v-model="$root.store.settings.use_camera"
            />
            <label for="camera"> Camera </label>
          </div>
          <div class="s-check-group">
            <input
              class="s-check"
              type="checkbox"
              id="mouse"
              v-model="$root.store.settings.use_mouse"
            />
            <label for="mouse"> Mouse </label>
          </div>
          <div class="s-check-group">
            <input
              class="s-check"
              type="checkbox"
              id="keyboard"
              v-model="$root.store.settings.use_keyboard"
            />
            <label for="keyboard"> keyboard </label>
          </div>
          <div class="s-check-group">
            <input
              class="s-check"
              type="checkbox"
              id="metadata"
              v-model="$root.store.settings.use_meta"
            />
            <label for="metadata"> Metadata </label>
          </div>
        </div>
      </Card>

      <Card class="my-4" :title="'Session'">
        <div class="s-number-group">
          <label for="num_sessions"> Number of Sessions: </label>
          <input
            class="s-number s-focus"
            type="number"
            min="1"
            id="num_sessions"
            v-model.number="$root.store.settings.num_sessions"
          />
        </div>
        <div class="s-number-group">
          <label for="session_duration"> Session Duration (seconds): </label>
          <input
            class="s-number s-focus"
            type="number"
            min="1"
            id="session_duration"
            v-model.number="$root.store.settings.session_duration"
          />
        </div>
        <div class="s-number-group">
          <label for="labeling_freq"> Labeling Frequency: </label>
          <input
            class="s-number s-focus"
            type="number"
            min="1"
            id="labeling_freq"
            v-model.number="$root.store.settings.label_frequency"
          />
        </div>
      </Card>

      <Card class="my-4" :title="'Database'">
        <div class="flex flex-row justify-between items-center my-4 mx-8">
          <label class="font-semibold mx-4" for="path"> Path: </label>
          <input
            class="bg-gray-200 border-2 border-gray-300 rounded-lg s-focus px-2 text-xl w-80"
            type="text"
            id="path"
            v-model="$root.store.settings.db_path"
          />
        </div>
      </Card>
    </main>
  </div>
</template>

<script>
import Card from "@/components/Card.vue";

export default {
  name: "Settings",
  components: {
    Card
  }
};
</script>

<style>
.s-check-group {
  @apply my-4;
  @apply mx-8;
  @apply font-semibold;
  @apply text-lg;
  @apply flex;
  @apply flex-col;
  @apply justify-center;
  @apply items-center;
}

.s-check {
  @apply w-6;
  @apply h-6;
  @apply m-2;
}

.s-number-group {
  @apply my-4;
  @apply mx-8;
  @apply font-semibold;
  @apply text-lg;
  @apply flex;
  @apply justify-between;
}

.s-number {
  @apply self-end;
  @apply bg-gray-200;
  @apply text-black;
  @apply border-gray-300;
  @apply border-2;
  @apply mx-8;
  @apply pl-4;
  @apply border-2;
  @apply rounded-full;
}

.s-focus:focus {
  @apply ring-2;
  @apply ring-blue-500;
}
</style>
