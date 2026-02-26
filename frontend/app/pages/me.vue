<script setup lang="ts">
definePageMeta({
  middleware: "guest",
});

import { ref, reactive, onMounted } from "vue";
import { useNuxtApp } from "#app";

const { $api } = useNuxtApp();

const user = ref<any>(null);
const addresses = ref<any[]>([]);
const loading = ref(false);
const message = ref("");

// форма редактирования адреса
const editingAddress = ref<number | null>(null);

const addressForm = reactive({
  id: null,
  full_name: "",
  street: "",
  city: "",
  postal_code: "",
  country: "",
  phone: "",
  is_default: false,
});

// ===================
// LOAD DATA
// ===================

onMounted(async () => {
  await loadUser();
  await loadAddresses();
  await fetchOrders();
});

const loadUser = async () => {
  const res = await $api.get("/users/me/");
  user.value = res.data;
};

const loadAddresses = async () => {
  const res = await $api.get("/addresses/");
  addresses.value = res.data;
};

// ===================
// EMAIL VERIFICATION
// ===================

const resendVerification = async () => {
  try {
    await $api.post("/users/resend-verification/");
    message.value = "Verification email sent";
  } catch (e) {
    message.value = "Error sending email";
  }
};

// ===================
// ADDRESS CRUD
// ===================

const startEdit = (addr: any) => {
  editingAddress.value = addr.id;
  Object.assign(addressForm, addr);
};

const saveAddress = async () => {
  try {
    if (editingAddress.value) {
      await $api.put(`/addresses/${editingAddress.value}/`, addressForm);
    } else {
      await $api.post("/addresses/", addressForm);
    }

    await loadAddresses();
    cancelEdit();
  } catch (e) {
    console.error(e);
  }
};

const cancelEdit = () => {
  editingAddress.value = null;
  Object.assign(addressForm, {
    id: null,
    full_name: "",
    street: "",
    city: "",
    postal_code: "",
    country: "",
    phone: "",
    is_default: false,
  });
};

const deleteAddress = async (id: number) => {
  await $api.delete(`/addresses/${id}/`);
  await loadAddresses();
};

const orders = ref([]);
const ordersLoading = ref(true);

const fetchOrders = async () => {
  try {
    const res = await $api.get("/orders/");
    orders.value = res.data;
  } finally {
    ordersLoading.value = false;
  }
};
</script>

<template>
  <div class="me-page">
    <h1>My Profile</h1>

    <div v-if="user">
      <p><strong>Email:</strong> {{ user.email }}</p>

      <p>
        <strong>Status:</strong>
        <span v-if="user.is_verified">✅ Verified</span>
        <span v-else>❌ Not verified</span>
      </p>

      <button v-if="!user.is_verified" @click="resendVerification">
        Resend verification email
      </button>

      <p v-if="message">{{ message }}</p>
    </div>

    <hr />

    <h2>My Addresses</h2>

    <div v-for="addr in addresses" :key="addr.id" class="address-card">
      <p>{{ addr.full_name }}</p>
      <p>{{ addr.street }}, {{ addr.city }}</p>
      <p>{{ addr.postal_code }}, {{ addr.country }}</p>
      <p>{{ addr.phone }}</p>
      <p v-if="addr.is_default">⭐ Default</p>

      <button @click="startEdit(addr)">Edit</button>
      <button @click="deleteAddress(addr.id)">Delete</button>
    </div>

    <hr />

    <h2>{{ editingAddress ? "Edit Address" : "Add Address" }}</h2>

    <form @submit.prevent="saveAddress">
      <input v-model="addressForm.full_name" placeholder="Full name" required />
      <input v-model="addressForm.street" placeholder="Street" required />
      <input v-model="addressForm.city" placeholder="City" required />
      <input v-model="addressForm.postal_code" placeholder="Postal code" required />
      <input v-model="addressForm.country" placeholder="Country" required />
      <input v-model="addressForm.phone" placeholder="Phone" required />

      <label>
        <input type="checkbox" v-model="addressForm.is_default" />
        Is default
      </label>

      <button type="submit">Save</button>
      <button type="button" @click="cancelEdit">Cancel</button>
    </form>
    <h2>My Orders</h2>

    <div v-if="ordersLoading">Loading...</div>

    <div v-else-if="orders.length === 0">No orders yet</div>

    <div v-else>
      <div v-for="order in orders" :key="order.uuid" class="order-card">
        <p><strong>ID:</strong> {{ order.uuid }}</p>
        <p><strong>Status:</strong> {{ order.status }}</p>
        <p><strong>Total:</strong> ${{ order.total_price }}</p>

        <NuxtLink :to="`/order-success/${order.uuid}`"> View details </NuxtLink>
      </div>
    </div>
  </div>
</template>
