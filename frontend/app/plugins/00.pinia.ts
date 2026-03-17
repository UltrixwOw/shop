import type { Pinia } from 'pinia'

export default defineNuxtPlugin((nuxtApp) => {

  (nuxtApp.$pinia as Pinia).use(({ store }) => {

    if (process.server) {

      console.log('🧠 pinia SSR store', store.$id)

    }

    if (process.client) {

      console.log('🌐 pinia client hydrate', store.$id)

    }

    // hydration guard
    store.$subscribe((mutation, state) => {

      if (store.$id === 'auth') {

        console.log('🔐 auth mutation', mutation.type)

      }

    })

  })

})