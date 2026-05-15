<script setup lang="ts">
import { reactive, watch, computed } from "vue";
import { useDebounceFn } from "@vueuse/core";

import { useCartStore } from "~/stores/cart";
import { useCartModalStore } from "~/stores/cartModal";
import { useProductPreviewModalStore } from "~/stores/productPreviewModal";

const { t } = useI18n();

const cart = useCartStore();
const modal = useCartModalStore();
const previewModal = useProductPreviewModalStore();

const localePath = useLocalePath();

// =============================
// INIT
// =============================

onMounted(async () => {
  await cart.init();
});

// =============================
// LOCAL STATE
// =============================

const localQty = reactive<Record<number, number>>({});

const confirmOpen = reactive<Record<number, boolean>>({});

// =============================
// SYNC LOCAL QTY
// =============================

watch(
  () => cart.items,
  (items) => {
    if (!items || items.length === 0) {
      Object.keys(localQty).forEach((key) => {
        delete localQty[Number(key)];
      });

      Object.keys(confirmOpen).forEach((key) => {
        delete confirmOpen[Number(key)];
      });

      return;
    }

    items.forEach((item) => {
      // quantity sync
      if (!localQty[item.id] || localQty[item.id] !== item.quantity) {
        localQty[item.id] = item.quantity;
      }

      // popover state init
      if (confirmOpen[item.id] === undefined) {
        confirmOpen[item.id] = false;
      }
    });

    const currentIds = new Set(items.map((i) => i.id));

    Object.keys(localQty).forEach((id) => {
      if (!currentIds.has(Number(id))) {
        delete localQty[Number(id)];
      }
    });

    Object.keys(confirmOpen).forEach((id) => {
      if (!currentIds.has(Number(id))) {
        delete confirmOpen[Number(id)];
      }
    });
  },
  {
    immediate: true,
    deep: true,
  }
);

// =============================
// UPDATE QUANTITY
// =============================

const debouncedUpdate = useDebounceFn(async (id: number, qty: number) => {
  try {
    await cart.updateQuantity(id, qty);
  } catch (error) {
    console.error("Failed to update quantity:", error);

    const item = cart.items.find((i) => i.id === id);

    if (item) {
      localQty[id] = item.quantity;
    }
  }
}, 400);

const update = (item: any, value: number | null) => {
  if (!value || value < 1) {
    value = 1;
  }

  if (value > item.product_stock) {
    value = item.product_stock;
  }

  localQty[item.id] = value;

  debouncedUpdate(item.id, value);
};

// =============================
// REMOVE
// =============================

const remove = async (id: number) => {
  try {
    await cart.removeFromCart(id);

    delete localQty[id];

    confirmOpen[id] = false;
  } catch (error) {
    console.error("Failed to remove item:", error);
  }
};

// =============================
// CHECKOUT
// =============================

const checkoutOrder = async () => {
  if (cart.isEmpty) return;

  modal.close();

  await navigateTo("/checkout");
};

// =============================
// TOTAL
// =============================

const totalWithLocalQty = computed(() => {
  return cart.items.reduce((sum, item) => {
    const qty = localQty[item.id] ?? item.quantity;

    return sum + item.price * qty;
  }, 0);
});

// =============================
// PREVIEW
// =============================

const openPreview = async (productId: number) => {
  if (!productId) return;

  await previewModal.open(productId);
};
</script>

<template>
  <UModal
    v-model:open="modal.isOpen"
    :title="$t('cart')"
    :description="$t('your_cart')"
    class="max-w-3xl"
  >
    <template #body>
      <!-- LOADING -->
      <div v-if="cart.loading" class="text-center py-10">
        <UIcon
          name="i-heroicons-arrow-path"
          class="w-8 h-8 mx-auto animate-spin text-gray-400"
        />

        <p class="mt-2 text-gray-500">
          {{ $t("cart_loading") }}
        </p>
      </div>

      <!-- EMPTY -->
      <div v-else-if="cart.isEmpty" class="text-gray-500 text-center py-10">
        <UIcon
          name="i-heroicons-shopping-bag"
          class="w-16 h-16 mx-auto mb-4 text-gray-300"
        />

        <p class="text-lg">
          {{ $t("empty_cart") }}
        </p>

        <UButton
          :to="localePath('/products')"
          color="primary"
          class="mt-4"
          @click="modal.close()"
        >
          {{ $t("go_to_products") }}
        </UButton>
      </div>

      <!-- ITEMS -->
      <div v-else class="space-y-5">
        <UCard
          v-for="item in cart.items"
          :key="item.id"
          class="relative"
        >
          <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <!-- PRODUCT -->
            <div
              class="flex items-center gap-4 relative z-10 cursor-pointer"
              @click.stop="openPreview(item.product)"
            >
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
                    class="tabular-nums text-gray-400 text-lg relative z-10"
                    :value="item.price * (localQty[item.id] ?? item.quantity)"
                  />

                  <p
                    v-if="localQty[item.id] >= item.product_stock"
                    class="text-xs text-red-500 absolute whitespace-nowrap"
                  >
                    {{
                      $t("max_stock", {
                        stock: item.product_stock,
                      })
                    }}
                  </p>
                </div>
              </div>
            </div>

            <!-- DELETE -->
            <UPopover v-model:open="confirmOpen[item.id]">
              <UButton
                size="sm"
                color="error"
                variant="ghost"
                icon="i-heroicons-trash"
                class="absolute top-2 right-2 z-20"
                :loading="cart.loading"
                @click.stop
              />

              <template #content>
                <div class="p-4 w-72">
                  <h4 class="font-semibold mb-2">
                    {{ $t("remove_product") }}
                  </h4>

                  <p class="text-sm text-gray-500 mb-2">
                    {{ item.product_name }}
                  </p>

                  <p class="text-sm mb-4">
                    {{ $t("remove_product_confirm") }}
                  </p>

                  <div class="flex gap-2">
                    <UButton
                      block
                      color="neutral"
                      variant="soft"
                      @click="confirmOpen[item.id] = false"
                    >
                      {{ $t("cancel") }}
                    </UButton>

                    <UButton
                      block
                      color="error"
                      :loading="cart.loading"
                      @click.stop="remove(item.id)"
                    >
                      {{ $t("delete") }}
                    </UButton>
                  </div>
                </div>
              </template>
            </UPopover>
          </div>
        </UCard>
      </div>
    </template>

    <template v-if="!cart.isEmpty && !cart.loading" #footer>
      <div class="flex w-full gap-4 justify-between items-center flex-col">
        <!-- TOTAL -->
        <div class="flex items-center">
          <span class="text-2xl mr-4 text-gray-400">
            {{ $t("cart_total") }}:
          </span>

          <span class="text-2xl font-bold text-primary">
            <AppMoney :value="totalWithLocalQty" />
          </span>
        </div>

        <!-- ACTIONS -->
        <div class="flex justify-between items-center w-full">
          <UButton
            block
            size="md"
            class="mr-4"
            color="neutral"
            variant="soft"
            :to="'/products'"
            @click.stop="modal.close()"
          >
            {{ $t("continue_shopping") }}
          </UButton>

          <UButton
            block
            size="md"
            :disabled="cart.isEmpty"
            :loading="cart.loading"
            @click="checkoutOrder"
          >
            {{ $t("checkout") }}
          </UButton>
        </div>
      </div>
    </template>
  </UModal>
</template>