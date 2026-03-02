<script setup lang="ts">
import { useCartStore } from '~/stores/cart'
import { useCartModalStore } from '~/stores/cartModal'

const cart = useCartStore()
const modal = useCartModalStore()

await cart.fetchCart()

const increase = (item: any) => {
  if (item.quantity >= item.product_stock) return
  cart.updateQuantity(item.id, item.quantity + 1)
}

const decrease = (item: any) => {
  if (item.quantity <= 1) return
  cart.updateQuantity(item.id, item.quantity - 1)
}

const remove = (id: number) => {
  cart.removeFromCart(id)
}

const checkoutOrder = async () => {
  if (cart.isEmpty) return
  modal.close()
  navigateTo('/checkout')
}
</script>

<template>
  <UModal
    v-model:open="modal.isOpen"
    title="Корзина"
    description="Ваши товары"
    class="max-w-3xl"
  >
    <template #body>
      <div v-if="cart.isEmpty">
        <UAlert
          color="neutral"
          variant="soft"
          title="Корзина пуста"
        />
      </div>

      <div v-else class="space-y-6">

        <UCard
          v-for="item in cart.items"
          :key="item.id"
          class="p-6"
        >
          <div class="flex justify-between items-center">

            <!-- LEFT -->
            <div class="space-y-1">
              <h4 class="font-semibold text-lg">
                {{ item.product_name }}
              </h4>

              <p class="text-sm text-zinc-500">
                ${{ Number(item.price).toFixed(2) }}
              </p>

              <p
                v-if="item.quantity >= item.product_stock"
                class="text-xs text-red-500"
              >
                Max stock reached
              </p>
            </div>

            <!-- CENTER QUANTITY -->
            <div class="flex items-center gap-5">

              <UButton
                size="lg"
                variant="soft"
                class="w-12 h-12 rounded-full text-xl font-bold"
                :disabled="item.quantity <= 1"
                @click="decrease(item)"
              >
                -
              </UButton>

              <span class="w-10 text-center text-xl font-semibold">
                {{ item.quantity }}
              </span>

              <UButton
                size="lg"
                variant="soft"
                class="w-12 h-12 rounded-full text-xl font-bold"
                :disabled="item.quantity >= item.product_stock"
                @click="increase(item)"
              >
                +
              </UButton>

            </div>

            <!-- RIGHT PRICE + REMOVE -->
            <div class="flex items-center gap-5">

              <span class="font-semibold text-primary text-xl">
                ${{ (Number(item.price) * item.quantity).toFixed(2) }}
              </span>

              <UButton
                size="sm"
                color="error"
                variant="ghost"
                icon="i-heroicons-trash"
                @click="remove(item.id)"
              />

            </div>

          </div>
        </UCard>

        <!-- TOTAL -->
        <div class="flex justify-between items-center pt-6 border-t">
          <span class="text-xl font-semibold">
            Итого:
          </span>

          <span class="text-3xl font-bold text-primary">
            ${{ cart.totalPrice.toFixed(2) }}
          </span>
        </div>

      </div>
    </template>

    <template #footer>
      <div class="flex gap-4 w-full">
        <UButton
          variant="ghost"
          block
          @click="modal.close()"
        >
          Закрыть
        </UButton>

        <UButton
          block
          size="lg"
          :disabled="cart.isEmpty"
          @click="checkoutOrder"
        >
          Оформить заказ
        </UButton>
      </div>
    </template>
  </UModal>
</template>