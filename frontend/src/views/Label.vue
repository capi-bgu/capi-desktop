<template>
  <div class="px-16 flex flex-col">
    <Card class="my-8" :title="'Mood'">
      <Range :values="mood" @selected="select_mood" />
    </Card>
    <Card class="my-8" :title="'Valance'">
      <Range :values="valance" @selected="select_valance" />
      <div class="help">
        <div @click="help_show.valance = !help_show.valance">
          <i class="far fa-question-circle help-icon" />
        </div>
        <transition name="fade">
          <span v-if="help_show.valance">
            Valance is a measure of the positivity of one's mood, ranging from
            negative (0) to positive (8). <br />
            See
            <router-link :to="{ name: 'About' }" class="text-blue-600 underline"
              >about</router-link
            >
            page for more information.
          </span>
        </transition>
      </div>
    </Card>
    <Card class="my-8" :title="'Arousal'">
      <Range :values="arousal" @selected="select_arousal"/>
      <div class="help">
        <div @click="help_show.arousal = !help_show.arousal">
          <i class="far fa-question-circle help-icon" />
        </div>
        <transition name="fade">
          <span v-if="help_show.arousal">
            Arousal is a measure of the intensity with which emotion is felt,
            ranging from low (0) to high (8). <br />
            See
            <router-link :to="{ name: 'About' }" class="text-blue-600 underline"
              >about</router-link
            >
            page for more information.
          </span>
        </transition>
      </div>
    </Card>
    <Card class="my-8" :title="'Dominance'">
      <Range :values="dominance" @selected="select_dominance" />
      <div class="help">
        <div @click="help_show.dominance = !help_show.dominance">
          <i class="far fa-question-circle help-icon" />
        </div>
        <transition name="fade">
          <span v-if="help_show.dominance">
            Dominance is a measure of how much one controls one's emotions,
            ranging from not at all (0) to fully (8). <br />
            See
            <router-link :to="{ name: 'About' }" class="text-blue-600 underline"
              >about</router-link
            >
            page for more information.
          </span>
        </transition>
      </div>
    </Card>
    <div class="flex flex-row justify-center">
      <button @click="submit"
        class="bg-gradient-to-tr from-green-400 to-green-500 hover:to-green-400 rounded-lg text-white text-2xl font-bold px-8 py-2"
      >
        Submit
      </button>
    </div>
  </div>
</template>

<script>
import Card from "@/components/Card.vue";
import Range from "@/components/Range.vue";

export default {
  name: "Label",
  components: {
    Card,
    Range
  },
  data() {
    return {
      selected: {
        mood: "happiness",
        valance: 0,
        arousal: 0,
        dominance: 0
      },
      help_show: {
        valance: false,
        arousal: false,
        dominance: false
      },
      mood: [
        { value: "happiness", emoji: "😄" },
        { value: "disgust", emoji: "🤢" },
        { value: "fear", emoji: "😨" },
        { value: "sadness", emoji: "😔" },
        { value: "anger", emoji: "😠" }
      ],
      valance: [
        {
          value: 0,
          icon: ["far", "text-4xl", "fa-sad-cry", "text-purple-600"]
        },
        {
          value: 1,
          icon: ["far", "text-4xl", "fa-sad-tear", "text-purple-600"]
        },
        { value: 2, icon: ["far", "text-4xl", "fa-frown", "text-purple-600"] },
        {
          value: 3,
          icon: ["far", "text-4xl", "fa-frown-open", "text-purple-600"]
        },
        { value: 4, icon: ["far", "text-4xl", "fa-meh", "text-purple-600"] },
        { value: 5, icon: ["far", "text-4xl", "fa-smile", "text-purple-600"] },
        {
          value: 6,
          icon: ["far", "text-4xl", "fa-smile-beam", "text-purple-600"]
        },
        {
          value: 7,
          icon: ["far", "text-4xl", "fa-grin-beam", "text-purple-600"]
        },
        {
          value: 8,
          icon: ["far", "text-4xl", "fa-grin-squint", "text-purple-600"]
        }
      ],
      arousal: [
        { value: 0, icon: ["fas", "text-4xl", "fa-bolt", "text-gray-400"] },
        { value: 1, icon: ["fas", "text-4xl", "fa-bolt", "text-gray-600"] },
        { value: 2, icon: ["fas", "text-4xl", "fa-bolt", "text-gray-900"] },
        { value: 3, icon: ["fas", "text-4xl", "fa-bolt", "text-yellow-900"] },
        { value: 4, icon: ["fas", "text-4xl", "fa-bolt", "text-yellow-700"] },
        { value: 5, icon: ["fas", "text-4xl", "fa-bolt", "text-yellow-600"] },
        { value: 6, icon: ["fas", "text-4xl", "fa-bolt", "text-yellow-500"] },
        { value: 7, icon: ["fas", "text-4xl", "fa-bolt", "text-yellow-400"] },
        { value: 8, icon: ["fas", "text-4xl", "fa-bolt", "text-yellow-300"] }
      ],
      dominance: [
        { value: 0, icon: ["fas", "fa-user", "text-xs", "text-purple-700"] },
        { value: 1, icon: ["fas", "fa-user", "text-sm", "text-purple-700"] },
        { value: 2, icon: ["fas", "fa-user", "text-base", "text-purple-700"] },
        { value: 3, icon: ["fas", "fa-user", "text-lg", "text-purple-700"] },
        { value: 4, icon: ["fas", "fa-user", "text-xl", "text-purple-700"] },
        { value: 5, icon: ["fas", "fa-user", "text-2xl", "text-purple-700"] },
        { value: 6, icon: ["fas", "fa-user", "text-3xl", "text-purple-700"] },
        { value: 7, icon: ["fas", "fa-user", "text-4xl", "text-purple-700"] },
        { value: 8, icon: ["fas", "fa-user", "text-5xl", "text-purple-700"] }
      ]
    };
  },
  methods: {
    submit: function() {
      this.$root.events.label({
        categorical: this.selected.mood,
        VAD: {
          valance: this.selected.valance,
          arousal: this.selected.arousal,
          dominance: this.selected.dominance
        }
      });
    },
    select_mood: function(mood) {
      this.selected.mood = mood;
    },
    select_valance: function(valance) {
      this.selected.valance = valance;
    },
    select_arousal: function(arousal) {
      this.selected.arousal = arousal;
    },
    select_dominance: function(dominance) {
      this.selected.dominance = dominance;
    }
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  @apply duration-500;
  @apply transition;
}
.fade-enter,
.fade-leave-to {
  @apply opacity-0;
}

.help {
  @apply text-center;
  @apply font-semibold;
  @apply px-16;
  @apply flex;
  @apply flex-col;
  @apply justify-center;
  @apply items-center;
  @apply mt-4;
  @apply font-semibold;
}

.help-icon {
  @apply text-2xl;
  @apply mb-2;
  @apply hover:text-blue-500;
}
</style>
