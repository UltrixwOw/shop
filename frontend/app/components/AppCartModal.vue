<script setup lang="ts">
import { reactive, watch } from "vue";
import { useDebounceFn } from "@vueuse/core";
import { useCartStore } from "~/stores/cart";
import { useCartModalStore } from "~/stores/cartModal";

const cart = useCartStore();
const modal = useCartModalStore();

onMounted(async () => {
  await cart.fetchCart()
})

const localQty = reactive<Record<number, number>>({});

watch(
  () => cart.items,
  (items) => {
    items.forEach((item) => {
      if (!localQty[item.id]) {
        localQty[item.id] = item.quantity;
      }
    });
  },
  { immediate: true }
);

const debouncedUpdate = useDebounceFn((id: number, qty: number) => {
  cart.updateQuantity(id, qty);
}, 400);

const update = (item: any, value: number | null) => {
  if (!value) value = 1;

  if (value < 1) value = 1;

  if (value > item.product_stock) {
    value = item.product_stock;
  }

  localQty[item.id] = value;
  debouncedUpdate(item.id, value);
};

const remove = (id: number) => {
  cart.removeFromCart(id);
};

const checkoutOrder = async () => {
  if (cart.isEmpty) return;
  modal.close();
  navigateTo("/checkout");
};

console.log(cart.items);
</script>

<template>
  <UModal
    v-model:open="modal.isOpen"
    title="Корзина"
    description="Ваши товары"
    class="max-w-3xl"
  >
    <template #body>
      <!-- EMPTY -->
      <div v-if="cart.isEmpty" class="text-gray-500 text-center py-10">
        <UIcon
          name="i-heroicons-shopping-bag"
          class="w-16 h-16 mx-auto mb-4 text-gray-300"
        />
        <p class="text-lg">Your cart is empty.</p>
        <UButton
          to="/products"
          color="primary"
          variant="soft"
          class="mt-4"
          @click="modal.close()"
        >
          Browse Products
        </UButton>
      </div>

      <!-- CART ITEMS -->
      <div v-else class="space-y-5">
        <UCard v-for="item in cart.items" :key="item.id" class="p-5 relative">
          <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <!-- ITEM -->
            <div class="flex items-center gap-4 relative z-2">
              <NuxtImg
                :src="item.product_image || '/images/productPreview.png'"
                :alt="item.product_name"
                format="webp"
                quality="80"
                class="w-16 h-16 rounded-md object-cover"
              />

              <div>
                <h4 class="font-semibold">
                  {{ item.product_name }}
                </h4>

                <p class="text-sm text-zinc-400">
                  <AppMoney :value="item.price" />
                </p>
              </div>
            </div>

            <!-- CONTROLS -->
            <div class="flex flex-col items-center gap-2 md:items-end">
              <div class="flex justify-between items-center gap-4 w-full">
                <div
                  class="flex md:justify-center justify-between md:absolute md:left-0 md:right-0 w-full"
                >
                  <UInputNumber
                    :model-value="localQty[item.id] ?? item.quantity"
                    :min="1"
                    :max="item.product_stock"
                    class="w-28"
                    size="md"
                    @update:model-value="(value) => update(item, value)"
                  />
                </div>
                <div class="relative">
                  <AppMoney
                    class="tabular-nums text-gray-400 text-lg relative z-2"
                    :value="Number(item.price) * (localQty[item.id] ?? item.quantity)"
                  />
                  <!-- MAX STOCK MESSAGE -->
                  <p
                    v-if="localQty[item.id] >= item.product_stock"
                    class="text-xs text-red-500 absolute"
                  >
                    Max stock reached
                  </p>
                </div>
              </div>
            </div>

            <UButton
              size="sm"
              color="error"
              variant="ghost"
              icon="i-heroicons-trash"
              class="absolute top-2 right-2 z-20"
              @click="remove(item.id)"
            />
          </div>
        </UCard>
      </div>
    </template>

    <template v-if="!cart.isEmpty" #footer>
      <div class="flex w-full gap-4 justify-between">
        <!--<UButton
          variant="ghost"
          block
          icon="i-heroicons-shopping-bag"
          to="/products"
          @click="modal.close()"
        >
          Продолжить покупки
        </UButton> -->
        <!-- TOTAL -->
        <div class="flex relative md:flex-row md:justify-between md:items-center w-50 flex-col items-start">
          <span class="text-md text-gray-400 absolute -top-3"> Итого: </span>

          <span class="text-2xl font-bold text-primary pt-1">
            <AppMoney :value="cart.totalPrice" />
          </span>
        </div>

        <UButton class="w-50" block size="lg" :disabled="cart.isEmpty" @click="checkoutOrder">
          Оформить заказ
        </UButton>
      </div>
    </template>
  </UModal>
</template>
