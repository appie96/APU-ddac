<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h1 class="text-center mb-4">Edit Reservation</h1>
        
        <div v-if="loading" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <form v-else @submit.prevent="updateReservation" class="reservation-form">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input
              type="text"
              id="name"
              v-model="reservation.name"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label for="date" class="form-label">Date</label>
            <input
              type="date"
              id="date"
              v-model="reservation.date"
              class="form-control"
              required
            />
          </div>

          <custom-time-picker
            id="time"
            label="Time"
            v-model="reservation.time"
          ></custom-time-picker>

          <div class="mb-3">
            <label for="guests" class="form-label">Number of Guests</label>
            <input
              type="number"
              id="guests"
              v-model="reservation.guests"
              class="form-control"
              min="1"
              required
            />
          </div>

          <div class="d-grid gap-2">
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? 'Updating...' : 'Update Reservation' }}
            </button>
            <button 
              type="button" 
              class="btn btn-secondary"
              @click="$router.push('/profile')"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CustomTimePicker from './CustomTimePicker.vue';

export default {
  name: 'ReservationEdit',
  components: {
    CustomTimePicker
  },
  data() {
    return {
      reservation: {
        name: "",
        date: "",
        time: "",
        guests: 1,
      },
      loading: true,
      error: null,
      isSubmitting: false
    };
  },
  async mounted() {
    await this.fetchReservation();
  },
  methods: {
    async fetchReservation() {
      const reservationId = this.$route.query.reservation_id;
      const token = localStorage.getItem("token");

      try {
        const response = await axios.get(`/api/reservation/${reservationId}/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.reservation = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching reservation:", error);
        this.error = "Failed to load reservation details. Please try again.";
        this.loading = false;
      }
    },

    async updateReservation() {
      const reservationId = this.$route.query.reservation_id;
      const token = localStorage.getItem("token");
      
      try {
        this.isSubmitting = true;
        await axios.patch(
          `/api/reservation/${reservationId}/update/`, 
          this.reservation,
          {
            headers: { 
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        
        this.$router.push({
          name: 'Profile',
          query: { message: 'Reservation updated successfully!' }
        });
      } catch (error) {
        console.error("Error updating reservation:", error);
        this.error = "Failed to update reservation. Please try again.";
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.reservation-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-label {
  font-weight: 500;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
