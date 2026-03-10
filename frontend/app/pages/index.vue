<script setup lang="ts">
import type { ButtonProps } from "@nuxt/ui";

const links = ref<ButtonProps[]>([
  {
    label: "Начать покупки",
    to: "/products",
    icon: "i-heroicons-shopping-bag",
  },
  {
    label: "Узнать больше",
    to: "/about",
    color: "neutral",
    variant: "subtle",
    trailingIcon: "i-lucide-arrow-right",
  },
]);

const cards = ref([
  {
    title: "Быстрая доставка",
    description:
      "Доставляем заказы по всему миру в кратчайшие сроки.",
    icon: "i-heroicons-truck",
  },
  {
    title: "Безопасная оплата",
    description:
      "Ваши платежные данные надежно защищены.",
    icon: "i-heroicons-shield-check",
  },
  {
    title: "Поддержка 24/7",
    description:
      "Всегда готовы помочь с любым вопросом.",
    icon: "i-heroicons-chat-bubble-left-right",
  },
]);
</script>

<template>
  <UContainer>
    <div>
      <UPageHero
        title="Добро пожаловать к Meloni"
        description="Откройте для себя уникальные товары и наслаждайтесь удобным шопингом с доставкой по всему миру."
        :links="links"
      />
    </div>
    <div>
      <UPageGrid>
        <UPageCard v-for="(card, index) in cards" :key="index" v-bind="card" />
      </UPageGrid>
    </div>
  </UContainer>
</template>
