<script setup lang="ts">
import { useImgModalStore } from "~/stores/imgModal";
import { useCartStore } from "~/stores/cart";
import { useProductsStore } from "~/stores/products"; // <-- Добавляем

const route = useRoute();
const { $api } = useNuxtApp();
const imgModal = useImgModalStore();
const cartStore = useCartStore();
const productsStore = useProductsStore(); // <-- Добавляем

const id = computed(() => route.params.id);
const loading = ref(true);
const error = ref<string | null>(null);

// Загружаем продукт
const { data: product } = await useAsyncData(`product-${id.value}`, async () => {
  const res = await $api.get(`/shop/products/${id.value}/`);
  const productData = res.data;

  // Добавляем продукт в productsStore, чтобы AppAddToCartButton его увидел
  if (!productsStore.items.find((p) => p.id === productData.id)) {
    // Добавляем в начало массива, чтобы не перезаписывать другие товары
    productsStore.items.unshift(productData);
  }

  return productData;
});

// Загружаем корзину как в products
onMounted(async () => {
  try {
    if (!cartStore.initialized) {
      await cartStore.fetchCart();
    }
  } catch (err) {
    error.value = "Failed to load cart";
    console.error(err);
  } finally {
    loading.value = false;
  }
});

// Для SSR - грузим корзину на сервере
if (import.meta.server && !cartStore.initialized) {
  await cartStore.fetchCart();
  loading.value = false;
}

// Вычисляемый массив для карусели
const carouselItems = computed(() => {
  if (product.value?.images?.length) {
    return product.value.images;
  }
  return [{ image: "/images/productPreview.png", isPlaceholder: true }];
});

function openLightbox(index: number) {
  if (!product.value?.images?.length || carouselItems.value[index]?.isPlaceholder) return;

  imgModal.open(
    product.value.images,
    index,
    product.value.name,
    product.value.description
  );
}
</script>

<template>
  <UContainer>
    <!-- Состояние загрузки - как в products -->
    <div v-if="loading" class="py-8 space-y-8">
      <USkeleton class="h-10 w-32 rounded-lg" />
      <!-- кнопка Products -->
      <USkeleton class="h-12 w-2/3 rounded-lg" />
      <!-- заголовок -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <USkeleton v-for="n in 3" :key="n" class="aspect-square rounded-lg" />
      </div>
      <USkeleton class="h-24 w-full rounded-lg" />
      <!-- описание -->
      <div class="flex items-center justify-between">
        <USkeleton class="h-10 w-24 rounded-lg" />
        <!-- цена -->
        <USkeleton class="h-10 w-32 rounded-lg" />
        <!-- кнопка Add to cart -->
      </div>
    </div>

    <!-- Ошибка - как в products -->
    <div v-else-if="error" class="py-8">
      <UAlert color="error" variant="soft" title="Error" :description="error" />
    </div>

    <!-- Продукт не найден -->
    <div v-else-if="!product" class="py-8">
      <UAlert
        color="error"
        variant="soft"
        title="Product not found"
        description="The requested product could not be found."
      />
    </div>

    <!-- Продукт загружен -->
    <div v-else class="py-8 space-y-8">
      <!-- Кнопка "Products" -->
      <UButton variant="ghost" icon="i-heroicons-shopping-bag" to="/products">
        Products
      </UButton>

      <!-- Заголовок товара -->
      <h1 class="text-3xl font-bold">{{ product.name }}</h1>

      <!-- Карусель изображений -->
      <UCarousel :items="carouselItems" :ui="{ item: 'basis-1/3' }" class="w-full">
        <template #default="{ item, index }">
          <div
            class="aspect-square overflow-hidden rounded-lg"
            :class="{ 'cursor-pointer': !item.isPlaceholder }"
            @click="!item.isPlaceholder ? openLightbox(index) : null"
          >
            <NuxtImg
              :src="item.image"
              :alt="product.name"
              format="webp"
              quality="80"
              class="w-full h-full object-cover"
              loading="lazy"
            />
          </div>
        </template>
      </UCarousel>

      <!-- Описание -->
      <p class="text-gray-400 leading-relaxed">{{ product.description }}</p>

      <USeparator />

      <!-- Цена и кнопка добавления в корзину -->
      <div class="flex items-center justify-between">
        <p class="text-2xl font-bold text-primary">${{ product.price }}</p>
        <AppAddToCartButton :productId="product.id" class="relative z-10 w-max" />
      </div>

      <USeparator />

      <!-- Отзывы -->
      <div>
        <h2 class="text-2xl font-semibold mb-4">Reviews</h2>
        <AppProductReviews :productId="product.id" />
      </div>
    </div>
  </UContainer>
</template>
