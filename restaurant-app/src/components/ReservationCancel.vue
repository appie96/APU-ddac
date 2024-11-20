<template>
  <div>
    <h1>Reservation Details</h1>
    <p><strong>Date:</strong> {{ reservation.date }}</p>
    <p><strong>Time:</strong> {{ reservation.time }}</p>
    <p><strong>Guests:</strong> {{ reservation.guests }}</p>
    <button @click="cancelReservation">Cancel Reservation</button>
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
      console.error("Error fetching reservation:", error);
    }
  },
  methods: {
    async cancelReservation() {
      const reservationId = this.$route.query.reservation_id;
      if (confirm("Are you sure you want to cancel this reservation?")) {
        try {
          await axios.delete(`/api/reservation/${reservationId}/cancel/`);
          alert("Reservation canceled successfully!");
          this.$router.push("/");
        } catch (error) {
          console.error("Error canceling reservation:", error);
        }
      }
    },
  },
};
</script>
