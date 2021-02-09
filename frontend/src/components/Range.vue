<template>
  <div
    class="flex flex-row items-center flex-grow my-4 w-full flex-wrap"
    style="flex-basis: 50%;"
  >
    <div
      v-for="item in values"
      :key="item.value"
      class="flex flex-col items-center flex-grow"
    >
      <input
        type="radio"
        :name="uid.toString()"
        :id="`${item.value}&${uid}`"
        :value="item.value"
        v-model="selected"
        required
      />
      <label
        :for="`${item.value}&${uid}`"
        class="flex flex-col items-center rounded-md px-4 py-2 font-bold"
      >
        <span v-if="item.emoji" class="text-4xl rounded-full px-4 pt-2 pb-4">
          {{ item.emoji }}
        </span>
        <span v-if="item.img" :src="item.img" />
        <div class="rounded-full  pb-2">
          <i v-if="item.icon" :class="item.icon" />
        </div>
        <span> {{ item.value }} </span>
      </label>
    </div>
  </div>
</template>

<script scoped>
let cuid = 0;

export default {
  name: "Range",
  beforeMount() {
    this.uid = cuid;
    cuid += 1;
  },
  props: {
    values: Array
  },
  data() {
    return {
      selected: null,
      uid: 0
    };
  }
};
</script>

<style scoped>
input[type="radio"] {
  @apply hidden;
}

label:hover {
  @apply ring-2;
  @apply ring-blue-500;
  @apply text-blue-600;
}

input[type="radio"]:checked + label {
  @apply ring-2;
  @apply ring-green-400;
  @apply text-green-500;
}
</style>
