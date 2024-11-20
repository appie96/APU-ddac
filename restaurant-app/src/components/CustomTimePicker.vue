<template>
  <div>
    <label :for="id">{{ label }}</label>
    <div class="time-buttons">
      <button
        v-for="time in availableTimes"
        :key="time"
        :class="['btn', 'btn-time', { 'btn-disabled': isTimeBooked(time), 'btn-selected': isSelected(time), 'btn-available': !isTimeBooked(time) }]"
        @click="selectTime(time)"
        :disabled="isTimeBooked(time)"
      >
        {{ time }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomTimePicker',
  props: {
    id: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    modelValue: {
      type: String,
      required: true
    },
    bookedTimes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      timeOptions: this.generateTimeOptions()
    };
  },
  computed: {
    availableTimes() {
      return this.timeOptions;
    }
  },
  methods: {
    generateTimeOptions() {
      const times = [];
      let startTime = new Date();
      startTime.setHours(10, 0, 0); // 10:00 AM
      const endTime = new Date();
      endTime.setHours(21, 30, 0); // 9:30 PM

      while (startTime <= endTime) {
        const hours = startTime.getHours().toString().padStart(2, '0');
        const minutes = startTime.getMinutes().toString().padStart(2, '0');
        times.push(`${hours}:${minutes}`);
        startTime.setMinutes(startTime.getMinutes() + 30); // 30 minutes interval
      }

      return times;
    },
    isTimeBooked(time) {
      return this.bookedTimes.includes(time);
    },
    isSelected(time) {
      return this.modelValue === time;
    },
    selectTime(time) {
      if (!this.isTimeBooked(time) && this.modelValue !== time) {
        this.$emit('update:modelValue', time);
        this.$emit('reserve', time); // Emit reserve event
      }
    }
  },
  watch: {
    modelValue(newValue) {
      this.$emit('update:modelValue', newValue);
    },
    bookedTimes() {
      // Trigger re-computation of availableTimes when bookedTimes changes
      this.timeOptions = this.generateTimeOptions();
    }
  }
};
</script>

<style scoped>
.time-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.btn-time {
  flex: 1 1 calc(33.333% - 10px);
  margin-bottom: 10px;
  padding: 10px;
  border: none;
  cursor: pointer;
  color: white;
}
.btn-available {
  background-color: #007bff;
}
.btn-available:hover {
  background-color: #0056b3;
  color: white;
}
.btn-disabled {
  background-color: grey;
  cursor: not-allowed;
}
.btn-selected {
  background-color: #0056b3; /* Green for selected time */
}
</style>