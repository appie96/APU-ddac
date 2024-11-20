<template>
  <div class="reservation-confirmation">
    <h1>Reservation Confirmation</h1>
    <div v-if="reservation">
      <p><strong>Reservation ID:</strong> {{ reservation.id }}</p>
      <p><strong>Name:</strong> {{ reservation.name }}</p>
      <p><strong>Email:</strong> {{ reservation.email }}</p>
      <p><strong>Date:</strong> {{ reservation.date }}</p>
      <p><strong>Time:</strong> {{ reservation.time }}</p>
      <p><strong>Guests:</strong> {{ reservation.guests }}</p>
    </div>
    <div v-else>
      <p>Loading reservation details...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      reservation: null,
    };
  },
  async mounted() {
    const reservationId = this.$route.query.reservation_id;
    try {
      const response = await axios.get(`/api/reservation/${reservationId}/`);
      this.reservation = response.data;
    } catch (error) {
      console.error("Error fetching reservation details:", error);
    }
  },
};
</script>

<style scoped>
.reservation-confirmation {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.reservation-confirmation h1 {
  color: #28a745;
}
.reservation-confirmation p {
  margin: 10px 0;
}
</style>
