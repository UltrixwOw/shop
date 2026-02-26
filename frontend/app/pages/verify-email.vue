<script setup>
const route = useRoute()
const config = useRuntimeConfig()

const loading = ref(true)
const success = ref(false)
const error = ref(null)

onMounted(async () => {
  const uid = route.query.uid
  const token = route.query.token

  if (!uid || !token) {
    error.value = "Invalid verification link"
    loading.value = false
    return
  }

  try {
    await $fetch(`${config.public.apiBase}/users/verify/`, {
      method: "POST",
      body: { uid, token }
    })

    success.value = true
  } catch (err) {
    error.value = err.data?.error || "Verification failed"
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="container">
    <h1>Email verification</h1>

    <div v-if="loading">Verifying...</div>

    <div v-else-if="success" class="success">
      ✅ Email successfully verified!
      <NuxtLink to="/login">Go to login</NuxtLink>
    </div>

    <div v-else class="error">
      ❌ {{ error }}
    </div>
  </div>
</template>