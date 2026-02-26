<script setup lang="ts">
import { useAuthStore } from "~/stores/auth"
import { useAuthModalStore } from "~/stores/authModal"

const auth = useAuthStore()
const modal = useAuthModalStore()
</script>

<template>
  <div>
    <button v-if="!auth.isAuthenticated" @click="modal.open()">
      Login
    </button>

    <button v-else @click="auth.logout()">
      Logout ({{ auth.user?.email }})
    </button>
  </div>
</template>