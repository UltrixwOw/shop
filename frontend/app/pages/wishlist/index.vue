<script setup lang="ts">
import { useWishlistStore } from '~/stores/wishlist'
import { useProductsStore } from '~/stores/products'
import { useProductPreviewModalStore } from '~/stores/productPreviewModal'

const wishlist = useWishlistStore()
const productsStore = useProductsStore()
const previewModal = useProductPreviewModalStore()
const toast = useToast()
const { requireAuth } = useRequireAuth()

// Состояния загрузки
const loading = ref(true)
const error = ref<string | null>(null)

// Инициализируем wishlist
onMounted(async () => {
  try {
    await wishlist.init()
    
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

const removeFromWishlist = async (productId: number) => {
  try {
    await wishlist.removeFromWishlist(productId)
    toast.add({
      title: 'Removed',
      description: 'Product removed from wishlist',
      color: 'success'
    })
  } catch (err) {
    toast.add({
      title: 'Error',
      description: 'Failed to remove product',
      color: 'error'
    })
  }
}

const handleShareWishlist = () => {
  requireAuth(async () => {
    if (!wishlist.items.length) {
      toast.add({
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

      toast.add({
        title: 'Link copied',
        description: 'Wishlist link copied to clipboard',
        color: 'success'
      })
    } catch (err) {
      toast.add({
        title: 'Error',
        description: 'Failed to generate share link',
        color: 'error'
      })
    }
  })
}

const openPreview = (product: any) => {
  previewModal.open(product);
};

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
        @click="handleShareWishlist"
      >
        Share
      </UButton>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <USkeleton v-for="n in 3" :key="n" class="h-96 rounded-lg" />
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
        class="relative flex flex-col justify-between cursor-pointer hover:shadow-lg transition"
        @click="openPreview(product)"
      >
        <!-- Кнопка удаления из избранного -->
        <div class="absolute top-2 right-2 z-20" @click.stop="removeFromWishlist(product.id)">
          <UButton
            icon="i-heroicons-heart-solid"
            color="neutral"
            variant="ghost"
            size="sm"
            class="rounded-full text-myPink-500 "
          />
        </div>

        <!-- Image -->
        <div class="aspect-square overflow-hidden rounded-md mb-4">
          <NuxtImg
            v-if="product.images?.length"
            :src="product.images[0].image"
            :srcset="[]"
            :alt="product.name"
            loading="lazy"
            format="webp"
            quality="80"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            class="w-full h-full object-cover hover:scale-105 transition"
          />

          <NuxtImg
            v-else
            src="/images/productPreview.png"
            :srcset="[]"
            alt="Product placeholder"
            loading="lazy"
            format="webp"
            quality="80"
            class="w-full h-full object-cover hover:scale-105 transition"
          />
        </div>

        <h3 class="text-lg font-semibold mb-2">
          {{ product.name }}
        </h3>

        <div>
          <AppRatingView
            :rating="Number(product.average_rating || 0)"
            :count="product.reviews_count || 0"
          />
        </div>

        <div class="flex justify-between items-center mt-4">
          <AppMoney class="tabular-nums text-primary font-bold text-xl" :value="product.price" />

          <AppAddToCartButton
            :productId="product.id"
            :disabled="product.stock === 0"
            class="relative z-10 w-max"
            @click.stop
          />
        </div>
      </UCard>
    </div>
  </div>
</template>