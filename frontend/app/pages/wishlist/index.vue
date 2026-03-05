<script setup lang="ts">
import { useWishlistStore } from '~/stores/wishlist'
import { useProductsStore } from '~/stores/products'

const wishlist = useWishlistStore()
const productsStore = useProductsStore()

// Состояния загрузки
const loading = ref(true)
const error = ref<string | null>(null)

// Загружаем данные при монтировании
onMounted(async () => {
  try {
    // Загружаем избранное
    await wishlist.fetchWishlist()
    
    // Загружаем товары, если их нет
    if (!productsStore.items.length) {
      await productsStore.fetchProducts()
    }
  } catch (err) {
    error.value = 'Failed to load wishlist'
    console.error(err)
  } finally {
    loading.value = false
  }
})

// Вычисляем товары из избранного
const wishlistProducts = computed(() => {
  if (!productsStore.items.length || !wishlist.items.length) return []
  
  return productsStore.items.filter(p =>
    wishlist.items.includes(p.id)
  )
})

// ✅ ИСПРАВЛЕНО: remove → removeFromWishlist
const removeFromWishlist = async (productId: number) => {
  try {
    await wishlist.removeFromWishlist(productId)
    useToast().add({
      title: 'Removed',
      description: 'Product removed from wishlist',
      color: 'success'
    })
  } catch (err) {
    useToast().add({
      title: 'Error',
      description: 'Failed to remove product',
      color: 'error'
    })
  }
}

const shareWishlist = async () => {
  if (!wishlist.items.length) {
    useToast().add({
      title: 'Empty',
      description: 'Your wishlist is empty',
      color: 'warning'
    })
    return
  }

  try {
    const share = await wishlist.generateShare()
    if (!share?.token) return

    const url = `${window.location.origin}/wishlist/share/${share.token}`
    await navigator.clipboard.writeText(url)

    useToast().add({
      title: 'Link copied',
      description: 'Wishlist link copied to clipboard',
      color: 'success'
    })
  } catch (err) {
    useToast().add({
      title: 'Error',
      description: 'Failed to generate share link',
      color: 'error'
    })
  }
}

// Для SSR - загружаем данные на сервере
if (import.meta.server) {
  await Promise.all([
    wishlist.fetchWishlist(),
    productsStore.fetchProducts()
  ])
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-10">

    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold">
        Wishlist
      </h1>

      <UButton
        icon="i-heroicons-share"
        variant="soft"
        :disabled="!wishlist.items.length"
        @click="shareWishlist"
      >
        Share
      </UButton>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <USkeleton v-for="n in 3" :key="n" class="h-64 rounded-xl" />
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="text-red-500 text-center py-10">
      {{ error }}
    </div>

    <!-- Пустой список -->
    <div
      v-else-if="!wishlistProducts.length"
      class="text-gray-500 text-center py-10"
    >
      <UIcon name="i-heroicons-heart" class="w-16 h-16 mx-auto mb-4 text-gray-300" />
      <p class="text-lg">Your wishlist is empty.</p>
      <UButton
        to="/products"
        color="primary"
        variant="soft"
        class="mt-4"
      >
        Browse Products
      </UButton>
    </div>

    <!-- Список товаров -->
    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <UCard
        v-for="product in wishlistProducts"
        :key="product.id"
        class="flex flex-col justify-between"
      >
        <div>
          <NuxtImg
            v-if="product.images?.length"
            :src="product.images[0].image"
            :alt="product.name"
            class="w-full h-48 object-cover rounded-lg mb-4"
          />
          
          <h2 class="text-lg font-semibold mb-2">
            {{ product.name }}
          </h2>

          <p class="text-primary font-bold mb-4">
            ${{ product.price }}
          </p>
        </div>

        <div class="flex items-center gap-2">
          <AppAddToCartButton
            :productId="product.id"
            :disabled="product.stock === 0"
            class="flex-1"
          />

          <UButton
            icon="i-heroicons-trash"
            color="red"
            variant="soft"
            @click="removeFromWishlist(product.id)"
          />
        </div>
      </UCard>
    </div>

  </div>
</template>