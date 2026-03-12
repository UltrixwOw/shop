<script setup lang="ts">
import { useImgModalStore } from "~/stores/imgModal";
import { useCartStore } from "~/stores/cart";
import { useProductsStore } from "~/stores/products";

const route = useRoute();
const { $api } = useNuxtApp();
const imgModal = useImgModalStore();
const cartStore = useCartStore();
const productsStore = useProductsStore();

const id = computed(() => route.params.id);
const error = ref<string | null>(null);

// Загружаем продукт на сервере (await гарантирует, что данные будут до рендера)
const { data: product } = await useAsyncData(`product-${id.value}`, async () => {
  try {
    const res = await $api.get(`/shop/products/${id.value}/`);
    const productData = res.data;

    // Добавляем продукт в productsStore на сервере
    if (process.client && !productsStore.items.find((p) => p.id === productData.id)) {
      // На клиенте добавляем в стор
      productsStore.items.unshift(productData);
    } else if (process.server) {
      // На сервере тоже добавляем для консистентности
      productsStore.items.unshift(productData);
    }

    return productData;
  } catch (err) {
    error.value = "Failed to load product";
    console.error(err);
    return null;
  }
});

// Загружаем корзину (только на клиенте, поисковикам корзина не нужна)
onMounted(async () => {
  try {
    if (!cartStore.initialized) {
      await cartStore.fetchCart();
    }
  } catch (err) {
    console.error("Failed to load cart", err);
  }
});

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

// Мета-теги для SEO
useHead({
  title: product.value?.name ? `${product.value.name} | Shop` : 'Product | Shop',
  meta: [
    {
      name: 'description',
      content: product.value?.description || 'Product description'
    },
    {
      property: 'og:title',
      content: product.value?.name || 'Product'
    },
    {
      property: 'og:description',
      content: product.value?.description || 'Product description'
    },
    {
      property: 'og:image',
      content: product.value?.images?.[0]?.image || '/images/productPreview.png'
    }
  ]
});
</script>

<template>
  <UContainer>
    <!-- Ошибка -->
    <div v-if="error" class="py-8">
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

    <!-- Продукт загружен - сразу рендерится с данными -->
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