<template>
  <div class="admin-page">
    <h1>Admin Dashboard</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Date</th>
          <th>Time</th>
          <th>Guests</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reservation in reservations" :key="reservation.id">
          <td>{{ reservation.id }}</td>
          <td>{{ reservation.name }}</td>
          <td>{{ reservation.email }}</td>
          <td>{{ reservation.date }}</td>
          <td>{{ reservation.time }}</td>
          <td>{{ reservation.guests }}</td>
          <td>
            <select v-model="reservation.status" @change="updateStatus(reservation.id, reservation.status)">
              <option value="pending">Pending</option>
              <option value="confirmed">Confirmed</option>
              <option value="canceled">Canceled</option>
            </select>
          </td>
          <td>
            <button @click="deleteReservation(reservation.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      reservations: [],
    };
  },
  mounted() {
    this.fetchReservations();
    console.log(this.reservations);
  },
  methods: {
    async fetchReservations() {
      try {
        const token = localStorage.getItem('token'); // 로컬 스토리지에서 JWT 토큰 가져오기
        const response = await axios.get(`${process.env.VUE_APP_BASE_URL}/api/admin/reservations/`, {
          headers: {
            Authorization: `Bearer ${token}`, // 인증 헤더 추가
          },
        });
        this.reservations = response.data;
      } catch (error) {
        console.error("Error fetching reservations:", error);
      }
    },
    async updateStatus(id, status) {
      try {
          await axios.put(`${process.env.VUE_APP_BASE_URL}/api/admin/reservations/${id}/`, { status });
          alert("Status updated successfully");
          this.fetchReservations(); // Reload reservations after update
      } catch (error) {
          console.error("Error updating status:", error);
      }
    },
    async deleteReservation(id) {
      if (confirm("Are you sure you want to delete this reservation?")) {
          try {
              await axios.delete(`${process.env.VUE_APP_BASE_URL}/api/admin/reservations/${id}/delete/`);
              this.fetchReservations(); // Reload reservations after deletion
          } catch (error) {
              console.error("Error deleting reservation:", error);
          }
      }
    },
  },  
};
</script>

<style>
/* Add your styles here */
.admin-page table {
  width: 100%;
  border-collapse: collapse;
}

.admin-page th,
.admin-page td {
  border: 1px solid #ddd;
  padding: 8px;
}

.admin-page th {
  background-color: #f4f4f4;
}
</style>
