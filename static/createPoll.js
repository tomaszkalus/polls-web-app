const { createApp, ref, computed, watch } = Vue
import pollAnswerInput from "./pollAnswerInput.js"

createApp({

    components: {
        pollAnswerInput
    },

    setup() {

        const defaultDate = (() => {
            const now = new Date();
            now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
            return now.toISOString().slice(0,16)

        })();

        const pollAnswersLimit = 8;
        const pollAnswers = ref([{ text: '', isRemovable: false }, { text: '', isRemovable: false }]);
        const isExpirationEnabled = ref(false);

        watch(isExpirationEnabled, e => {
            console.log(e)

        })

        let isPollAnswersLimitExceeded = computed(() => {
            return pollAnswers.value.length >= pollAnswersLimit
        })

        function addAnswer() {
            if (!isPollAnswersLimitExceeded.value) {
                pollAnswers.value.push({ text: "", isRemovable: true });
            }
        }

        function removeAnswer(index) {
            console.log(index)
            console.log(pollAnswers.value)
            if (pollAnswers.value.length > 1) {
                pollAnswers.value.splice(index, 1);
            }
        }

        return {
            addAnswer,
            pollAnswers,
            removeAnswer,
            isExpirationEnabled,
            defaultDate
        }
    }
}).mount('#answers-editor')