const { createApp, ref, computed } = Vue
import pollAnswerInput from "./pollAnswerInput.js"

createApp({

    components: {
        pollAnswerInput
    },

    setup() {

        const pollAnswersLimit = 8;
        const pollAnswers = ref([{ text: '', isRemovable: false }, { text: '', isRemovable: false }]);
        

        let isPollAnswersLimitExceeded = computed(() => {
            return pollAnswers.value.length >= pollAnswersLimit
        })

        function addAnswer() {
            if (!isPollAnswersLimitExceeded.value) {
                pollAnswers.value.push({ text: "", isRemovable: true });
            }
        }

        function removeAnswer(index) {
            if (pollAnswers.value.length > 1) {
                pollAnswers.value.splice(index, 1);
            }
        }

        return {
            addAnswer,
            pollAnswers,
            removeAnswer,
        }
    }
}).mount('#answers-editor')