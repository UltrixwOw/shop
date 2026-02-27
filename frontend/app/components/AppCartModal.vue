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

      <div v-else class="space-y-6">
        <UCard
          v-for="item in cart.items"
          :key="item.id"
        >
          <div class="flex justify-between items-start gap-4">

            <div>
              <h4 class="font-semibold">
                {{ item.product_name }}
              </h4>
              <p class="text-sm text-gray-500">
                ${{ item.product_price }}
              </p>
            </div>

            <div class="flex items-center gap-2">

              <UButton
                size="xs"
                variant="soft"
                @click="decrease(item)"
              >
                -
              </UButton>

              <span class="w-6 text-center">
                {{ item.quantity }}
              </span>

              <UButton
                size="xs"
                variant="soft"
                @click="increase(item)"
              >
                +
              </UButton>

            </div>

            <UButton
              size="xs"
              color="error"
              variant="ghost"
              icon="i-heroicons-trash"
              @click="remove(item.id)"
            />

          </div>
        </UCard>

        <div class="flex justify-between items-center pt-4 border-t">
          <span class="text-lg font-semibold">
            Итого:
          </span>

          <span class="text-xl font-bold text-primary">
            ${{ cart.totalPrice }}
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