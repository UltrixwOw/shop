export default defineNuxtRouteMiddleware(async () => {

  const auth = await useAuthReady()

  if (!auth.isAuthenticated) {
    return navigateTo('/')
  }

})