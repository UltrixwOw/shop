<script setup lang="ts">
import { useCartStore } from '~/stores/cart'
import { useCartModalStore } from '~/stores/cartModal'

const cart = useCartStore()
const modal = useCartModalStore()

await cart.fetchCart()

const increase = (item: any) => {
  cart.updateQuantity(item.id, item.quantity + 1)
}

const decrease = (item: any) => {
  if (item.quantity > 1) {
    cart.updateQuantity(item.id, item.quantity - 1)
  }
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
    class="max-w-2xl"
  >
    <template #body>
      <div v-if="cart.isEmpty">
        <UAlert
          color="neutral"
          variant="soft"
          title="Корзина пуста"
        />
      </div>

      <div v-else class="space-y-5">

        <UCard
          v-for="item in cart.items"
          :key="item.id"
          class="p-5"
        >
          <div class="flex justify-between items-center">

            <!-- LEFT -->
            <div class="space-y-1">
              <h4 class="font-semibold text-lg">
                {{ item.product_name }}
              </h4>

              <p class="text-sm text-zinc-500">
                ${{ item.price }}
              </p>
            </div>

            <!-- CENTER QUANTITY -->
            <div class="flex items-center gap-4">

              <UButton
                size="sm"
                variant="soft"
                class="w-10 h-10 rounded-full text-lg font-bold"
                @click="decrease(item)"
              >
                -
              </UButton>

              <span class="w-8 text-center text-lg font-semibold">
                {{ item.quantity }}
              </span>

              <UButton
                size="sm"
                variant="soft"
                class="w-10 h-10 rounded-full text-lg font-bold"
                @click="increase(item)"
              >
                +
              </UButton>

            </div>

            <!-- RIGHT PRICE + REMOVE -->
            <div class="flex items-center gap-4">

              <span class="font-semibold text-primary text-lg">
                ${{ (item.price * item.quantity).toFixed(2) }}
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

        <div class="flex justify-between items-center pt-6 border-t">
          <span class="text-lg font-semibold">
            Итого:
          </span>

          <span class="text-2xl font-bold text-primary">
            ${{ cart.totalPrice.toFixed(2) }}
          </span>
        </div>

      </div>
    </template>

    <template #footer>
      <div class="flex gap-3 w-full">
        <UButton
          variant="ghost"
          block
          @click="modal.close()"
        >
          Закрыть
        </UButton>

        <UButton
          block
          :disabled="cart.isEmpty"
          @click="checkoutOrder"
        >
          Оформить заказ
        </UButton>
      </div>
    </template>
  </UModal>
</template>