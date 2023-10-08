const { ref, computed } = Vue

export default {
  name: 'pollAnswerInput',
  props: {
    id: Number,
    removable: Boolean,
    text: String,
    modelValue: String
  },
  emits: ['update:modelValue', 'removeAnswer'],

  setup(props) {

    const answerText = ref(props.text);
    const answerId = props.id;

    const answerNumber = computed(() => {
      return props.id + 1
    })

    const answerIdName = computed(() => {
      return `poll-answer-${answerNumber.value}`
    })

    const answerDisplayName = computed(() => {
      return `Answer ${answerNumber.value}`
    })


    return {
      answerNumber,
      answerIdName,
      answerDisplayName,
      answerText,
      answerId
    }
  },

  template: `
    <div>
    <label :for="answerIdName">Answer {{ answerNumber }}:</label>
    <div class="input-group mb-3">
    <input type="text" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" :name="answerIdName" class="form-control">
    <button v-if="removable" class="btn btn-outline-secondary" type="button" @click="$emit('removeAnswer', answerId)"><i class="fas fa-trash"></i></button>
    </div>
    </div>
    `
}
