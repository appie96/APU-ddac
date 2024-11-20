<template>
  <div class="container mt-5">
    <h1 class="text-center">Make a Reservation</h1>
    <form>
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          id="name"
          v-model="name"
          class="form-control"
          disabled
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="form-control"
          disabled
        />
      </div>
      <div class="mb-3">
        <label for="guests" class="form-label">Number of Guests</label>
        <input
          type="number"
          id="guests"
          v-model="guests"
          class="form-control"
          min="1"
        />
      </div>
      <div class="mb-3">
        <label for="date" class="form-label">Date</label>
        <input
          type="date"
          id="date"
          v-model="date"
          class="form-control"
          @change="fetchBookedTimes"
        />
      </div>
      <custom-time-picker
        id="time"
        label="Time"
        v-model="time"
        :bookedTimes="bookedTimes"
        @reserve="handleTimeSelection"
      ></custom-time-picker>
    </form>

    <!-- 예약 알림 메시지 -->
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CustomTimePicker from './CustomTimePicker.vue';

export default {
  name: 'ReservationPage',
  components: {
    CustomTimePicker,
  },
  data() {
    return {
      name: "",
      email: "",
      date: "",
      time: "",
      guests: 1,
      bookedTimes: [],
      isSubmitting: false, // 중복 요청 방지 플래그
      successMessage: "", // 성공 메시지
      errorMessage: "", // 에러 메시지
    };
  },
  methods: {
    fetchUserData() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push('/login');
        return;
      }

      axios
        .get("http://127.0.0.1:8000/api/user-info", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          this.name = response.data.name;
          this.email = response.data.email;
        })
        .catch((error) => {
          console.error("Failed to fetch user data:", error);
          if (error.response?.status === 401) {
            this.$router.push('/login');
          }
        });
    },

    fetchBookedTimes() {
      if (!this.date) return;

      const token = localStorage.getItem("token");
      axios
        .get(`http://127.0.0.1:8000/api/reservations/date/${this.date}/`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          this.bookedTimes = response.data.map(reservation => reservation.time);
        })
        .catch((error) => {
          console.error("Failed to fetch booked times:", error);
        });
    },

    handleTimeSelection(selectedTime) {
      if (this.isSubmitting) {
        console.warn("Reservation is already being processed");
        return;
      }

      this.isSubmitting = true; // 중복 요청 방지 플래그 설정
      this.successMessage = "";
      this.errorMessage = "";

      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push('/login');
        return;
      }

      const reservationData = {
        name: this.name,
        email: this.email,
        date: this.date,
        time: selectedTime,
        guests: this.guests,
      };

      axios
        .post("http://127.0.0.1:8000/api/reservation", reservationData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        .then(() => {
          this.successMessage = "Reservation created successfully!";
          setTimeout(() => {
            this.successMessage = ""; // 메시지 숨기기
            this.$router.push('/');
          }, 3000);
        })
        .catch((error) => {
          console.error("Failed to create reservation:", error);
          if (
            error.response &&
            error.response.data &&
            error.response.data.error === "This time slot is already booked."
          ) {
            this.errorMessage = "This time slot is already booked. Please choose another time.";
          } else {
            this.errorMessage = "Failed to create reservation. Please try again.";
          }
          setTimeout(() => {
            this.errorMessage = ""; // 메시지 숨기기
          }, 3000);
        })
        .finally(() => {
          this.isSubmitting = false; // 요청 완료 후 플래그 초기화
        });
    },
  },
  mounted() {
    this.fetchUserData();
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
.success-message {
  color: green;
  margin-top: 20px;
}
.reservation-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: left;
}
form div {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  box-sizing: border-box;
}
button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.alert {
  padding: 15px;
  margin-top: 20px;
  border-radius: 5px;
}
.alert-success {
  background-color: #d4edda;
  color: #155724;
}
.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
