<!-- pages/wishlist/share/[uuid].vue -->
<script setup lang="ts">
import { useProductsStore } from '~/stores/products'

const route = useRoute()
const router = useRouter()
const { $api } = useNuxtApp()
const productsStore = useProductsStore()

const token = route.params.uuid as string

// Загружаем публичный вишлист
const { data: wishlistData, pending: wishlistPending } = await useAsyncData(
  `wishlist-shared-${token}`,
  async () => {
    try {
      const res = await $api.get(`/wishlist/public/${token}/`)
      return res.data
    } catch (err: any) {
      if (err.response?.status === 404) {
        throw createError({
          statusCode: 404,
          statusMessage: 'Public wishlist not found',
          fatal: true
        })
      }
      throw err
    }
  }
)

// Получаем ID товаров из вишлиста
const productIds = computed(() => wishlistData.value?.products || [])

// Загружаем товары через store (как в index.vue)
const { data: products, pending: productsPending } = await useAsyncData(
  `wishlist-products-${token}`,
  async () => {
    if (!productIds.value.length) return []
    
    // Используем fetchProducts из store
    await productsStore.fetchProducts()
    
    // Фильтруем только те товары, которые есть в вишлисте
    return productsStore.items.filter(p => productIds.value.includes(p.id))
  },
  {
    watch: [productIds],
    server: true
  }
)

// Если товары загружены, обновляем store
if (products.value) {
  // Не перезаписываем весь store, а только добавляем нужные товары
  const existingIds = new Set(productsStore.items.map(p => p.id))
  const newProducts = products.value.filter(p => !existingIds.has(p.id))
  productsStore.items = [...productsStore.items, ...newProducts]
}

// Товары для отображения (из computed, как в index.vue)
const wishlistProducts = computed(() => {
  if (!productIds.value.length || !productsStore.items.length) return []
  return productsStore.items.filter(p => productIds.value.includes(p.id))
})

// Добавление в корзину
const addToCart = async (productId: number) => {
  try {
    await $api.post('/cart/add/', { product_id: productId, quantity: 1 })
    useToast().add({
      title: 'Added to cart',
      description: 'Product has been added to your cart',
      color: 'success'
    })
  } catch (err: any) {
    useToast().add({
      title: 'Error',
      description: err.response?.data?.detail || 'Failed to add to cart',
      color: 'error'
    })
  }
}

// Мета-теги
useHead({
  title: wishlistData.value 
    ? `${wishlistData.value.user}'s Wishlist` 
    : 'Shared Wishlist',
  meta: [
    {
      name: 'description',
      content: wishlistData.value
        ? `Check out ${wishlistData.value.user}'s wishlist with ${wishlistData.value.products.length} items`
        : 'Shared wishlist'
    }
  ]
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-10">

    <!-- Шапка -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold mb-2">
          Shared Wishlist
        </h1>
        <p v-if="wishlistData?.user" class="text-gray-500">
          by {{ wishlistData.user }}
        </p>
        <p v-if="wishlistData?.products" class="text-sm text-gray-400">
          {{ wishlistData.products.length }} items
        </p>
      </div>

      <UButton
        icon="i-heroicons-arrow-left"
        variant="soft"
        @click="router.back()"
      >
        Go Back
      </UButton>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="wishlistPending || productsPending" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <USkeleton v-for="n in 6" :key="n" class="h-80 rounded-xl" />
    </div>

    <!-- Пустой вишлист -->
    <div
      v-else-if="!wishlistData?.products?.length"
      class="text-center py-20"
    >
      <UIcon
        name="i-heroicons-heart"
        class="w-20 h-20 mx-auto mb-4 text-gray-300"
      />
      <p class="text-xl text-gray-500 mb-2">
        This wishlist is empty
      </p>
      <p class="text-gray-400 mb-6">
        The user hasn't added any items yet
      </p>
    </div>

    <!-- Сетка товаров (точно как в index.vue) -->
    <div
      v-else-if="wishlistProducts.length"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <UCard
        v-for="product in wishlistProducts"
        :key="product.id"
        class="relative flex flex-col justify-between cursor-pointer hover:shadow-lg transition"
        @click="navigateTo(`/products/${product.id}`)"
      >
        <!-- Изображение -->
        <div class="aspect-square overflow-hidden rounded-md mb-4">
          <NuxtImg
            v-if="product.images?.length"
            :src="product.images[0].image"
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
            alt="Product placeholder"
            loading="lazy"
            format="webp"
            quality="80"
            class="w-full h-full object-cover hover:scale-105 transition"
          />
        </div>

        <!-- Информация -->
        <h3 class="text-lg font-semibold mb-2 line-clamp-2">
          {{ product.name }}
        </h3>

        <div class="flex justify-between items-center">
          <p class="text-primary font-bold text-xl">
            ${{ product.price }}
          </p>

          <UBadge
            v-if="product.stock > 0"
            color="success"
            variant="soft"
            size="sm"
          >
            In stock
          </UBadge>
          <UBadge
            v-else
            color="error"
            variant="soft"
            size="sm"
          >
            Out of stock
          </UBadge>
        </div>

        <!-- Кнопка добавления в корзину -->
        <div class="mt-4">
          <UButton
            :disabled="product.stock === 0"
            icon="i-heroicons-shopping-cart"
            color="primary"
            block
            @click.stop="addToCart(product.id)"
          >
            Add to Cart
          </UButton>
        </div>
      </UCard>
    </div>

    <!-- Если товары не найдены -->
    <div
      v-else
      class="text-center py-20 text-gray-500"
    >
      <p>No products found in this wishlist</p>
    </div>

  </div>
</template>