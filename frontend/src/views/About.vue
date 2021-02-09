<template>
  <div>
    <main class="my-8 mx-16 text-center">
      <div
        class="grid grid-flow-col grid-rows-2 grid-cols-3 gap-x-8 items-center"
      >
        <div class="row-start-1">
          <Card :title="'Who are we?'">
            <p class="pt-8 px-4 pb-4">
              We are a group of undergraduate students from Ben Gurion
              University, studying information systems engineering, and this is
              our graduation project. The team members are Yuval Khoramian,
              Shoham Zarfati, Ron Zeidman, and Hod Twito. Prof. Yuval Shahar and
              Doc. Michael Gilead.
            </p>
          </Card>
        </div>

        <div class="row-start-1 col-span-2">
          <Card class="row-start-1 col-span-2" :title="'What are we doing?'">
            <p class="pt-8 px-4 pb-4">
              Our project attempts to "teach" computers to interpret human
              emotions by watching subjects like yourself use their computer.
              This software collects your usage data, including images from your
              camera, keyboard presses, and mouse movements. We will later use
              this data to create Machine Learning models that will understand
              the data and predict how you feel.
            </p>
          </Card>
        </div>

        <div class="col-start-1 row-start-2 col-span-2">
          <Card :title="'Are we stealing your data?'">
            <p class="pt-8 px-4 pb-4">
              No. All data is stored on your computer. Nothing is sent to us or
              anyone else. When you complete the data collection process, you
              will be able to inspect the collected data either using this
              software or by hand. Then choose what you are willing to share
              with us and send the data to us yourself. Additionally, it is
              possible to determine which data is collected in the first place
              through the settings menu.
            </p>
          </Card>
        </div>

        <div class="col-start-3 row-start-2">
          <Card :title="'Will this work?'">
            <p class="pt-8 px-4 pb-4">
              There is quite a bit of research in this field with some promising
              results. Obviously, no one has achieved a significant breakthrough
              allowing computers to easily identify how a user is feeling.
              Incremental improvements are the name of the game in research.
            </p>
          </Card>
        </div>
      </div>

      <Card class="my-8" :title="'Emotion labels'">
        <span class="text-left pt-8 px-4 pb-4">
          <p class="text-left">
            When you choose the labels for how you feel, there are 4 categories.
            First are the ordinary emotions we are used to, such as fear,
            happiness, sadness, etc. here, you should choose the state that best
            describes your current mood. However, it is acceptable to skip it if
            you feel that your mood cannot be identified by one of the emotions
            presented. The following three categories are less common and might
            require a more in-depth explanation to understand fully.
          </p>
          <h1 class="font-semibold mt-2">Valance:</h1>
          <p class="text-left">
            The first picture (leftmost) shows a person who is clearly
            distressed - relevant experiences could include panic, irritation,
            disgust, despair, defeat, or crisis. The last pictures shows an
            individual who is obviously elated - relevant experiences could
            include fun, delight, happiness, relaxation, satisfaction, or
            repose. The remaining pictures depict intermediate states.
          </p>
          <h1 class="font-semibold mt-2">Arousal:</h1>
          <p class="text-left">
            The first pictures shows an individual who is very calm, almost
            sleeping - relevant states could include relaxation, tranquility,
            idleness, meditation, boredom, or laziness. The last picture shows
            an individual who is bursting with arousal - relevant states could
            include excitation, euphoria, excitement, rage, agitation, or anger.
          </p>
          <h1 class="font-semibold mt-2">Dominance:</h1>
          <p class="text-left">
            The first picture shows an individual who feels a lack of control
            and agency - relevant states could include subordination,
            intimidation, subjugation, withdrawal, submission, or resignation.
            The last picture shows a person who is dominant and in control of
            the situation - relevant states could include control, influence,
            being important, dominant, recognized, or decisive.
          </p>
        </span>
      </Card>
    </main>
  </div>
</template>

<script>
import Card from "@/components/Card.vue";

export default {
  name: "About",
  components: {
    Card
  }
};
</script>
